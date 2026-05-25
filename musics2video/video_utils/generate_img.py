import os
from pathlib import Path
import cssutils
import logging
import subprocess
from ..logger import get_logger, setup_logging
from ..configs import M2VConfig
from ..renderer import *
from PIL import Image

cssutils.log.setLevel(logging.CRITICAL)
BASE_DIR = Path(__file__).resolve().parent

def extract_thumbnail(audio_name: str, temp_dir: str):
    output_path = str(Path(temp_dir) / 'cover.png')
    audio_path = str(Path(temp_dir) / audio_name)
    cmd = ['ffmpeg', 
            '-i', audio_path, 
            '-an',
            '-vcodec',
            'copy', 
            output_path,
            '-y']
    result = subprocess.run(cmd, check = True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
def get_styles(config: M2VConfig) -> tuple[str, str]:
    template_path = (BASE_DIR / '..' / 'templates' / config.style / 'template.html').resolve()
    style_path = (BASE_DIR / '..' / 'templates' / config.style /  'style.css').resolve()
    style_config = config.style_config
    css_content = style_path.read_text(encoding='utf-8')
    sheet = cssutils.parseString(css_content)       
    for i in sheet:
        if i.type == i.STYLE_RULE:
            if i.selectorText == 'body' and style_config.get('bg'):
                i.style['background'] = style_config.get('bg')          
            elif i.selectorText == '.song' and style_config.get('text'):
                i.style['color'] = style_config.get('text')              
            elif i.selectorText == '.song.active' and style_config.get('text'):
                i.style['color'] = style_config.get('text')                  
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    css = sheet.cssText.decode('utf-8')
    return template_content, css
    
def song_html(titles: list[str], index: int) -> str:
    html_pieces = []
    for i, j in enumerate(titles, start = 1):
        if i == index:
            active = ' active' 
        else:
            active = '' 
        html_pieces.append(f'<div class="song{active}">{j}</div>')
    return '\n'.join(html_pieces)

def get_cover(cover: str, temp_dir: str):
    exts = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp', '.gif'}
    with Image.open(cover) as img:
        _, ext = os.path.splitext(cover)     
        if ext.lower() not in exts:
            raise ValueError('get_cover: invalid image format')     
        jpg_path = Path(temp_dir) / 'cover.png'
        if img.mode not in ('RGB'):
            img = img.convert('RGB')
        img.save(jpg_path, 'PNG')
             
def generate_img(titles: list[str], cover: str | None = None, config: M2VConfig = M2VConfig()):
    setup_logging(level = config.level, name = 'generate_img')
    logger = get_logger(__name__)
    try:
        logger.info('get cover image')
        if not config.use_yt_cover:
            get_cover(cover, config.temp_dir)
        logger.info('generating images')
        renderer = config.renderer
        template, style = get_styles(config)   
        for i in range(1, len(titles)+1):
            if config.use_yt_cover:
                extract_thumbnail(f'{i}.{config.yt_audio_format}', config.temp_dir)
            img_html = template.replace('{{SONGS}}', song_html(titles, i))            
            output_file_path = str(Path(config.temp_dir) / f'{i}.png')
            renderer(img_html, style, output_file_path)            
    except Exception as e:
        logger.error(e)
        raise RuntimeError(e)
