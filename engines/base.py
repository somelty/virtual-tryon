from abc import ABC, abstractmethod
from PIL import Image


class TryOnEngine(ABC):
    @abstractmethod
    def composite(self, user_photo: Image.Image, clothing: Image.Image,
                  category: str) -> Image.Image:
        """将衣物合成到用户照片上，返回 RGBA 图片"""
        pass
