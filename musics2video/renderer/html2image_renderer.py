import os
from html2image import Html2Image
from PIL import Image
from pathlib import Path

def renderer(html: str, css: str, img_dir: str, resolution: tuple[int, int] = (1920, 1080)):
    output_dir = os.path.dirname(os.path.abspath(img_dir))
    output_filename = os.path.basename(img_dir)
    hti = Html2Image(temp_path=output_dir, size=(1920, 1080))
    hti.browser.flags = ['--headless',
            '--timeout=2000',
            '--no-sandbox',
            '--disable-gpu',
            '--log-level=3',
            '--disable-gpu-program-cache',
            '--no-zygote']
    hti.output_path = output_dir
    hti.screenshot(html_str=html, css_str=css, save_as=output_filename)
    if resolution != (1920, 1080):
        img = Image.open(str(Path(output_dir) / output_filename))
        resized_img = img.resize(resolution)
        img.close()
        resized_img.save(str(Path(output_dir) / output_filename))
