import boto3
from enum import Enum

class status(Enum):
    EMPTY = 0
    PROCESSING = 1
    COMPLETED = 2
    FAILED = 3

def lambda_handler(event, context):
    keyvalue=event['Records'][0]['s3']['object']['key']
    filename=keyvalue.split('.')[0]
    deletekey=filename+'.mp4'
    s3=boto3.client('s3')
    db = boto3.resource('dynamodb')
    db_tb=db.Table("MP3-youtube-downloader")
    db_tb.put_item(
            Item={'VideoID': filename,
                'Status' : 2,
             } )
    resp = s3.delete_object(Bucket='youtubemp3mediafiles', Key=deletekey)
    print('done')
