import os
from pytube import YouTube, Playlist
from tqdm import tqdm

def download_video(url, output_path='downloads'):
    yt = YouTube(url)
    stream = yt.streams.get_highest_resolution()
    print(f"Downloading: {yt.title}")
    stream.download(output_path)
    print(f"Downloaded: {yt.title}")

def download_audio(url, output_path='downloads'):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    print(f"Downloading: {yt.title}")
    out_file = stream.download(output_path)
    
    # Convert to MP3
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print(f"Downloaded and converted: {yt.title}")

def download_playlist(url, format='video', output_path='downloads'):
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

    print("1. Download a video")
    print("2. Download audio")
    print("3. Download a playlist")
    choice = input("Enter your choice: ")

    url = input("Enter the URL: ")

    if choice == '1':
        download_video(url)
    elif choice == '2':
        download_audio(url)
    elif choice == '3':
        format_choice = input("Download as video or audio (mp3)? (video/audio): ").strip().lower()
        if format_choice in ['video', 'audio']:
            download_playlist(url, format=format_choice)
        else:
            print("Invalid format choice!")
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
