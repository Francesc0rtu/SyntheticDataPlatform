import logging
import os.path

from flask import Flask, render_template, request, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename

# [logging config
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
# logging config]


app = Flask(__name__)
app.secret_key = "somesecretkey"

app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.png', '.csv', '.zip']
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'DATA/input_data')
DOWNLOAD_FOLDER  = os.path.join(os.getcwd(), 'DATA/download')


# http://localhost:5000
@app.route('/', methods=['GET'])
def index():
    logging.info('Showing index page')
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_files():
    """Upload a file."""
    logging.info('Starting file upload')

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    metadata  = request.files['metadata']
    # obtaining the name of the destination file
    filename = file.filename
    metadata_name  = metadata.filename
    if filename == '':
        logging.info('Invalid file')
        flash('No file selected for uploading')
        return redirect(request.url)
    else:
        logging.info('Selected file is= [%s]', filename)
        file_ext = os.path.splitext(filename)[1]
        if file_ext in app.config['ALLOWED_EXTENSIONS']:
            secure_fname = secure_filename(filename)
            file.save(os.path.join(UPLOAD_FOLDER, secure_fname))
            logging.info('Upload is successful')
            flash('File uploaded successfully')
            return redirect('/')
        else:
            logging.info('Invalid file extension')
            flash('Not allowed file type')
            return redirect(request.url)


@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    """Download a file."""
    logging.info('Downloading file= [%s]', filename)
    logging.info(app.root_path)
    full_path = os.path.join(app.root_path, DOWNLOAD_FOLDER)
    logging.info(full_path)
    return send_from_directory(full_path, filename, as_attachment=True)


# http://localhost:5000/files
@app.route('/files', methods=['GET'])
def list_files():
    """Endpoint to list files."""
    logging.info('Listing already uploaded files from the upload folder.')
    upf = []
    for filename in os.listdir(DOWNLOAD_FOLDER):
        path = os.path.join(DOWNLOAD_FOLDER, filename)
        if os.path.isfile(path):
            upf.append(filename)

    # return jsonify(uploaded_files)
    return render_template('list.html', files=upf)


def check_upload_dir():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)


if __name__ == '__main__':
    check_upload_dir()
    # Development only: run "python app.py" and open http://localhost:5000
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=False, port=server_port, host='0.0.0.0')
