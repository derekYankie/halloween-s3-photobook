from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import flash
from flask_bootstrap import Bootstrap
import boto3
from filters import datetimeformat, file_type

#* Use boto3 to access s3 resource
#I'm having boto3 use my aws cli creds insted of storing it in an environment variable file
boto3.setup_default_session(profile_name='default')
s3 = boto3.resource('s3')


#Create app
app = Flask(__name__)
Bootstrap(app)
app.secret_key= 'this_is_a_secret'
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

#Route uploaded files 
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    s3_resource = boto3.resource('s3')
    my_bucket = s3.Bucket('halloween-s3-photobook-2021')
    #put uploaded file into bucket
    my_bucket.Object(file.filename).put(Body=file)
    print('Uploaded file:', file.filename)

    flash('File uploaded successfully')
    return redirect(url_for('files'))

#Route deleted files 
@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    s3_resource = boto3.resource('s3')
    my_bucket = s3.Bucket('halloween-s3-photobook-2021')
    my_bucket.Object(key).delete()

    flash('File deleted successfully')

    return redirect(url_for('files'))


if __name__ == '__main__':
    app.run()