# SPOTHIEFY
Turn your Spotify playlists into mp3 files in an automated and easy way.

## Overview
Spothiefy is an application developed in Python using its library Selenium, which can automate web processes. Combining this with PyTube video downloader, it becomes really easy and practical to download the songs listed on your favorite Spotify playlist.

## How to Use It
1. **Clone the Repository**: `git clone https://github.com/mateussimeao/spothiefy.git`
2. **Choose your playlist**: Paste your playlist url on the "LINK" string (currently only taking spotify links)
3. **Set your download path**: Select the path in your local disk where you want the playlist folder to be created and downloaded by changing the USER_PATH string
4. **You are good to go!**: Just run the main.py file. Make sure you have the chrome web driver downloaded and the PyTube and Selenium libraries installed

## Common Issues
You may run into an exception *pytube.exceptions.RegexMatchError: __init__: could not find match for ^\w+\W*, if so, you can easily solve it by following the steps on [Stack Overflow](https://stackoverflow.com/questions/70776558/pytube-exceptions-regexmatcherror-init-could-not-find-match-for-w-w)
