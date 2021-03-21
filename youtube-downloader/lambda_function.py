from __future__ import unicode_literals
import youtube_dl, sys
from smart_open import open
from contextlib import redirect_stdout

        
def lambda_handler(event, context):

    ydl_opts = { 'outtmpl': '-', 'cachedir': False, 'logtostderr': True, 'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }] }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        with open('s3://srikar-static/test.mp4','wb') as f:
            with redirect_stdout(f): 
                ydl.download(['https://www.youtube.com/watch?v=zzEYsi_P0RU'])


    print('done')
