import numpy as np
import cv2
from PIL import Image
from engines.base import TryOnEngine


class MediaPipeEngine(TryOnEngine):
    """MediaPipe Pose 关键点引擎"""

    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_WRIST = 15
    RIGHT_WRIST = 16

    def __init__(self):
        self._pose = None

    @property
    def pose(self):
        if self._pose is None:
            import mediapipe as mp
            self._pose = mp.solutions.pose.Pose(
                static_image_mode=True,
                model_complexity=1,
                enable_segmentation=False
            )
        return self._pose

    def _detect_keypoints(self, image):
        """返回 (keypoints_dict, image_width, image_height) 或 (None, None, None)"""
        img_rgb = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2RGB)
        results = self.pose.process(img_rgb)
        if not results.pose_landmarks:
            return None, None, None
        h, w = img_rgb.shape[:2]
        kp = {}
        for idx, lm in enumerate(results.pose_landmarks.landmark):
            kp[idx] = (int(lm.x * w), int(lm.y * h))
        return kp, w, h

    def _get_region_for_category(self, keypoints, category, img_w, img_h):

        def midpoint(a, b):
            return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)

        upper_categories = {'T-shirt/top', 'Pullover', 'Shirt', 'Coat', 'Dress'}
        lower_categories = {'Trouser'}
        shoe_categories = {'Sandal', 'Sneaker', 'Ankle boot'}
        bag_categories = {'Bag'}

        if category in upper_categories:
            if self.LEFT_SHOULDER in keypoints and self.RIGHT_SHOULDER in keypoints:
                shoulder_mid = midpoint(keypoints[self.LEFT_SHOULDER], keypoints[self.RIGHT_SHOULDER])
                x1 = max(0, shoulder_mid[0] - 120)
                x2 = min(img_w, shoulder_mid[0] + 120)
                y1 = max(0, shoulder_mid[1] - 20)
                if self.LEFT_HIP in keypoints and self.RIGHT_HIP in keypoints:
                    hip_mid = midpoint(keypoints[self.LEFT_HIP], keypoints[self.RIGHT_HIP])
                    y2 = hip_mid[1]
                else:
                    y2 = min(img_h, y1 + 250)
                return (x1, y1, x2, y2)
            return (220, 150, 380, 330) if category != 'Dress' else (210, 150, 390, 600)

        if category in lower_categories:
            if all(k in keypoints for k in [self.LEFT_HIP, self.RIGHT_HIP]):
                hip_mid = midpoint(keypoints[self.LEFT_HIP], keypoints[self.RIGHT_HIP])
                x1 = max(0, hip_mid[0] - 100)
                x2 = min(img_w, hip_mid[0] + 100)
                y1 = hip_mid[1]
                if self.LEFT_ANKLE in keypoints and self.RIGHT_ANKLE in keypoints:
                    ankle_mid = midpoint(keypoints[self.LEFT_ANKLE], keypoints[self.RIGHT_ANKLE])
                    y2 = ankle_mid[1]
                else:
                    y2 = min(img_h, y1 + 350)
                return (x1, y1, x2, y2)
            return (240, 330, 360, 680)

        if category in shoe_categories:
            regions = []
            for ankle_idx in [self.LEFT_ANKLE, self.RIGHT_ANKLE]:
                if ankle_idx in keypoints:
                    a = keypoints[ankle_idx]
                    regions.append((max(0, a[0] - 30), a[1] - 20,
                                   min(img_w, a[0] + 30), min(img_h, a[1] + 40)))
            if regions:
                return regions
            return [(250, 680, 280, 720), (320, 680, 350, 720)]

        if category in bag_categories:
            if self.LEFT_WRIST in keypoints:
                w = keypoints[self.LEFT_WRIST]
                return (max(0, w[0] - 60), max(0, w[1] - 40),
                       min(img_w, w[0] + 60), min(img_h, w[1] + 80))
            return (140, 280, 220, 400)

        return None

    def composite(self, user_photo, clothing, category):
        user_photo = user_photo.convert("RGBA")
        clothing = clothing.convert("RGBA")
        clothing.putalpha(200)

        keypoints, img_w, img_h = self._detect_keypoints(user_photo)

        if keypoints is None:
            from engines.simple import SimpleEngine
            return SimpleEngine().composite(user_photo, clothing, category)

        region = self._get_region_for_category(keypoints, category, img_w, img_h)

        if region is None:
            return user_photo

        if isinstance(region, list):
            for r in region:
                fitted = self._affine_fit(clothing, r)
                user_photo.paste(fitted, r[:2], fitted)
        else:
            fitted = self._affine_fit(clothing, region)
            user_photo.paste(fitted, region[:2], fitted)

        return user_photo

    def _affine_fit(self, img, region):
        tw = region[2] - region[0]
        th = region[3] - region[1]
        if tw <= 0 or th <= 0:
            return img
        src_pts = np.float32([[0, 0], [img.width, 0], [0, img.height]])
        dst_pts = np.float32([[0, 0], [tw, 0], [0, th]])
        matrix = cv2.getAffineTransform(src_pts, dst_pts)
        warped = cv2.warpAffine(np.array(img), matrix, (tw, th),
                                flags=cv2.INTER_LANCZOS4)
        return Image.fromarray(warped, 'RGBA')
