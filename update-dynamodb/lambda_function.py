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
    Status=status.COMPLETED.value
    s3=boto3.client('s3')
    db = boto3.resource('dynamodb')
    db_tb=db.Table("MP3-youtube-downloader")
    db_tb.put_item(
            Item={'VideoID': filename,
                'Status' : Status,
             } )
    resp = s3.delete_object(Bucket='youtubemp3mediafiles', Key=deletekey)
    
    s3obj = boto3.resource('s3')
    s3_object = s3obj.Object('youtubemp3mediafiles', keyvalue)
    s3_object.metadata.update({'Content-Disposition':'attachment'})
    s3_object.copy_from(CopySource={'Bucket':'youtubemp3mediafiles', 'Key': keyvalue}, Metadata=s3_object.metadata, MetadataDirective='REPLACE')
    print('done')
