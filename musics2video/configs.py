from dataclasses import dataclass
from datetime import datetime

@dataclass
class M2VConfig:
    temp_dir: str = f'./{datetime.now().strftime("%Y%m%d_%H%M%S_%f")}_temp/'
    level: str = 'INFO'
    yt_audio_format: str = 'opus'
    audio_quality: int = 0
