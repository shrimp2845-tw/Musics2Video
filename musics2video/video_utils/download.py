from tqdm import tqdm
from pathlib import Path
import subprocess
from ..logger import get_logger, setup_logging
from ..configs import M2VConfig
from .get_title import get_title

def download_one(url: str, name: str, config: M2VConfig = M2VConfig()) -> str:
    title = get_title(url, config = config)
    cmd = ['yt-dlp',
            '-x',
            '--audio-format', config.yt_audio_format,
            '--audio-quality', str(config.audio_quality),
            '-o', Path(config.temp_dir) / f'{name}.{config.yt_audio_format}',
            url]
    if config.use_yt_cover:
        cmd.insert(2, '--embed-thumbnail')
    subprocess.run(cmd, check = True, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    return title

def download_musics(urls: list[str], config: M2VConfig = M2VConfig()) -> list[str]:
    """
    download all musics and return a list[music name]
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
            titles.append(download_one(j, str(i), config))
        return titles
    except Exception as e:
        logger.error(e)
        raise RuntimeError(e)
