import streamlit as st
from pytube import Playlist ,YouTube 
from pytube.cli import on_progress
import os

# Function to download a range of videos from a YouTube playlist with a specific resolution
def download_playlist_range(playlist_url, output_path, start_index, end_index, resolution='720p'):
    playlist = Playlist(playlist_url)
    total_videos = len(playlist.videos)

    # Validate the indices
    if end_index==0 or end_index>total_videos:
        end_index = total_videos

    if start_index > end_index:
        st.warning("Invalid start or end index. Please enter valid indices within the range of the playlist.(1-Total_length)")
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
                # Get the file size to calculate the progress 
                selected_stream.download(output_path, filename=f"{video.title}.mp4",)

                st.write(f'Download completed: {video.title}')
               
            else:
                st.write(f'Video "{video.title}" does not have a {resolution} stream. Trying for best resolution')
                selected_stream = video.streams.get_highest_resolution()
                selected_stream.download(output_path, filename=f"{video.title}.mp4")
                st.write(f'Download completed: {video.title}')

    


def main():
    st.title("YouTube Playlist Downloader")
    st.write("Enter the YouTube Playlist URL, select the desired resolution, specify the download folder path, and choose a range of videos to download.")

    playlist_url = st.text_input("Enter YouTube Playlist URL")
    desired_resolution = st.selectbox("Select Resolution", ["1080p", "720p", "480p"])
    download_path = st.text_input("Download Folder Path", "./downloads")
    start_index = st.number_input("Start Index", min_value=1, value=1)
    end_index = st.number_input("End Index", min_value=0, value=0)

    if st.button("Download"):
        if not playlist_url:
            st.warning("Please enter a YouTube Playlist URL.")
        else:
            st.write("Downloading...")
            try:
                download_playlist_range(playlist_url, download_path, start_index, end_index, resolution=desired_resolution)
            except:
                video = YouTube(playlist_url,on_progress_callback=on_progress)
                st.write(f'Downloading: {video.title}')
                # Filter streams by resolution
                streams = video.streams.filter(res=desired_resolution)
                if streams:
                    # Choose the first stream (highest quality) with the specified resolution
                    selected_stream = streams[0]
                    selected_stream.download(download_path, filename=f"{video.title}.mp4")

                    st.write(f'Download completed: {video.title}')
                else:
                    st.write(f'Video "{video.title}" does not have a {desired_resolution} stream. Trying for best resolution')
                    selected_stream = video.streams.get_highest_resolution()
                    selected_stream.download(download_path, filename=f"{video.title}.mp4")
                    st.write(f'Download completed: {video.title}')

if __name__ == "__main__":
    main()
