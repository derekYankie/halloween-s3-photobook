from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import boto3
from filters import datetimeformat, file_type

#Use boto3 to access s3 resource
#I'm having boto3 use my aws cli creds insted of storing it in an enviorment variable file
boto3.setup_default_session(profile_name='default')
s3 = boto3.resource('s3')


#Create app
app = Flask(__name__)
Bootstrap(app)
#Register jinja filters
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type

#Route index page
@app.route('/')
def index():
    print("Dude, you're webpage is running!")
    return render_template('index.html')

#Route Halloween files page
@app.route('/files')
def files():
 
    my_bucket = s3.Bucket('halloween-s3-photobook-2021')
    #print all items in s3 Bucket
    for file in my_bucket.objects.all():
        print(f"file name: {file.key}")
    summaries = my_bucket.objects.all()
    print(f"S3 Bucket Object:", my_bucket)

    return render_template('files.html', my_bucket=my_bucket, files=summaries)


if __name__ == '__main__':
    app.run()