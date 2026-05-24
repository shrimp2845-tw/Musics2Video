import os
import sys
from tqdm import tqdm
import subprocess
from ..logger import get_logger, setup_logging
from ..configs import M2VConfig
from .get_title import get_title

def download_one(url: str, name: str, config: M2VConfig = M2VConfig()) -> str:
    title = get_title(url, config = config)
    cmd = ['yt-dlp',
            '-x',
            '--audio-format', config.yt_audio_format,
            "--audio-quality", str(config.audio_quality),
            '-o', f'{config.temp_dir}{name}.{config.yt_audio_format}',
            url]
    subprocess.run(cmd, check = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return title

def download_musics(urls: list[str], config: M2VConfig = M2VConfig()) -> list[tuple[str, str]]:
    """
    download all musics and return a list[tuple[file_name, music name]]
    """
    setup_logging(level = config.level, name = 'download')
    logger = get_logger(__name__)
    try:
        logger.info('start downloading audios')
        if config.level not in ('WARNING', 'ERROR', 'CRITICAL'):
            que = tqdm(urls)
        else:
            que = urls
        titles = []    
        for i, j in enumerate(que, start = 1):
            titles.append((f'{i}.{config.yt_audio_format}', download_one(j, str(i), config)))
        return titles
    except Exception as e:
        logger.error(e)
        raise RuntimeError(e)
