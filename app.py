import streamlit as st
from streamlit_file_browser import st_file_browser
from song_downloader import execute

st.title("Spothiefy 😎")

link = st.text_input("Paste your playlist/album link:", placeholder="https://open.spotify.com/intl-pt/album/123456...")

download_path = st.text_input("Paste the folder path you wish the songs to be downloaded to:", placeholder="C:/User/Downloads...")
print(download_path)
if st.button("Download"):
    if not link or not download_path:
        st.warning("Please fill all info before downloading.")
    else:
        with st.spinner('Downloading songs, please wait...'):
            try:
                playlist_name = execute(link, download_path)
                st.success(f'{playlist_name} successfully downloaded! 🎶')
            except Exception as e:
                st.error(f"An error occurred while downloading: {str(e)}")

