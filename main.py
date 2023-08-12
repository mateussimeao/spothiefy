from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pytube import YouTube

def create_playlist(link: str, drive):
    drive.get(link)
    time.sleep(5)
    playlist = drive.find_elements(By.XPATH, '//div[@class="h4HgbO_Uu1JYg5UGANeQ wTUruPetkKdWAR1dd6w4"]')
    tracklist = []

    for song in playlist:
        dic_track = {
        'index': '',
        'name': '',
        'artist': ''
    }
    print(song.text)
    
    dic_track['index'] = (song.find_element(By.CSS_SELECTOR, 'span')).text
    dic_track['name'] = (song.find_element(By.CSS_SELECTOR,'div[class="Type__TypeElement-sc-goli3j-0 fZDcWX t_yrXoUO3qGsJS4Y6iXX standalone-ellipsis-one-line"]')).text
    dic_track['artist'] = (song.find_element(By.CSS_SELECTOR, 'span[class="Type__TypeElement-sc-goli3j-0 bDHxRN rq2VQ5mb9SDAFWbBIUIn standalone-ellipsis-one-line"]')).text
    print(dic_track)
    tracklist.append(dic_track)
           
    drive.quit()
    return tracklist

def download_songs(tracks, drive): 
        #todo
        def download_yt(url, output_path):
            youtube = YouTube(url)
            video = youtube.streams.filter(only_audio=True).first()
            video.download(output_path)

        #def convert_to_mp3(input_file, output_file):
            

        yt_page = "https://youtube.com"
        drive.get(yt_page)
        time.sleep(5)
        search_bar = WebDriverWait(drive, 10).until(EC.element_to_be_clickable(By.CSS_SELECTOR, "input[id='search']"))
        search_bar.send_keys(tracks[0]['name'] + tracks[0]['artist'])
        first_video = drive.find_element(By.CSS_SELECTOR, 'ytd-video-renderer[class="style-scope ytd-item-section-renderer"]')
        tag_a = first_video.find_element(By.CSS_SELECTOR, 'a[id="thumbnail"]')
        video_link = tag_a.get_attribute('href')
        print(video_link)

        download_yt(video_link, './')

def main():
    # any spotify playlist link
    LINK = 'https://open.spotify.com/intl-pt/album/0uCgOj02DByzYk0iaaM327'
    drive = webdriver.Chrome()
    tracks = create_playlist(LINK, drive) # get the songs and artists from the playlist as a dictionary list
    print(tracks)
    
    #download_songs(tracks, drive)

if __name__ == "__main__":
    main()
