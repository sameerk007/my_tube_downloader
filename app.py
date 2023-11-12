import streamlit as st
from pytube import Playlist
import os

# Function to download a range of videos from a YouTube playlist with a specific resolution
def download_playlist_range(playlist_url, output_path, start_index, end_index, resolution='720p'):
    playlist = Playlist(playlist_url)
    total_videos = len(playlist.videos)

    # Validate the indices
    if not 1 <= start_index <= total_videos or not 1 <= end_index <= total_videos or start_index > end_index:
        st.warning("Invalid start or end index. Please enter valid indices within the range of the playlist.")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)

    st.write(f'Total Videos in Playlist: {total_videos}')
    st.write(f'Downloading videos from index {start_index} to {end_index}')

    for index, video in enumerate(playlist.videos, start=1):
        if start_index <= index <= end_index:
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
    st.write("Enter the YouTube Playlist URL, select the desired resolution, specify the download folder path, and choose a range of videos to download.")

    playlist_url = st.text_input("Enter YouTube Playlist URL")
    desired_resolution = st.selectbox("Select Resolution", ["1080p", "720p", "480p"])
    download_path = st.text_input("Download Folder Path", "./downloads")
    start_index = st.number_input("Start Index", min_value=1, value=1)
    end_index = st.number_input("End Index", min_value=1, value=1)

    if st.button("Download"):
        if not playlist_url:
            st.warning("Please enter a YouTube Playlist URL.")
        else:
            st.write("Downloading...")
            download_playlist_range(playlist_url, download_path, start_index, end_index, resolution=desired_resolution)
            st.write("Download completed!")

if __name__ == "__main__":
    main()
