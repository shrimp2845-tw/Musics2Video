import os
from dataclasses import dataclass, field
from datetime import datetime
from .renderer import *
from typing import Callable
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).resolve().parent

@dataclass
class M2VConfig:
    temp_dir: str = f'./{datetime.now().strftime("%Y%m%d_%H%M%S_%f")}_temp/'
    temp_cover: str = 'temp_cover'
    level: str = 'INFO'
    yt_audio_format: str = 'opus'
    audio_quality: int = 0
    style: str = 'classic'
    renderer:  Callable[[str, str, str, tuple[int, int]], None] = html2image_renderer
    use_yt_cover: bool = False
    output_dir: str = './'
    video_format: str = 'mp4'
    resolution: tuple[int, int] = (1920, 1080)
    fps: int = 10
    custom_template: str | None = None
    shorten_title: bool = True
    def __post_init__(self):
        if Path(self.temp_dir).resolve() == Path.cwd().resolve() or Path(self.temp_dir).resolve() in Path.cwd().resolve().parents:
            raise ValueError('invalid temp_dir')
        if (Path(self.temp_dir) / self.temp_cover).resolve() == Path(self.temp_dir).resolve() or (Path(self.temp_dir) / self.temp_cover).resolve() in Path(self.temp_dir).resolve().parents:
            raise ValueError('invalid temp_cover')
        if not os.path.exists(self.temp_dir):
            os.mkdir(self.temp_dir)
        if not os.path.exists(str(Path(self.temp_dir) / self.temp_cover)):
            os.mkdir(str(Path(self.temp_dir) / self.temp_cover))
        if not os.path.exists(str(Path(self.temp_dir) / self.temp_cover / 'default_cover.png')):
            shutil.copy(str(Path(BASE_DIR / 'templates' / 'default_cover.png')), str(Path(self.temp_dir) / self.temp_cover / 'default_cover.png'))
        if self.custom_template:
            self.custom_template = str(Path(self.custom_template).resolve())
        


