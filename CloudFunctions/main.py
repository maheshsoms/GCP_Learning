from google.cloud import bigquery
from google.cloud import vision_v1

def cloud_to_vision(file,context):
    bucket = file['bucket']
    filename = file['name']
    image_uri = 'gs://{}/{}'.format(bucket,filename)
    table_id = 'explore-services-322117:MyPictures.Picture_meta'

    row = {
        'name': filename,
        'uri': image_uri,
        'label_anotations': [],
        'landmark_annotations': []
    }

    print('now reading {}'.format(image_uri))

    vision_client = vision_v1.IacImageAnnotatorClient()
    response = vision_client.annotate_image({
            'image': {
                'source': {
                    'image_uri': image_uri
                }
            }
    })

    labels = response.label_annotations
    landmarks = response.landmark_annotations

    if labels:
        for label in labels:
            row['label_annotations'].append({
                'description': label.description,
                'confidence': round(label.score*100, 2)
            })

    if landmarks:
        for landmark in landmarks:
            row['landmark_annotations'].append({
                'description': landmark.description,
                'confidence': round(landmark.score*100, 2)
            })
    bigquery_client = bigquery.Client()
    response = bigquery_client.insert_rows_json(table_id, [row])
