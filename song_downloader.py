from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import yt_dlp

def create_playlist(link: str, drive):
    drive.get(link)
    time.sleep(5)
    info = []

    playlist = drive.find_elements(By.CSS_SELECTOR, 'div[data-testid="tracklist-row"]')
    title = drive.find_element(By.CSS_SELECTOR, 'h1[class="e-9812-text encore-text-headline-large encore-internal-color-text-base"]').text
    info.append(title)
    tracklist = []

    for song in playlist:
        dic_track = {
            'index': '',
            'name': '',
            'artist': ''
        }
        
        dic_track['index'] = (song.find_element(By.CSS_SELECTOR, 'span')).text
        dic_track['name'] = (song.find_element(By.CSS_SELECTOR,'div[class="e-9812-text encore-text-body-medium encore-internal-color-text-base btE2c3IKaOXZ4VNAb8WQ standalone-ellipsis-one-line"]')).text
        dic_track['artist'] = (song.find_element(By.CSS_SELECTOR, 'span[class="e-9812-text encore-text-body-small"]')).text
        
        tracklist.append(dic_track)
    info.append(tracklist)
     
    return info

def download_songs(download_path, playlist, drive): 
    title = playlist[0]
    tracks = playlist[1]
    # choose where you want the playlist to be downloaded
    folder_path = os.path.join(download_path, title)

    # creating playlist folder
    try:
        os.mkdir(folder_path)
        print('playlist folder created')
    except FileExistsError:
        print('folder already exists')  

    # finding the youtube link
    yt_page = "https://youtube.com"

    for track in tracks:
        try:
            drive.get(yt_page)
            time.sleep(7)
            search_bar = drive.find_element(By.CSS_SELECTOR, "input[name='search_query']")
            search_bar.click()
            search_bar.send_keys(f"{track['name']} {track['artist']}")
            time.sleep(3)
            bt_search = drive.find_element(By.CSS_SELECTOR, 'button[class="ytSearchboxComponentSearchButton"]')
            bt_search.click()
            time.sleep(5)
            first_video = drive.find_element(By.CSS_SELECTOR, 'ytd-video-renderer[class="style-scope ytd-item-section-renderer"]')
            tag_a = first_video.find_element(By.CSS_SELECTOR, 'a[id="thumbnail"]')
            video_link = tag_a.get_attribute('href')
            print(f"Downloading: {track['name']} by: {track['artist']}")
            
            filename = f"{track['artist']} - {track['name']}"

            # download current song
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(folder_path, filename + '.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',     # converte para mp3
                    'preferredquality': '320',     # qualidade do áudio
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_link])
            print('song downloaded')
        except Exception as e:
            print(f"Error while downloading: {str(e)}")

def normalize_path(path: str) -> str:
    # Escapa qualquer barra invertida isolada (ex: \U) para \\U
    safe_path = path.encode('unicode_escape').decode()
    return safe_path.replace("\\", "/")

def execute(link, download_path):
    download_path = normalize_path(download_path)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    service = Service(executable_path="chromedriver.exe")
    
    drive = webdriver.Chrome(service=service, options=options)
    playlist = create_playlist(link, drive) # get the songs and artists from the playlist as a dictionary list
    download_songs(download_path, playlist, drive) # download the songs from YouTube based on the list

    drive.quit()
    print('done')
    return playlist[0]

