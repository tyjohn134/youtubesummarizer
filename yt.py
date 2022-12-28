# Extract all video_urls
import re
from pytube import YouTube, Channel

def get_video_id(url):
    # Compile the regex pattern
    pattern = re.compile(
        r'^(?:https?://)?(?:www\.)?(?:youtu\.be/|youtube\.com/(?:embed/|v/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$')

    # Search for a match in the URL
    match = pattern.search(url)

    # Extract the video ID from the match
    if match:
        video_id = match.group(1)
        return video_id
    return None


class YTDownloader:
    def __init__(self, url) -> None:
        self.url = url
        self.yt = YouTube(url) if "watch?" in url else None
        self.channel = Channel(url) if "watch?" not in url else None

    def get_channel_urls(self):
        c = self.channel
        video_urls = c.video_urls
        return video_urls

    def get_channel_titles(self):
        c = self.channel
        video_titles = [video.title for video in c.videos]
        return video_titles

    def get_title(self):
        y = self.yt
        return y.title

    def download(self):
        file_path = self.yt.streams.filter(only_audio=True)[
            0].download(filename=f"{get_video_id(self.url)}.mp4")
        return file_path

    def download_url(self, url):
        file_path = YouTube(url).streams.filter(only_audio=True)[
            0].download(filename=f"{get_video_id(url)}.mp4")
        return file_path
