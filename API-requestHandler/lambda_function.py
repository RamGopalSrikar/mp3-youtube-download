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

    print(event)
    URL_id=event['params']['path']['URL']
    #initiating return parameters
    Status=status.EMPTY.value
    name = 'None'
    S3_presignedUrl='Not Available'
    #checking if file already exist in dynamodb
    db = boto3.resource('dynamodb')
    db_tb=db.Table("MP3-youtube-downloader")
    val = db_tb.get_item(
    Key={
        'videoID' : URL_id
    }
    )
    if 'Item' in val:
        print(val['Item'])
        filename=val['Item']['filename']
        Status=val['Item']['Status']
        name=filename.split('.')[0]
        if (val['Item']['Status']==2):
            s3 = boto3.client('s3')
            S3_presignedUrl= s3.generate_presigned_url("get_object", Params={'Bucket':'test-srikar-data','Key':filename},ExpiresIn=100)
        else:
            print('file is still processing')
    else:
        sqs = boto3.resource('sqs')
        queue = sqs.get_queue_by_name(QueueName="YouTube-mp3player")
        response=queue.send_message(MessageBody=URL_id)
        print(response)


    return {
        'statusCode': 200,
        'name':name,
        'Status' : Status,
        's3presigned-url': S3_presignedUrl
    }


