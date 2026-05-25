from rembg import remove
from engines.base import TryOnEngine, crop_to_content, uniform_fit


class SimpleEngine(TryOnEngine):
    """固定坐标粘贴引擎 + rembg 背景移除，用于回退"""

    REGION_MAPPING = {
        'T-shirt/top': (220, 150, 380, 330),
        'Pullover': (220, 150, 380, 330),
        'Dress': (210, 150, 390, 600),
        'Coat': (220, 150, 380, 360),
        'Shirt': (220, 150, 380, 330),
        'Trouser': (240, 330, 360, 680),
        'Sandal': [(250, 680, 280, 720), (320, 680, 350, 720)],
        'Sneaker': [(250, 680, 280, 720), (320, 680, 350, 720)],
        'Ankle boot': [(250, 680, 280, 720), (320, 680, 350, 720)],
        'Bag': (140, 280, 220, 400),
    }

    def composite(self, user_photo, clothing, category):
        user_photo = user_photo.resize((600, 800)).convert("RGBA")
        clothing = remove(clothing).convert("RGBA")  # rembg 移除背景，保留衣物主体透明通道
        clothing = crop_to_content(clothing)  # 裁剪到衣物实际边界框，消除图片内留白导致的贴合错位

        region = self.REGION_MAPPING.get(category)
        if region is None:
            return user_photo

        if isinstance(region, list):
            for r in region:
                fitted = self._fit(clothing, r)
                user_photo.paste(fitted, r[:2], fitted)
        else:
            fitted = self._fit(clothing, region)
            user_photo.paste(fitted, region[:2], fitted)

        return user_photo

    def _fit(self, img, region):
        return uniform_fit(img, region)
