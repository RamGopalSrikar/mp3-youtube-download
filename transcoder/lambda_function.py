
import boto3
from enum import Enum



def lambda_handler(event, context):
    
    print(event)
    keyvalue=event['Records'][0]['s3']['object']['key']
    filename=keyvalue.split('.')[0]
    outputkey=filename+'.mp3'
    outputs=[{
            'Key': outputkey,
            'PresetId' : '1351620000001-300010',
        },]

    transcoder=boto3.client('elastictranscoder')
    response=transcoder.create_job(
        PipelineId='1616349788040-7gsiuk',
        Input ={
            'Key' : keyvalue,
            'Container' : 'mp4',
        },
        Outputs=outputs,
    )
    print(response)
    print('done')
