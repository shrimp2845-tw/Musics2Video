import subprocess
from pathlib import Path
from tqdm import tqdm
from ..logger import get_logger, setup_logging
from ..configs import M2VConfig

def merge(songs_length: int, video_name: str, config: M2VConfig = M2VConfig()):
    """
    Combines rendered templates images and audios into segmented files, then concats into final video.

    Args:
        songs_length (int): Total count volume of tracked media files rows.
        video_name (str): Target output video filename string context.
        config (M2VConfig): Configuration controls block setup criteria parameters wrapper.
    """
    setup_logging(level = config.level)
    logger = get_logger(__name__)
    try:
        output_path = str(Path(config.output_dir) / video_name)
        file_list = str(Path(config.temp_dir) / 'videos.txt')
        videos = []
        logger.info('combining images and audios')
        iter = range(1, songs_length+1)
        if config.level not in ('WARNING', 'ERROR', 'CRITICAL'):
            iter = tqdm(iter)
        for i in iter:
            video_path = str((Path(config.temp_dir) / f'{i}.{config.video_format}').resolve())
            audio_path = str(Path(config.temp_dir) / f'{i}.{config.yt_audio_format}')
            img_path = str(Path(config.temp_dir) / f'{i}.png')
            cmd = ['ffmpeg',
                    '-loop', '1',
                    '-r', '1',
                    '-i', img_path,
                    '-i', audio_path,
                    '-c:v', 'libx264',
                    '-tune', 'stillimage',
                    '-crf', '30',
                    '-c:a', 'copy',
                    '-pix_fmt', 'yuv420p',
                    '-r', str(config.fps),
                    '-shortest',
                    '-y',
                    video_path]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            videos.append(video_path)
        with open(file_list, 'w') as f:
            for i in videos:
                f.write(f"file '{i}'\n")
        logger.info('merging videos')
        cmd = ['ffmpeg',
                '-f', 'concat',
                '-safe', '0',
                '-i', file_list,
                '-c', 'copy',
                '-y',
                output_path]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        logger.error(e)
        raise RuntimeError(e) from e
