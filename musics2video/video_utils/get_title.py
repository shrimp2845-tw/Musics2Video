from urllib.parse import urlparse, parse_qs
from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL
from ..logger import get_logger, setup_logging
from ..configs import M2VConfig

class __NoLogger:
    def debug(self, *args, **kwargs):
        pass

    def warning(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass

def sanitize(name: str) -> str:
    if len(name) < 45:
        return name
    return name[:40] + '......'
    
def get_all_name(url: str) -> str:
    ydl_opts = {'quiet': True,
            'skip_download': True,
            'no_warnings': True, 
            'logger': __NoLogger}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download = False)
    return info.get('title')
    
def get_yt_name(url: str) -> str | None:
    url = url.strip()
    ytm = YTMusic()
    video_id = None
    parsed_url = urlparse(url)
    if 'youtube.com' in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if 'v' in query_params:
             video_id = query_params['v'][0]
    elif 'youtu.be' in parsed_url.netloc:
        video_id = parsed_url.path.strip('/')
    if not video_id or len(video_id) != 11:
        return None
    track_info = ytm.get_song(video_id)
    video_details = track_info.get('videoDetails', {})       
    song_title = video_details.get('title')
    artist = video_details.get('author')
    if artist and song_title:
        return f'{song_title} - {artist}'
    return None
    
def get_title(url: str, config: M2VConfig = M2VConfig()) -> str:
    setup_logging(level = config.level, name = 'get_title')
    logger = get_logger(__name__)
    try:
        name = get_yt_name(url)
        if not name:
            name = get_all_name(url)
        return sanitize(name)
    except Exception as e:
        logger.error(e)
        raise RuntimeError(e)
