from engines.base import TryOnEngine


class SimpleEngine(TryOnEngine):
    """固定坐标粘贴引擎，用于回退"""

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
        clothing = clothing.convert("RGBA")
        clothing.putalpha(230)

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
        tw = region[2] - region[0]
        th = region[3] - region[1]
        return img.resize((tw, th))
