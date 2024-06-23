import pytube
from pytube.exceptions import AgeRestrictedError
from tqdm import tqdm
import os

# Mensaje de bienvenida con arte ASCII
def print_welcome_message():
    welcome_message = r"""
     ███▄ ▄███▓ ▄▄▄       ██▀███  ▓██   ██▓ ██▓ ▒█████   ▒█████   ▒█████  ▒██   ██▒
    ▓██▒▀█▀ ██▒▒████▄    ▓██ ▒ ██▒ ▒██  ██▒▓██▒▒██▒  ██▒▒██▒  ██▒▒██▒  ██▒▒▒ █ █ ▒░
    ▓██    ▓██░▒██  ▀█▄  ▓██ ░▄█ ▒  ▒██ ██░▒██▒▒██░  ██▒▒██░  ██▒▒██░  ██▒░░  █   ░
    ▒██    ▒██ ░██▄▄▄▄██ ▒██▀▀█▄    ░ ▐██▓░░██░▒██   ██░▒██   ██░▒██   ██░ ░ █ █ ▒ 
    ▒██▒   ░██▒ ▓█   ▓██▒░██▓ ▒██▒  ░ ██▒▓░░██░░ ████▓▒░░ ████▓▒░░ ████▓▒░▒██▒ ▒██▒
    ░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░   ██▒▒▒ ░▓  ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▒░▒░ ▒▒ ░ ░▓ ░
    ░  ░      ░  ▒   ▒▒ ░  ░▒ ░ ▒░ ▓██ ░▒░  ▒ ░  ░ ▒ ▒░   ░ ▒ ▒░   ░ ▒ ▒░ ░░   ░▒ ░
    ░      ░     ░   ▒     ░░   ░  ▒ ▒ ░░   ▒ ░░ ░ ░ ▒  ░ ░ ░ ▒  ░ ░ ░ ▒   ░    ░  
           ░         ░  ░   ░      ░ ░      ░      ░ ░      ░ ░      ░ ░   ░    ░  
                                     ░ ░                                            
    """
    print(welcome_message)

# Función para mostrar una animación llamativa durante la descarga
def download_with_animation(stream, output_path, filename):
    total_size = stream.filesize
    bytes_downloaded = 0
    with open(os.path.join(output_path, filename), "wb") as f:
        for chunk in tqdm(
            iterable=stream.stream_to_buffer(chunk_size=1024),
            total=total_size // 1024,
            unit='KB',
            desc=filename,
            ncols=100
        ):
            if chunk:
                f.write(chunk)
                bytes_downloaded += len(chunk)

# Función para descargar un video
def download_video(url):
    try:
        yt = pytube.YouTube(url)
        stream = yt.streams.get_highest_resolution()
        output_path = "./downloads"
        print(f"Descargando video: {yt.title}")
        stream.download(output_path)
        print("Video descargado exitosamente!")
    except AgeRestrictedError:
        print("El video está restringido por edad y no se puede descargar.")

# Función para descargar música
def download_audio(url):
    try:
        yt = pytube.YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        output_path = "./downloads"
        print(f"Descargando audio: {yt.title}")
        stream.download(output_path, filename=f"{yt.title}.mp3")
        print("Audio descargado exitosamente!")
    except AgeRestrictedError:
        print("El video está restringido por edad y no se puede descargar.")

# Función para descargar una playlist como videos
def download_playlist(url):
    pl = pytube.Playlist(url)
    output_path = "./downloads"
    print(f"Descargando playlist: {pl.title}")
    for video_url in pl.video_urls:
        try:
            yt = pytube.YouTube(video_url)
            stream = yt.streams.get_highest_resolution()
            print(f"Descargando video: {yt.title}")
            stream.download(output_path)
            print("Video descargado exitosamente!")
        except AgeRestrictedError:
            print(f"El video {yt.title} está restringido por edad y no se puede descargar.")
    print("Playlist descargada exitosamente!")

# Función para descargar una playlist como música
def download_playlist_audio(url):
    pl = pytube.Playlist(url)
    output_path = "./downloads"
    print(f"Descargando playlist como música: {pl.title}")
    for video_url in pl.video_urls:
        try:
            yt = pytube.YouTube(video_url)
            stream = yt.streams.filter(only_audio=True).first()
            print(f"Descargando audio: {yt.title}")
            stream.download(output_path, filename=f"{yt.title}.mp3")
            print("Audio descargado exitosamente!")
        except AgeRestrictedError:
            print(f"El video {yt.title} está restringido por edad y no se puede descargar.")
    print("Playlist descargada exitosamente!")

if __name__ == "__main__":
    # Crear el directorio de descargas si no existe
    if not os.path.exists("./downloads"):
        os.makedirs("./downloads")

    print_welcome_message()

    while True:
        print("\nOpciones:")
        print("1. Descargar video")
        print("2. Descargar música")
        print("3. Descargar playlist como videos")
        print("4. Descargar playlist como música")
        print("5. Salir")
        option = input("Seleccione una opción: ")

        if option == "1":
            url = input("Ingrese la URL del video de YouTube: ")
            download_video(url)
        elif option == "2":
            url = input("Ingrese la URL del video de YouTube: ")
            download_audio(url)
        elif option == "3":
            url = input("Ingrese la URL de la playlist de YouTube: ")
            download_playlist(url)
        elif option == "4":
            url = input("Ingrese la URL de la playlist de YouTube: ")
            download_playlist_audio(url)
        elif option == "5":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, por favor intente de nuevo.")