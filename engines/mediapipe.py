import os
import numpy as np
import cv2
from PIL import Image
from rembg import remove
from engines.base import TryOnEngine, crop_to_content, uniform_fit

# MediaPipe 0.10.x 新 API 模型路径
_MODEL_PATH = os.path.join(os.path.expanduser('~'), '.cache', 'mediapipe',
                           'pose_landmarker_lite.task')


# 继承 TryOnEngine 抽象类，要实现 composite 的方法
class MediaPipeEngine(TryOnEngine):
    """MediaPipe Pose 关键点引擎（v0.10.x tasks API）"""

    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_HIP = 23
    RIGHT_HIP = 24
    LEFT_ANKLE = 27
    RIGHT_ANKLE = 28
    LEFT_WRIST = 15
    RIGHT_WRIST = 16

    def __init__(self):
        self._landmarker = None

    # 懒加载 MediaPipe 模型，第一次调用时才加载，加载失败后不再尝试加载，避免重复报错
    @property
    def landmarker(self):
        if self._landmarker is None and os.path.exists(_MODEL_PATH):
            try:
                from mediapipe.tasks.python.vision import (
                    PoseLandmarker, PoseLandmarkerOptions, RunningMode
                )
                from mediapipe.tasks.python.core.base_options import BaseOptions

                options = PoseLandmarkerOptions(
                    base_options=BaseOptions(model_asset_path=_MODEL_PATH),
                    running_mode=RunningMode.IMAGE,
                    num_poses=1,
                )
                self._landmarker = PoseLandmarker.create_from_options(options)
            except Exception:
                self._landmarker = False  # 标记为失败，不再重试
        return self._landmarker

    def _detect_keypoints(self, image):
        """ 把图片传给 MediaPipe
            AI 识别全身关键点，坐标keypoints_dict：肩膀、腰、手腕、脚踝
            返回 (keypoints_dict, image_width, image_height) 或 (None, None, None)
        """
        if not self.landmarker or self.landmarker is False:
            return None, None, None

        try:
            import mediapipe as mp

            # 转为 MediaPipe Image
            img_rgb = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2RGB)
            h, w = img_rgb.shape[:2]
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)

            result = self.landmarker.detect(mp_image)
            if not result.pose_landmarks:
                return None, None, None

            # 取第一个检测到的人体
            landmarks = result.pose_landmarks[0]
            kp = {}
            for idx, lm in enumerate(landmarks):
                kp[idx] = (int(lm.x * w), int(lm.y * h))
            return kp, w, h
        except Exception:
            return None, None, None

# 根据关键点和类别计算衣物放置区域，返回 (x1, y1, x2, y2) 或 [(x1, y1, x2, y2), ...] 或 None
    def _get_region_for_category(self, keypoints, category, img_w, img_h):

        def midpoint(a, b):
            return ((a[0] + b[0]) // 2, (a[1] + b[1]) // 2)

        upper_categories = {'T-shirt/top',
                            'Pullover', 'Shirt', 'Coat', 'Dress'}
        lower_categories = {'Trouser'}
        shoe_categories = {'Sandal', 'Sneaker', 'Ankle boot'}
        bag_categories = {'Bag'}

        if category in upper_categories:
            if self.LEFT_SHOULDER in keypoints and self.RIGHT_SHOULDER in keypoints:
                shoulder_mid = midpoint(
                    keypoints[self.LEFT_SHOULDER], keypoints[self.RIGHT_SHOULDER])
                x1 = max(0, shoulder_mid[0] - 120)
                x2 = min(img_w, shoulder_mid[0] + 120)
                y1 = max(0, shoulder_mid[1] - 20)
                if self.LEFT_HIP in keypoints and self.RIGHT_HIP in keypoints:
                    hip_mid = midpoint(
                        keypoints[self.LEFT_HIP], keypoints[self.RIGHT_HIP])
                    y2 = hip_mid[1]
                else:
                    y2 = min(img_h, y1 + 250)
                return (x1, y1, x2, y2)

            return (220, 150, 380, 330) if category != 'Dress' else (210, 150, 390, 600)

        if category in lower_categories:
            if all(k in keypoints for k in [self.LEFT_HIP, self.RIGHT_HIP]):
                hip_mid = midpoint(
                    keypoints[self.LEFT_HIP], keypoints[self.RIGHT_HIP])
                x1 = max(0, hip_mid[0] - 100)
                x2 = min(img_w, hip_mid[0] + 100)
                y1 = hip_mid[1]
                if self.LEFT_ANKLE in keypoints and self.RIGHT_ANKLE in keypoints:
                    ankle_mid = midpoint(
                        keypoints[self.LEFT_ANKLE], keypoints[self.RIGHT_ANKLE])
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

# 将衣物合成到用户照片上，返回 RGBA 图片
    def composite(self, user_photo, clothing, category):
        user_photo = user_photo.convert("RGBA")
        # 将人物照最大边缩至 800px，确保关键点检测在一致尺度下进行
        max_dim = 800
        if max(user_photo.width, user_photo.height) > max_dim:
            scale = max_dim / max(user_photo.width, user_photo.height)
            user_photo = user_photo.resize(
                (int(user_photo.width * scale), int(user_photo.height * scale)),
                Image.LANCZOS,
            )
        clothing = remove(clothing).convert("RGBA")  # rembg 移除背景
        clothing = crop_to_content(clothing)  # 裁剪到衣物实际边界框，消除图片内留白导致的贴合错位

        keypoints, img_w, img_h = self._detect_keypoints(user_photo)

        if keypoints is None:
            from engines.simple import SimpleEngine
            return SimpleEngine().composite(user_photo, clothing, category)

        region = self._get_region_for_category(
            keypoints, category, img_w, img_h)

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
        return uniform_fit(img, region)
