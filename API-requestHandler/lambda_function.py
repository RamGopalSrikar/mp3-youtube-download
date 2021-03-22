import json
import boto3
from enum import Enum

class status(Enum):
    EMPTY = 0
    PROCESSING = 1
    COMPLETED = 2
    FAILED = 3



def lambda_handler(event, context):
    # TODO implement
    #URL_id=event['params']['path']['URL']
    URL_id='sCbbMZ-q4-I'
    #initiating return parameters
    Status=0
    name = 'None'
    S3_presignedUrl='Not Available'
    #checking if file already exist in dynamodb
    db = boto3.resource('dynamodb')
    db_tb=db.Table("MP3-youtube-downloader")
    val = db_tb.get_item(
    Key={
        'VideoID' : URL_id
    }
    )
    print(val)
    if 'Item' in val:
        print(val['Item'])
        Status=val['Item']['Status']
        filename=URL_id+'.mp3'
        if (val['Item']['Status']==2):
            print('generating pre-signed URL')
            s3 = boto3.client('s3')
            S3_presignedUrl= s3.generate_presigned_url("get_object", Params={'Bucket':'youtubemp3mediafiles','Key':filename},ExpiresIn=100)
        else:
            print('file is still processing')
    else:
        print('file being sent for SQS to process')
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName="youtubemp3requests")
        response=queue.send_message(MessageBody=URL_id)


    return {
        'statusCode': 200,
        'name':name,
        'Status' : Status,
        's3presigned-url': S3_presignedUrl
    }


