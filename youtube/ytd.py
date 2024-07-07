import sys
from pytube import YouTube

# Check if URL is passed as an argument
if len(sys.argv) != 2:
    print("Usage: python3 ytd.py <youtube_url>")
    sys.exit(1)

# Store the URL
url = sys.argv[1]

try:
    # Create a YouTube object with the URL
    yt = YouTube(url)
    
    # Get the highest resolution stream available
    stream = yt.streams.get_highest_resolution()
    
    # Download the video
    print(f"Downloading {yt.title}...")
    stream.download()
    print("Download completed!")
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
