import os
from pathlib import Path
from tqdm import tqdm
from PIL import Image
from .download import download_one
from .get_local import get_local
from ..logger import get_logger, setup_logging
from ..configs import M2VConfig

def get_cover(cover: str, temp_dir: str, temp_cover: str, name: str = 'default_cover.png'):
    """
    Validates, converts, and saves a custom cover file into standard RGB PNG format.

    Args:
        cover (str): Source local image filepath string.
        temp_dir (str): Base temporary execution workspace folder string.
        temp_cover (str): Cover images container folder name context.
        name (str): Outbound image target base file name allocation parameter.
    """
    exts = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.gif'}
    with Image.open(cover) as img:
        ext = os.path.splitext(cover)[-1]
        if ext.lower() not in exts:
            raise ValueError('get_cover: invalid image format')
        png_path = Path(temp_dir) / temp_cover / name
        if img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(png_path, 'PNG')

def read_audio_list(name: str) -> list[list[str | None]]:
    """
    Parses text file instructions separating sources, file locations, and individual covers.

    Args:
        name (str): Target text record compilation mapping structure path.

    Returns:
        list[list[str | None]]: Sub-arrays grouping extraction directives parsed into items rows.
    """
    audio_list = []
    with open(name, 'r', encoding='utf-8') as f:
        for i in f:
            parts = list(i.strip().split('{{NEXT}}'))
            if not parts:
                continue
            if parts[0].lower() not in ('local', 'download'):
                raise ValueError(f'read_audio_list: Invalid line format {i.strip()}')
            if len(parts) == 2:
                parts.append(None)
                audio_list.append(parts)
            elif len(parts) == 3:
                audio_list.append(parts)
            else:
                raise ValueError(f'read_audio_list: Invalid line format {i.strip()}')
    return audio_list

def get_data(list_path: str, default_cover: str | None = None, config: M2VConfig | None = None):
    """
    Iteratively updates, imports, downloads, and maps raw track listing configurations data.

    Args:
        list_path (str): Filepath linking index lists.
        default_cover (str | None): Custom backup artwork image location path if available.
        config (M2VConfig): Context environment system choices settings wrapper object.

    Returns:
        list[str]: Compiled array container tracking finalized display names indexes entries.
    """
    if config is None:
        config = M2VConfig()
    setup_logging(level = config.level)
    logger = get_logger(__name__)
    try:
        if default_cover:
            logger.debug('getting default cover')
            get_cover(default_cover, config.temp_dir, config.temp_cover)
        logger.info('start download & get local audio files')
        que = read_audio_list(list_path)
        if config.level not in ('WARNING', 'ERROR', 'CRITICAL'):
            que = tqdm(que)
        titles = []
        for i, j in enumerate(que, start = 1):
            method, url_or_path, cover = j
            if method == 'download':
                titles.append(download_one(url_or_path, str(i), config = config))
            elif method == 'local':
                titles.append(get_local(url_or_path, str(i), config = config))
            else:
                raise ValueError('get_audio: invalid method')
            if cover:
                get_cover(cover, config.temp_dir, config.temp_cover, name = f'{str(i)}.png')
        return titles
    except Exception as e:
        logger.error(e)
        raise RuntimeError(e) from e
