import boto3

#* Use boto3 to access s3 resource
#I'm having boto3 use my aws cli creds insted of storing it in an environment variable file
boto3.setup_default_session(profile_name='default')

# Hallowen bucket
s3 = boto3.resource('s3')
def get_bucket():
    s3_resource = boto3.resource('s3')
    halloween_bucket = s3.Bucket('halloween-s3-photobook-2021')

    return halloween_bucket