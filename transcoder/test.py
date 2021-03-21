import boto3

s3 = boto3.client('s3')
response=s3.get_object(Bucket='srikar-static',Key='video.mp4')

outputs=[{
        'Key': 'audio.mp3',
        'PresetId' : '1351620000001-300010',
    },]

transcoder=boto3.client('elastictranscoder')
response=transcoder.create_job(
    PipelineId='1615590917710-tyvzlm',
    Input ={
        'Key' : 'video.mp4',
        'Container' : 'mp4',
    },
    Outputs=outputs,
)

print('done')