import os
from flask import Flask, flash, request, redirect, render_template, jsonify

from werkzeug.utils import secure_filename
from resume_parser import resumeparse
import json


class Object(object):
    pass



app=Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()
# file Upload
UPLOAD_FOLDER = os.path.join(path, 'uploads')

if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = set(['doc', 'docx', 'pdf', 'txt'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        response = {}
        response['msg'] = ""
        response['data']  = {}
        response['isok'] = False
        if 'file' not in request.files:
            response['isok'] = False
            response['msg'] = "No file part"
            # flash('No file part')
            # return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            response['isok'] = False
            response['msg'] = "No file selected for uploading"
            # flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename) 
            file.save(filepath)
            data = resumeparse.read_file(filepath)
            response['isok'] = True
            response['msg'] = 'Successfully parsed'
            response['data'] = data
            # flash(data)
            # return jsonify(data)
            # flash('File successfully uploaded')
            # return redirect('/')
        else:
            response['isok'] = False
            response['msg'] = 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'
            # flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            # return redirect(request.url)
    
        return jsonify(response)
        

if __name__ == "__main__":
    app.run(host = '127.0.0.1',port = 5000, debug = False)



