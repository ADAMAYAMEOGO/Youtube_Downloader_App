# main.py
import os
import threading
from kivy.lang import Builder
from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from download_manager import DownloadManager
from utils import validate_url, format_bytes
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import Screen


class YouTubeDownloaderApp(MDApp):
    def build(self):
        self.download_manager = DownloadManager()
        self.root = Builder.load_file('youtubedownloader.kv')
        return self.root

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.create_quality_menu()


    def create_quality_menu(self):
        quality_items = [{"text": "Low"}, {"text": "Medium"}, {"text": "High"}]
        self.quality_menu = MDDropdownMenu(
            caller=self.root.ids['quality_button'],
            items=quality_items,
            width_mult=4,
            #callback=self.set_quality
            callback=self.quality_callback
        )
        self.ids['quality_button'].bind(on_release=self.quality_menu.open)

    def quality_callback(self, instance):
        self.ids['quality_button'].text = instance.text
        self.quality_menu.dismiss()



    def download_video(self):
        url = self.root.ids['url_input'].text
        if validate_url(url):
            quality = self.root.ids['quality_dropdown'].selected_item["text"].lower()
            threading.Thread(target=self.download_manager.download_video, args=(url, quality, self.update_progress)).start()
        else:
            self.show_error("Invalid URL. Please enter a valid YouTube video URL.")

    def download_audio(self):
        url = self.root.ids['url_input'].text
        if validate_url(url):
            threading.Thread(target=self.download_manager.download_audio, args=(url, self.update_progress)).start()
        else:
            self.show_error("Invalid URL. Please enter a valid YouTube video URL.")

    def update_progress(self, d):
        if d['status'] == 'finished':
            file_name = os.path.basename(d['filename'])
            Clock.schedule_once(lambda dt: self.add_to_download_list(file_name), 0)

    def add_to_download_list(self, file_name):
        download_item = OneLineListItem(text=file_name)
        self.root.ids['download_list'].add_widget(download_item)

    def show_error(self, message):
        self.root.ids['url_input'].error = True
        self.root.ids['url_input'].helper_text = message


if __name__ == '__main__':
    YouTubeDownloaderApp().run()
