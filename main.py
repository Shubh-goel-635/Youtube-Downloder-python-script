import os
import sys
import time
from pytube import YouTube, Playlist
from copy import deepcopy
from plyer import notification
import ctypes


def get_notification(name):
    icon_name = 'yt1.ico'
    icon_path = os.path.join(os.path.dirname(__file__), icon_name)
    notification.notify(title="Downloaded",
                        message=f'{name}',
                        app_name='Youtube Downloader',
                        app_icon=icon_path,
                        timeout=10
                        )


def progress_function(chunk, file_handle, bytes_remaining):
    global file_size
    current = ((file_size - bytes_remaining) / file_size)
    percent = '{0:.1f}'.format(current * 100)
    progress = int(50 * current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()


def get_reso(url):
    video = YouTube(url)
    reso = set()
    for stream in video.streams:
        if stream.resolution:
            reso.add(stream.resolution)
    reso = list(reso)
    reso.sort()
    return reso


def DownloadVideo(url, reso_type=1, name='', notifications=1):
    def downloadHighReso(url,video, name=''):
        video_reso_type = video.streams.filter(progressive=True).get_highest_resolution()
        global file_size
        file_size = video_reso_type.filesize
        name += video_reso_type.default_filename
        print(f'{name} of size {round(file_size / 1048576, 2)}MB')
        if not os.path.isfile(name):
            video_reso_type.download(filename=name)
            print('\n\tDownload Completed')
        else:
            print('\tAlready Available')

    def downloadLowReso(url, video, name=''):
        video_reso_type = video.streams.filter(progressive=True).get_lowest_resolution()
        global file_size
        file_size = video_reso_type.filesize
        name += video_reso_type.default_filename
        print(f'{name} of size {round(file_size / 1048576, 2)}MB')
        if not os.path.isfile(name):
            video_reso_type.download(filename=name)
            print('\n\tDownload Completed')
        else:
            print('\tAlready Available')

    def downloadAudioOnly(url, video, name=''):
        video_reso_type = video.streams.filter().get_audio_only()
        global file_size
        file_size = video_reso_type.filesize
        name += video_reso_type.default_filename
        print(f'{name} of size {round(file_size / 1048576, 2)}MB')
        if not os.path.isfile(name):
            video_reso_type.download(filename=name)
            print('\n\tDownload Completed')
        else:
            print('\tAlready Available')

    video = YouTube(url, on_progress_callback=progress_function)
    if reso_type == 1:
        downloadHighReso(url, video, name)
    elif reso_type == 2:
        downloadLowReso(url, video, name)
    elif reso_type == 3:
        downloadAudioOnly(url, video, name)
    else:
        print("Enter 1/2/3 Choice correctly!!")
        main()
    if notifications == 1:
        get_notification(video.title)


def DownloadPlaylist(url, reso_type=1):
    ytList = Playlist(url)
    start, end = 1, ytList.length

    print(f'{ytList.title} Contains {end} Video\nDo You Wish To Download All Video(y/n): ')
    ask = input()
    if ask.casefold() == 'y' or ask.casefold() == 'yes':
        print(f'Enter Start Of Playlist: ')
        start = int(input())
    elif ask.casefold() == 'n' or ask.casefold() == 'no':
        print(f'Enter Start And End Of Playlist: ')
        start, end = map(int, input().split())
    else:
        print("Enter y/n Correctly!!")
        DownloadPlaylist(url, reso_type)

    if not (1 <= start <= ytList.length and start <= end <= ytList.length):
        print('Enter start/end correctly!!')
        DownloadPlaylist(url, reso_type)

    first_video_link = ytList.video_urls[start - 1]
    first_video = YouTube(first_video_link)
    title = first_video.streams.get_highest_resolution().default_filename
    title = ''.join(title.split('.')[:-1])
    cwd = os.getcwd()
    new_dir = os.path.join(cwd, title)
    if not os.path.exists(new_dir):
        os.makedirs(title)
        print('New Directory Created')
    os.chdir(new_dir)

    count = deepcopy(start)
    for link in ytList.video_urls[start - 1:end]:
        DownloadVideo(url=link, reso_type=reso_type, name=str(count) + ' ',notifications=0)
        count += 1
    get_notification(ytList.title)


def main():
    app_name = 'Youtube Downloader - Made by Shubh Goel'
    ctypes.windll.kernel32.SetConsoleTitleW(app_name)
    path = os.path.dirname(__file__)

    output_path = os.path.join(path, 'Output')
    if not os.path.exists(output_path):
        os.chdir(path)
        os.makedirs(name='Output')
    os.chdir(output_path)

    url = input("Enter Link: ")
    is_video = input("Enter y if it is video else n: ")
    reso_type = int(input('1 - High Resolution \n2 - Low Resolution \n3 - Audio Only \nEnter Your Choice: '))

    if is_video.casefold() == 'y' or is_video.casefold() == 'yes':
        DownloadVideo(url, reso_type)
    elif is_video.casefold() == 'n' or is_video.casefold() == 'no':
        DownloadPlaylist(url, reso_type)
    else:
        print("Enter y/n only")
        main()


if __name__ == '__main__':
    main()
