import os
import shutil
from .video_utils.get_data import get_data
from .video_utils.download import download_musics
from .video_utils.merge import merge
from .video_utils.generate_img import generate_img
from .logger import get_logger, setup_logging
from .configs import M2VConfig

class M2V:
    """
    The main orchestration class for the Musics2Video generation pipeline.

    This class provides high-level methods to build a combined video playlist
    either directly from a list of URLs or from a formatted local batch file.
    """
    def __init__(self, config: M2VConfig = M2VConfig()):
        self.config = config
        setup_logging(level=config.level)
        self.logger = get_logger(__name__)

    def generate_from_download(self, urls: list, output_name: str):
        """
        Downloads audio tracks from URLs, renders tracklist images, and merges them into a video.

        It processes everything inside a temporary directory and ensures that
        the directory is cleaned up afterward, even if errors occur during execution.

        Args:
            urls (list): A list of online music or video URLs to process.
            output_name (str): The filename for the final output video.
        """
        logger = self.logger
        try:
            logger.info('start "generate_from_download"')
            titles = download_musics(urls, config = self.config)
            generate_img(titles, config = self.config)
            merge(len(titles), video_name=output_name, config=self.config)
            logger.info('program "generate_from_download" ended successfully')
        except Exception as e:
            raise RuntimeError(e) from e
        finally:
            if os.path.isdir(self.config.temp_dir):
                shutil.rmtree(self.config.temp_dir)

    def generate_from_list(self, list_path: str, output_name: str):
        """
        Processes a mixed list file (local/download), generates frame images, and merges them into a video.

        Like the download counterpart, it manages internal assets within a
        temporary space and handles automatic workspace cleanup upon completion or failure.

        Args:
            list_path (str): The path to the text file specifying tracks and configurations.
            output_name (str): The filename for the final output video.
        """
        logger = self.logger
        try:
            logger.info('start "generate_from_list"')
            titles = get_data(list_path, config=self.config)
            generate_img(titles, config=self.config)
            merge(len(titles), video_name=output_name, config=self.config)
            logger.info('program "generate_from_list" ended successfully')
        except Exception as e:
            raise RuntimeError(e) from e
        finally:
            if os.path.isdir(self.config.temp_dir):
                shutil.rmtree(self.config.temp_dir)
