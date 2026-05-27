from pathlib import Path
from pydub import AudioSegment
from .get_title import sanitize
from ..configs import M2VConfig

def get_local(original_path: str, name: str, config: M2VConfig = M2VConfig()) -> str:
    """
    Processes a local file path, formats audio track file extensions, and extracts title metadata.

    Args:
        original_path (str): Path pointing directly to local storage source elements.
        name (str): Assigned numeric identifier or target save identity string context.
        config (M2VConfig): System values and criteria requirements control container object.

    Returns:
        str: Cleansed string mapping tracking extracted display titles labels values.
    """
    title = str(Path(original_path).stem).strip()
    output_path = str(Path(config.temp_dir) / f'{name}.{config.yt_audio_format}')
    audio = AudioSegment.from_file(original_path)
    audio.export(output_path, format=config.yt_audio_format)
    if config.shorten_title:
        return sanitize(title)
    return title
