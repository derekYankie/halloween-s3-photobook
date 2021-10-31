import boto3

#* Use boto3 to access s3 resource
#I'm having boto3 use my aws cli creds insted of storing it in an environment variable file
boto3.setup_default_session(profile_name='default')

#* Hallowen bucket
s3 = boto3.resource('s3')
def get_bucket():
    s3_resource = boto3.resource('s3')
    halloween_bucket = s3.Bucket('halloween-s3-photobook-2021')

    return halloween_bucket
#* Display images
def show_image(bucket):
    s3_client = boto3.client('s3')
    public_urls = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 100)
            public_urls.append(presigned_url)
    except Exception as e:
        pass
    print(f"[INFO] : The contents inside show_image = ", public_urls)
    return public_urls