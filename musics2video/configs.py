import os
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable
from pathlib import Path
import shutil
from .renderer import *

BASE_DIR = Path(__file__).resolve().parent

@dataclass
class M2VConfig:
    """
    Configuration class for the Musics2Video generation pipeline.

    This dataclass holds all the technical, environmental, and stylistic
    settings required to download audio files, render templates, and merge
    the final output video.

    Attributes:
        temp_dir (str): Path to the temporary directory for intermediate assets.
        temp_cover (str): Subdirectory name within temp_dir to store cover images.
        level (str): Logging level (e.g., 'INFO', 'DEBUG', 'WARNING').
        yt_audio_format (str): Target audio format for yt-dlp downloading and processing (e.g., 'opus').
        audio_quality (int): Quality setting for the audio download extraction (0 is highest quality, 9 is lowest).
        style (str): Name of the built-in visual style template (e.g., 'classic', 'modern').
        renderer (Callable): Renderer function used to convert HTML/CSS to image.
        use_yt_cover (bool): Whether to pull and use thumbnails from YouTube videos.
        output_dir (str): Target path where the final video will be saved.
        video_format (str): File extension/format for output videos (e.g., 'mp4').
        resolution (tuple[int, int]): Dimensions of the output video (width, height).
        fps (int): Frames per second configuration for the output video.
        custom_template (str | None): path to a local custom HTML and CSS template directory.
        shorten_title (bool): If True, truncates song titles to keep the layout tidy.
    """
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
    fps: int = 30
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
