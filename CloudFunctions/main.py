from google.cloud import bigquery
from google.cloud import vision_v1

def cloud_to_vision(file,context):
    bucket = file['bucket']
    filename = file['name']
    image_uri='gss://{}/{}'.format(bucket,filename)
    table_id = ''
