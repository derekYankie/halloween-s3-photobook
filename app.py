from flask import Flask, render_template, request, redirect, url_for
from flask.helpers import flash
from resources import get_bucket
from flask_bootstrap import Bootstrap
from filters import datetimeformat, file_type

# * Create app
app = Flask(__name__)
Bootstrap(app)
app.secret_key= 'this_is_a_secret'
# * Register jinja filters
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['file_type'] = file_type

# * Landing page
@app.route('/')
def index():
    print("Dude, you're webpage is running!")
    return render_template('index.html')

# * Halloween files page/list
@app.route('/files')
def files():
    halloween_bucket = get_bucket()
    # * Display all items in s3 Bucket
    for file in halloween_bucket.objects.all():
        print(f"file name: {file.key}")
    summaries = halloween_bucket.objects.all()
    print(f"S3 Bucket Object:", halloween_bucket)

    return render_template('files.html', halloween_bucket=halloween_bucket, files=summaries)

# * Upload files 
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    halloween_bucket = get_bucket()
    #put uploaded file into bucket
    halloween_bucket.Object(file.filename).put(Body=file)
    print('Uploaded file:', file.filename)

    flash('File uploaded successfully')
    return redirect(url_for('files'))

# * Delete files 
@app.route('/delete', methods=['POST'])
def delete():
    key = request.form['key']

    halloween_bucket = get_bucket()
    halloween_bucket.Object(key).delete()

    flash('File deleted successfully')

    return redirect(url_for('files'))


if __name__ == '__main__':
    app.run()