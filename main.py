from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from pytube import YouTube
import os

def create_playlist(link: str, drive):
    drive.get(link)
    time.sleep(5)
    info = []

    playlist = drive.find_elements(By.XPATH, '//div[@class="h4HgbO_Uu1JYg5UGANeQ wTUruPetkKdWAR1dd6w4"]')
    title = drive.find_element(By.CSS_SELECTOR, 'h1[class="Type__TypeElement-sc-goli3j-0 dYGhLW"]').text
    info.append(title)
    tracklist = []

    for song in playlist:
        dic_track = {
            'index': '',
            'name': '',
            'artist': ''
        }
        
        dic_track['index'] = (song.find_element(By.CSS_SELECTOR, 'span')).text
        dic_track['name'] = (song.find_element(By.CSS_SELECTOR,'div[class="Type__TypeElement-sc-goli3j-0 fZDcWX t_yrXoUO3qGsJS4Y6iXX standalone-ellipsis-one-line"]')).text
        dic_track['artist'] = (song.find_element(By.CSS_SELECTOR, 'span[class="Type__TypeElement-sc-goli3j-0 bDHxRN rq2VQ5mb9SDAFWbBIUIn standalone-ellipsis-one-line"]')).text
        
        tracklist.append(dic_track)
    info.append(tracklist)
           
    return info

def download_songs(info, drive): 
    title = info[0]
    tracks = info[1]
    # choose where you want the playlist to be downloaded
    folder_path = 'C:\\Users\\Usuario\\Downloads\\' + title

    # creating playlist folder
    try:
        os.mkdir(folder_path)
        print('playlist folder created')
    except FileExistsError:
        print('folder already exists')  

    # finding the youtube link
    yt_page = "https://youtube.com"

    for track in tracks:
        drive.get(yt_page)
        time.sleep(5)
        search_bar = drive.find_element(By.CSS_SELECTOR, "input[id='search']")
        search_bar.click()
        search_bar.send_keys(f"{track['name']} {track['artist']}")
        time.sleep(3)
        bt_search = drive.find_element(By.CSS_SELECTOR, 'button[id="search-icon-legacy"]')
        bt_search.click()
        time.sleep(5)
        first_video = drive.find_element(By.CSS_SELECTOR, 'ytd-video-renderer[class="style-scope ytd-item-section-renderer"]')
        tag_a = first_video.find_element(By.CSS_SELECTOR, 'a[id="thumbnail"]')
        video_link = tag_a.get_attribute('href')
        print(f"Downloading: {track['name']} by: {track['artist']}")

        # download current song
        youtube = YouTube(video_link)
        video = youtube.streams.filter(file_extension='mp4').first()
        print('downloading song...')
        time.sleep(5)
        out_file = video.download(output_path=folder_path)
        new_file = folder_path + '/' + track['artist'] + ' - ' + track['name'] + '.mp3'
        os.rename(out_file, new_file)
        print('song downloaded')
        time.sleep(2)

def main():
    # any spotify playlist link
    LINK = 'SPOTIFY PLAYLIST/ALBUM LINK GOES HERE'
    drive = webdriver.Chrome()
    playlist = create_playlist(LINK, drive) # get the songs and artists from the playlist as a dictionary list
    
    download_songs(playlist, drive)
    drive.quit()
    print('done')

if __name__ == "__main__":
    main()
