import os
from html2image import Html2Image

def renderer(html: str, css: str, img_dir: str):
    output_dir = os.path.dirname(os.path.abspath(img_dir))
    output_filename = os.path.basename(img_dir)
    hti = Html2Image(temp_path=output_dir, size=(1920, 1080))
    hti.browser.flags = ['--headless',
            '--no-sandbox',
            '--disable-gpu',
            '--log-level=4',
            '--disable-gpu-program-cache']
    hti.output_path = output_dir
    hti.screenshot(html_str=html, css_str=css, save_as=output_filename)
