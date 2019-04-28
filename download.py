#!/usr/bin/python3
import datetime
import glob
import shutil
import sys

import ffmpy
import youtube_dl

math_tutorial = 'Lga-oupKJx4'
discussion = 'rfqJt8Z7Mvk'

def audio(video_id, work_dir):
    YOUTUBE_BASE_URL = 'https://www.youtube.com/watch?v=' + video_id
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': work_dir + '/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([YOUTUBE_BASE_URL])

def dwnld(video_id, work_dir):
    YOUTUBE_BASE_URL = 'https://www.youtube.com/watch?v=' + video_id
    # listsubtitles: True   lists all available subtitles
    # allsubtitles: True    downloads all the subtitles of the video
    # subtitleslangs: [langs]   list of languages of the subtitles to download
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'outtmpl': work_dir + '/%(id)s.%(ext)s',
        'subtitlesformat': 'vtt',
        'writesubtitles': True,
        'format': 'mp4'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([YOUTUBE_BASE_URL])
        except:
            print("nope")
            return

    input = video_id + ".mp4"
    output = video_id + ".wav"
    try:
        audio(video_id, work_dir)
    #try:
    #    ff = ffmpy.FFmpeg(
    #        inputs={input: None},
    #        outputs={output: '-ar 11025 -ac 1 -s s16 -b:a 176k'}
    #    )
    #    ff.run()
    #except FileExistsError:
    #    print("Audio already extracted")
    except Exception as e:
        print("Failed to extract audio for " + str(video_id) + ": " + str(e))
