# sudo apt install python3-tqdm
# sudo pip install pytube

import sys
from pytube import YouTube
from tqdm import tqdm

if len(sys.argv) != 2:
    print("Usage: python3 download_youtube_video.py <youtube_url>")
    sys.exit(1)

url = sys.argv[1]

try:
    yt = YouTube(url)
    
    stream = yt.streams.filter(res="1080p", mime_type="video/mp4").first()
    if not stream:
        stream = yt.streams.get_highest_resolution()
    
    print(f"Downloading {yt.title} in {stream.resolution}...")

    with tqdm(total=stream.filesize, unit='B', unit_scale=True, desc=yt.title) as pbar:
        def progress_function(stream, chunk, bytes_remaining):
            pbar.update(len(chunk))
        yt.register_on_progress_callback(progress_function)
        stream.download()

    print("Download completed!")
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)