import os
from pathlib import Path
from ..configs import M2VConfig
from .get_title import sanitize
import subprocess
from pydub import AudioSegment

def get_local(original_path: str, name: str, config: M2VConfig = M2VConfig()) -> str:
    title = str(Path(original_path).stem).strip()
    output_path = str(Path(config.temp_dir) / f'{name}.{config.yt_audio_format}')
    audio = AudioSegment.from_file(original_path)
    audio.export(output_path, format=config.yt_audio_format)
    if config.shorten_title:
        return sanitize(title)
    return title
