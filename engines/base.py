import numpy as np
from abc import ABC, abstractmethod
from PIL import Image


def crop_to_content(img: Image.Image, threshold: int = 10) -> Image.Image:
    """裁剪 RGBA 图片到非透明像素的边界框，解决衣物在图片中偏位导致的贴合错位"""
    alpha = np.array(img.getchannel('A'))
    rows = np.any(alpha > threshold, axis=1)
    cols = np.any(alpha > threshold, axis=0)
    if not rows.any() or not cols.any():
        return img
    ymin, ymax = np.where(rows)[0][[0, -1]]
    xmin, xmax = np.where(cols)[0][[0, -1]]
    return img.crop((xmin, ymin, xmax + 1, ymax + 1))


def uniform_fit(img: Image.Image, region: tuple) -> Image.Image:
    """按目标区域高度等比缩放 RGBA 衣物图，水平居中。
    衣物比区域窄则居中留透明，比区域宽则居中裁切。"""
    tw = region[2] - region[0]
    th = region[3] - region[1]
    if tw <= 0 or th <= 0:
        return img

    scale = th / img.height
    new_w = max(1, int(img.width * scale))
    new_h = th

    resized = img.resize((new_w, new_h), Image.LANCZOS)

    if new_w <= tw:
        # 衣物比区域窄：放在透明画布上水平居中
        canvas = Image.new('RGBA', (tw, th), (0, 0, 0, 0))
        left = (tw - new_w) // 2
        canvas.paste(resized, (left, 0), resized)
        return canvas
    else:
        # 衣物比区域宽：居中裁切
        left = (new_w - tw) // 2
        return resized.crop((left, 0, left + tw, th))


class TryOnEngine(ABC):
    '''
    虚拟试衣引擎接口，所有引擎都必须实现这个接口
    '''
    @abstractmethod
    def composite(self, user_photo: Image.Image, clothing: Image.Image,
                  category: str) -> Image.Image:
        """将衣物合成到用户照片上，返回 RGBA 图片"""
        pass
