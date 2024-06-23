import os
import json
from pytube import YouTube, Playlist
from tqdm import tqdm
from pytube.request import Request

# Load cookies from the JSON file
def load_cookies(filepath):
    with open(filepath, 'r') as file:
        cookies = json.load(file)
    return cookies

def download_video(url, cookies, output_path='downloads'):
    yt = YouTube(url, request=Request(cookies=cookies))
    stream = yt.streams.get_highest_resolution()
    print(f"Downloading: {yt.title}")
    stream.download(output_path)
    print(f"Downloaded: {yt.title}")

def download_audio(url, cookies, output_path='downloads'):
    yt = YouTube(url, request=Request(cookies=cookies))
    stream = yt.streams.filter(only_audio=True).first()
    print(f"Downloading: {yt.title}")
    out_file = stream.download(output_path)
    
    # Convert to MP3
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(f"Downloaded and converted: {yt.title}")

def download_playlist(url, cookies, format='video', output_path='downloads'):
    pl = Playlist(url)
    print(f'Downloading playlist: {pl.title}')
    
    for video in tqdm(pl.videos, desc='Downloading videos', unit='video'):
        if format == 'audio':
            stream = video.streams.filter(only_audio=True).first()
            out_file = stream.download(output_path)
            
            # Convert to MP3
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            print(f"Downloaded and converted: {video.title}")
        else:
            stream = video.streams.get_highest_resolution()
            stream.download(output_path)
            print(f"Downloaded: {video.title}")

def main():
    welcome_message = """
    *************************************
    *                                   *
    *     Welcome to YouTube Downloader *
    *                                   *
    *************************************
    """
    print(welcome_message)
    
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    cookies = load_cookies('cookies.json')

    print("1. Download a video")
    print("2. Download audio")
    print("3. Download a playlist")
    choice = input("Enter your choice: ")

    url = input("Enter the URL: ")

    if choice == '1':
        download_video(url, cookies)
    elif choice == '2':
        download_audio(url, cookies)
    elif choice == '3':
        format_choice = input("Download as video or audio (mp3)? (video/audio): ").strip().lower()
        if format_choice in ['video', 'audio']:
            download_playlist(url, cookies, format=format_choice)
​⬤