from urllib.parse import urlparse, parse_qs
from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL
from ..configs import M2VConfig

class __NoLogger:
    """Internal null-logger to silence output generated"""
    def debug(self, *args, **kwargs):
        pass

    def warning(self, *args, **kwargs):
        pass

    def error(self, *args, **kwargs):
        pass

def sanitize(name: str) -> str:
    """Truncates titles exceeding length limits and appends dots to avoid visual layout overflow.

    Args:
        name (str): Input unformatted label title context.

    Returns:
        str: Output transformed safe title content.
    """
    if len(name) < 25:
        return name
    return name[:23] + '......'

def get_all_name(url: str) -> str:
    """
    Extracts base standard video titles via generic yt-dlp backend info exploration queries.

    Args:
        url (str): Absolute network path web link identifier resource locator string.

    Returns:
        str: Cleaned string identifying retrieved network title string context mapping.
    """
    ydl_opts = {'quiet': True,
            'skip_download': True,
            'no_warnings': True,
            'logger': __NoLogger}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download = False)
    return info.get('title')

def get_yt_name(url: str) -> str | None:
    """
    Extracts pure metadata titles targeting YouTube parameters directly using ytmusicapi.

    Args:
        url (str): Raw tracking web page query index context connection path.

    Returns:
        str | None: String metadata if matched effectively, otherwise returns None.
    """
    url = url.strip()
    ytm = YTMusic()
    video_id = None
    parsed_url = urlparse(url)
    hostname = (parsed_url.hostname or '').lower()
    if hostname == 'youtube.com' or hostname.endswith('.youtube.com'):
        query_params = parse_qs(parsed_url.query)
        if 'v' in query_params:
            video_id = query_params['v'][0]
    elif hostname == 'youtu.be':
        video_id = parsed_url.path.strip('/')
    if not video_id or len(video_id) != 11:
        return None
    track_info = ytm.get_song(video_id)
    video_details = track_info.get('videoDetails', {})
    song_title = video_details.get('title')
    if song_title:
        return song_title
    return None

def get_title(url: str, config: M2VConfig | None = None) -> str:
    """
    Orchestrates metadata collection from multi-service endpoints.

    Args:
        url (str): Live target audio host tracking address resource link.
        config (M2VConfig): Context configuration controls setup block framework variables.

    Returns:
        str: Finalized target sanitized track header indicator string.
    """
    if config is None:
        config = M2VConfig()
    name = get_yt_name(url)
    if not name:
        name = get_all_name(url)
    name = name.strip()
    if config.shorten_title:
        return sanitize(name)
    return name
