from typing import List, Optional
from pathlib import Path
import typer
from .configs import M2VConfig
from .m2v import M2V

app = typer.Typer(help="Musics2Video - A Python cli tool for generating your own music playlist video", add_completion=False)

def build_config(level: str,
        yt_audio_format: str,
        audio_quality: int,
        style: str,
        use_yt_cover: bool,
        output_dir: str,
        video_format: str,
        width: int,
        height: int,
        fps: int,
        custom_template: Optional[Path],
        shorten_title: bool,
        temp_dir: Optional[str] = None) -> M2VConfig:
    """Helper function to build an M2VConfig instance from CLI arguments."""
    resolution = (width, height)
    custom_template_str = str(custom_template) if custom_template else None
    config_kwargs = {'level': level,
            'yt_audio_format': yt_audio_format,
            'audio_quality': audio_quality,
            'style': style,
            'use_yt_cover': use_yt_cover,
            'output_dir': output_dir,
            'video_format': video_format,
            'resolution': resolution,
            'fps': fps,
            'custom_template': custom_template_str,
            'shorten_title': shorten_title}
    if temp_dir:
        config_kwargs['temp_dir'] = temp_dir
    return M2VConfig(**config_kwargs)

ConfigOptions = {
    'level': typer.Option('INFO', '--level', '-l', help='Global logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).'),
    'yt_audio_format': typer.Option('opus', '--audio-fmt', help='Target audio format for downloading and internal processing.'),
    'audio_quality': typer.Option(0, '--audio-q', help='Audio extraction quality setting (0 is highest, 9 is lowest).'),
    'style': typer.Option('classic', '--style', '-s', help='Built-in visual style template name (classic, modern).'),
    'use_yt_cover': typer.Option(True, '--yt-cover/--no-yt-cover', help='Whether to fetch and use thumbnails from YouTube videos (or other video platform provided fetchable thumbnail).'),
    'output_dir': typer.Option('./', '--out-dir', '-o', help='Target output directory path for the final video.'),
    'video_format': typer.Option('mp4', '--video-fmt', help='Output video file container format extension.'),
    'width': typer.Option(1920, '--width', help='Output video resolution width in pixels.'),
    'height': typer.Option(1080, '--height', help='Output video resolution height in pixels.'),
    'fps': typer.Option(10, '--fps', help='Frames per second configuration for the final video.'),
    'custom_template': typer.Option(None, '--custom-tmpl', help='Path to a local custom HTML/CSS template folder.'),
    'shorten_title': typer.Option(True, '--shorten/--no-shorten', help='Truncate long track titles to preserve layout integrity.'),
    'temp_dir': typer.Option(None, '--temp-dir', help='Path for intermediate assets (auto-generated if omitted).')}


@app.command(name='download')
def generate_from_download(
        urls: List[str] = typer.Argument(..., help='One or more online music/video URLs to process.'),
        output_name: str = typer.Option('output.mp4', '--name', '-n'),
        level: str = ConfigOptions['level'],
        yt_audio_format: str = ConfigOptions['yt_audio_format'],
        audio_quality: int = ConfigOptions['audio_quality'],
        style: str = ConfigOptions['style'],
        use_yt_cover: bool = ConfigOptions['use_yt_cover'],
        output_dir: str = ConfigOptions['output_dir'],
        video_format: str = ConfigOptions['video_format'],
        width: int = ConfigOptions['width'],
        height: int = ConfigOptions['height'],
        fps: int = ConfigOptions['fps'],
        custom_template: Optional[Path] = ConfigOptions['custom_template'],
        shorten_title: bool = ConfigOptions['shorten_title'],
        temp_dir: Optional[str] = ConfigOptions['temp_dir']):
    """
    Download audio tracks from online URLs, render layout frames, and compile into a video.
    """
    config = build_config(level, yt_audio_format, audio_quality, style, use_yt_cover, output_dir, video_format, width, height, fps, custom_template, shorten_title, temp_dir)
    processor = M2V(config=config)
    processor.generate_from_download(urls=urls, output_name=output_name)


@app.command(name='list')
def generate_from_list(list_path: Path = typer.Argument(..., help='Path to the formatted local text file specifying batch tracks.'),
        output_name: str = typer.Option('output.mp4', '--name', '-n'),
        level: str = ConfigOptions['level'],
        yt_audio_format: str = ConfigOptions['yt_audio_format'],
        audio_quality: int = ConfigOptions['audio_quality'],
        style: str = ConfigOptions['style'],
        use_yt_cover: bool = ConfigOptions['use_yt_cover'],
        output_dir: str = ConfigOptions['output_dir'],
        video_format: str = ConfigOptions['video_format'],
        width: int = ConfigOptions['width'],
        height: int = ConfigOptions['height'],
        fps: int = ConfigOptions['fps'],
        custom_template: Optional[Path] = ConfigOptions['custom_template'],
        shorten_title: bool = ConfigOptions['shorten_title'],
        temp_dir: Optional[str] = ConfigOptions['temp_dir']):
    """
    Process a mixed batch list file (local files/downloads) to generate layouts and merge into a video.
    """
    config = build_config(level, yt_audio_format, audio_quality, style, use_yt_cover, output_dir, video_format, width, height, fps, custom_template, shorten_title, temp_dir)
    processor = M2V(config=config)
    processor.generate_from_list(list_path=str(list_path), output_name=output_name)

if __name__ == '__main__':
    app()
