import os
from tqdm import tqdm
import subprocess
from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError
from ..logger import get_logger, setup_logging
from ..color import red
from ..configs import M2VConfig

def __sanitize(name: str) -> str:
    if len(name) < 50:
        return name
    return name[:47] + '......'
    
def __get_title(url: str) -> str:
    ydl_opts = {'quiet': True,
            'skip_download': True,
            'no_warnings': True}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download = False)
    return __sanitize(info.get('title'))
    
def __download_one(url: str, name: str, config: M2VConfig = M2VConfig()) -> str:
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
    return __get_title(url)

def download_musics(urls: list[str], config: M2VConfig = M2VConfig()) -> list[tuple[str, str]]:
    """
    download all musics and return a list[tuple[file_name, music name]]
    """
    global LOGGER
    level = config.level
    setup_logging(level = level, name = 'download')
    LOGGER = get_logger(__name__)   
    LOGGER.info('start downloading audios')
    if level not in ('WARNING', 'ERROR', 'CRITICAL'):
        que = tqdm(urls)
    else:
        que = urls
    titles = []    
    for i, j in enumerate(que, start = 1):
        titles.append((str(i)+'.mp3', __download_one(j, str(i)+'.mp3', config)))
    return titles
