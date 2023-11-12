import streamlit as st
from pytube import Playlist
import os

# Function to download a YouTube playlist with a specific resolution
def download_playlist(playlist_url, output_path, resolution='720p'):
    playlist = Playlist(playlist_url)

    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    for video in playlist.videos:
        st.write(f'Downloading: {video.title}')
        # Filter streams by resolution
        streams = video.streams.filter(res=resolution)
        if streams:
            # Choose the first stream (highest quality) with the specified resolution
            selected_stream = streams[0]
            selected_stream.download(output_path)
            st.write(f'Download completed: {video.title}')
        else:
            st.write(f'Video "{video.title}" does not have a {resolution} stream.')

def main():
    st.title("YouTube Playlist Downloader")
    st.write("Enter the YouTube Playlist URL, select the desired resolution, and specify the download folder path.")

    playlist_url = st.text_input("Enter YouTube Playlist URL")
    desired_resolution = st.selectbox("Select Resolution", ["1080p", "720p", "480p"])
    download_path = st.text_input("Download Folder Path", "./downloads")

    if st.button("Download"):
        if not playlist_url:
            st.warning("Please enter a YouTube Playlist URL.")
        else:
            st.write("Downloading...")
            download_playlist(playlist_url, download_path, resolution=desired_resolution)
            st.write("Download completed!")

if __name__ == "__main__":
    main()
