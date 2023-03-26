# download_manager.py
import os
from pydub import AudioSegment
from youtube_dl import YoutubeDL
from settings import DEFAULT_DOWNLOAD_PATH, VIDEO_QUALITY_OPTIONS, AUDIO_FORMAT
from utils import create_download_folder


class DownloadManager:
    def __init__(self):
        self.downloads = []

    def download_video(self, url, quality, on_progress_callback):
        create_download_folder()
        ydl_opts = {
            'format': VIDEO_QUALITY_OPTIONS[quality],
            'outtmpl': os.path.join(DEFAULT_DOWNLOAD_PATH, '%(title)s.%(ext)s'),
            'progress_hooks': [on_progress_callback],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    def download_audio(self, url, on_progress_callback):
        create_download_folder()
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DEFAULT_DOWNLOAD_PATH, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': AUDIO_FORMAT,
                'preferredquality': '192',
            }],
            'progress_hooks': [on_progress_callback],
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
