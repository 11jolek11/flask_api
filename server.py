from flask import Flask, flash, request, redirect, url_for, jsonify
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = './assets/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/files')
def list_files():
    files = []
    for entry in os.listdir(UPLOAD_FOLDER):
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, entry)):
            files.append(entry)
    resp = jsonify({'files': files})
    resp.status_code = 200
    return resp

@app.route('/files/<file>')
def get_line(file):
    resp = jsonify({})
    line = request.args.get('line', default=1, type=int)
    if not os.path.exists(os.path.join(UPLOAD_FOLDER, file)):
        resp = jsonify({'message': "file not found"})
        resp.status_code = 404
        return resp
    with open(os.path.join(UPLOAD_FOLDER, file)) as file_name:
        temp = file_name.readlines()[line-1]
        resp = jsonify({'content': temp})
        resp.status_code = 200
    return resp

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            # FIXME: 
            print('no file found')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print("Empty file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resp = jsonify({'message': "File transfer completed"})
            resp.status_code = 201
            return resp
    return jsonify({'message': "Error 500"})


if __name__ == "__main__":
    app.run()
