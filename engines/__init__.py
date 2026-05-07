from engines.base import TryOnEngine
from engines.simple import SimpleEngine
from engines.mediapipe import MediaPipeEngine


def get_engine(engine_name):
    """根据配置名返回对应的引擎实例"""
    engines = {
        'simple': SimpleEngine(),
        'mediapipe': MediaPipeEngine(),
    }
    return engines.get(engine_name, MediaPipeEngine())
