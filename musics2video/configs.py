import os
from dataclasses import dataclass, field
from datetime import datetime
from .renderer import *
from typing import Callable

@dataclass
class M2VConfig:
    temp_dir: str = f'./{datetime.now().strftime("%Y%m%d_%H%M%S_%f")}_temp/'
    level: str = 'INFO'
    yt_audio_format: str = 'm4a'
    audio_quality: int = 0
    style: str = 'classic'
    style_config: dict = field(default_factory=dict)
    renderer:  Callable[[str, str, str], None] = html2image_renderer
    use_yt_cover: bool = False
    output_dir: str = './'
    video_format: str = 'mp4'
    def __post_init__(self):
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)


