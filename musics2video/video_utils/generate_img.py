import os
from pathlib import Path
from ..logger import get_logger, setup_logging
from ..configs import M2VConfig
from PIL import Image
import shutil

BASE_DIR = Path(__file__).resolve().parent

def get_styles(config: M2VConfig) -> tuple[str, str]:
    if config.custom_template:
        template_path = str(Path(config.custom_template) / 'template.html')
        style_path = str(Path(config.custom_template) / 'style.css')
    else:
        template_path = str((BASE_DIR / '..' / 'templates' / config.style / 'template.html').resolve())
        style_path = str((BASE_DIR / '..' / 'templates' / config.style /  'style.css').resolve())
    with open(style_path, 'r') as f:
        css_content = f.read()
    with open(template_path, 'r') as f:
        template_content = f.read()
    return template_content, css_content
    
def song_html(titles: list[str], index: int) -> str:
    html_pieces = []
    for i, j in enumerate(titles, start = 1):
        if i == index:
            active = ' active' 
        else:
            active = '' 
        html_pieces.append(f'<div class="song{active}">{j}</div>')
    return '\n'.join(html_pieces)

def get_cover(cover: str, temp_dir: str, temp_cover: str):
    exts = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.gif'}
    with Image.open(cover) as img:
        _, ext = os.path.splitext(cover)     
        if ext.lower() not in exts:
            raise ValueError('get_cover: invalid image format')     
        png_path = Path(temp_dir) / temp_cover / 'default_cover.png'
        if img.mode not in ('RGB'):
            img = img.convert('RGB')
        img.save(png_path, 'PNG')
             
def generate_img(titles: list[str], cover: str | None = None, config: M2VConfig = M2VConfig()):
    setup_logging(level = config.level)
    logger = get_logger(__name__)
    try:
        logger.info('get cover image')
        if cover:
            get_cover(cover, config.temp_dir, config.temp_cover)
        logger.info('generating images')
        renderer = config.renderer
        template, style = get_styles(config)
        for i in range(1, len(titles)+1):
            if os.path.exists(str(Path(config.temp_dir) / config.temp_cover / f'{i}.png')):
                shutil.copy(str(Path(config.temp_dir) / config.temp_cover / f'{i}.png'), str(Path(config.temp_dir) / 'cover.png'))
            else:
                shutil.copy(str(Path(config.temp_dir) / config.temp_cover / f'default_cover.png'), str(Path(config.temp_dir) / 'cover.png'))            
            img_html = template.replace('{{SONGS}}', song_html(titles, i))
            output_file_path = str(Path(config.temp_dir) / f'{i}.png')
            renderer(img_html, style, output_file_path, config.resolution)            
    except Exception as e:
        logger.error(e)
        raise RuntimeError(e)
