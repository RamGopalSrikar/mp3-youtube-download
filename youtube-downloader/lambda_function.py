from __future__ import unicode_literals
import youtube_dl, sys
from smart_open import open
from contextlib import redirect_stdout
import boto3
from enum import Enum

class status(Enum):
    EMPTY = 0
    PROCESSING = 1
    COMPLETED = 2
    FAILED = 3
       
def lambda_handler(event, context):
    print(event)

    url_id=event['Records'][0]['body']
    print(url_id)
    url='https://www.youtube.com/watch?v='+url_id

    # checking if the file is present
    db = boto3.resource('dynamodb')
    db_tb=db.Table("MP3-youtube-downloader")
    val = db_tb.get_item(
    Key={
        'VideoID' : url_id
    }
    )
    print(val)
    if 'Item' in val:
        print('skip processing of the file')

    else:
    
        print('entered processing of the file')
        s3filename=url_id+".mp4"
        ydl_opts = { 'outtmpl': '-', 'cachedir': False, 'logtostderr': True, 'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }] }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            with open('s3://youtubemp3mediafiles/'+s3filename,'wb') as f:
                with redirect_stdout(f): 
                    ydl.download([url])
                    result=ydl.extract_info(url)

        filename = result['title']

        db_tb.put_item(
            Item={
                'VideoID': url_id,
                'Status'  : 1,
                'filename' : filename,
             } )
        print('done')

    return {
        'status' : 200,
    }
