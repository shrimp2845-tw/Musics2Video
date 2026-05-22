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
            '--quiet',
            '--no-progress',
            '--no-warnings',
            '--extract-audio',
            '--audio-format', 'mp3',
            '--audio-quality', str(config.audio_quality),
            '-o', config.temp_dir + name,
            url]
    subprocess.run(cmd, check = True)
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
            titles.append((str(i)+'.mp3', download_one(j, str(i)+'.mp3', config)))
        return titles
    except Exception as e:
        logger.error(e)
        sys.exit(1)
