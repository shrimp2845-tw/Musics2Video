import os
from pathlib import Path
import shutil
from ..logger import get_logger, setup_logging
from ..configs import M2VConfig

BASE_DIR = Path(__file__).resolve().parent

def get_styles(config: M2VConfig) -> tuple[str, str]:
    """
    Reads and returns the HTML template and CSS stylesheet data.

    Args:
        config (M2VConfig): Pipeline structural configurations object.

    Returns:
        tuple[str, str]: HTML content text and CSS context style contents.
    """
    if config.custom_template:
        template_path = str(Path(config.custom_template) / 'template.html')
        style_path = str(Path(config.custom_template) / 'style.css')
    else:
        template_path = str((BASE_DIR / '..' / 'templates' / config.style / 'template.html').resolve())
        style_path = str((BASE_DIR / '..' / 'templates' / config.style /  'style.css').resolve())
    with open(style_path, 'r', encoding='utf-8') as f:
        css_content = f.read()
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    return template_content, css_content

def song_html(titles: list[str], index: int) -> str:
    """
    Assembles track listings into raw HTML structure with one active highlight class.

    Args:
        titles (list[str]): Track labels compilation list.
        index (int): Loop step positional threshold indicating which song is currently active.

    Returns:
        str: Finished structural block component of item collections.
    """
    html_pieces = []
    for i, j in enumerate(titles, start = 1):
        if i == index:
            active = ' active'
        else:
            active = ''
        html_pieces.append(f'<div class="song{active}">{j}</div>')
    return '\n'.join(html_pieces)

def generate_img(titles: list[str], config: M2VConfig = M2VConfig()):
    """
    Converts the processed title blocks sequence iteratively into rendered frame image elements.

    Args:
        titles (list[str]): Total list containing localized item title names.
        config (M2VConfig): Execution context values setup instance object.
    """
    setup_logging(level = config.level)
    logger = get_logger(__name__)
    try:
        logger.info('generating images')
        renderer = config.renderer
        template, style = get_styles(config)
        for i in range(1, len(titles)+1):
            if os.path.exists(str(Path(config.temp_dir) / config.temp_cover / f'{i}.png')):
                shutil.copy(str(Path(config.temp_dir) / config.temp_cover / f'{i}.png'), str(Path(config.temp_dir) / 'cover.png'))
            else:
                shutil.copy(str(Path(config.temp_dir) / config.temp_cover / 'default_cover.png'), str(Path(config.temp_dir) / 'cover.png'))
            img_html = template.replace('{{SONGS}}', song_html(titles, i))
            output_file_path = str(Path(config.temp_dir) / f'{i}.png')
            renderer(img_html, style, output_file_path, config.resolution)
    except Exception as e:
        logger.error(e)
        raise RuntimeError(e) from e
