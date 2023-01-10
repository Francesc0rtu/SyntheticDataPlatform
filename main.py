import logging
import os.path

from flask import Flask, render_template, request, redirect,  flash, send_from_directory, url_for
from werkzeug.utils import secure_filename



# [logging config
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO)
# logging config]


app = Flask(__name__)
app.secret_key = "somesecretkey"

app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.png', '.csv', '.zip']
app.config['MAX_CONTENT_LENGTH'] = 100000 * 1024 * 1024

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'DATA/input')
DOWNLOAD_FOLDER  = os.path.join(os.getcwd(), 'DATA/output')


@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))


# http://localhost:5000/upload
@app.route('/upload', methods=['GET'])
def upload():
    logging.info('Showing upload page')
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    """Upload a file."""
    logging.info('Starting file upload')

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    files = request.files.getlist("file")
    for file in files:
       file.save(os.path.join(UPLOAD_FOLDER, file.filename))
 
    return redirect('/upload')


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('upload'))
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
    
        if username == 'admin' and password == 'admin':
            error = 'Invalid Credentials. Please try again.'
        
            
    return render_template('register.html', error=error)


if __name__ == '__main__':
    check_upload_dir()
    # Development only: run "python app.py" and open http://localhost:5000
    server_port = os.environ.get('PORT', '8000')
    app.run(debug=False, port=server_port, host='0.0.0.0')



