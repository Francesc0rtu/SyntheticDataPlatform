import logging
import os.path
from flask import Flask, render_template, request, redirect,  flash, send_from_directory, url_for
from flask_wtf.csrf import CSRFProtect
import os
from flask_login import login_user, current_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename

#import src module
from src.database import Database, ListOfdatasets
from src.util import check_user_exist, zip_and_move
from src.form import Login, Register, Upload
from src.core import generate_synthetic_data


# Starting app
app = Flask(__name__)
CSRFProtect(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
csrf.init_app(app)

app.config['ALLOWED_EXTENSIONS'] = ['.json', '.csv']
app.config['MAX_CONTENT_LENGTH'] = 100000 * 1024 * 1024

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'DATA/input')
DOWNLOAD_FOLDER  = os.path.join(os.getcwd(), 'DATA/output')


# Load database
database = Database()

#Logging 
login = LoginManager(app)
login.login_view = 'login'



# * Define User class and logging manager
class User:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated():
        return True

    @staticmethod
    def is_active():
        return True

    @staticmethod
    def is_anonymous():
        return False

    def get_id(self):
        return self.username

    @login.user_loader
    def load_user(username):
        u = database.get_user(username=username)
        if not u:
            return None
        return User(username=u['Username'])


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if current_user.is_authenticated:
            return redirect(url_for('upload'))
        form = Login()
        if form.validate_on_submit():
            user = database.get_user(username=form.name.data)
            
            if user and check_password_hash(user['Password'], form.password.data):
                user_obj = User(username=user['Username'])
                login_user(user_obj)
                next_page = request.args.get('next')
                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('upload')
                return redirect(next_page)
            else:
                error = "Invalid username or password"
        return render_template('login.html', title='Sign In', form=form, error=error)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        error = None
        form = Register()
        if form.validate_on_submit():
            msg = check_user_exist(database=database, username=form.username.data, email=form.email.data)
            if msg:
                error = msg
                return render_template('signup.html', form=form, error=error)
            hash_password = generate_password_hash(form.password.data)
            database.load_user(username=form.username.data, email=form.email.data, password=hash_password)
            return redirect(url_for('login'))
            
        return render_template('signup.html', form=form, error=error)




# * Starting point of application
@app.route('/', methods=['GET'])
def index():
    return redirect(url_for('login'))


# * Upload page
@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    msg = None
    username = current_user.username
    path = "DATA/input/tmp/"
    form = Upload()
    if form.validate_on_submit():

        dataset_name = form.dataset_name.data
        for file in form.files.data:
            file_filename = secure_filename(file.filename)
            file.save(path + file_filename)
  

        filename = zip_and_move(path, current_user.username, dataset_name)
        generate_synthetic_data(filename)
        msg = "Synthetic data generated successfully"
  
    return render_template('upload.html', username=username, form=form, msg=msg)




    


# * Download page
@app.route('/download/<path:data_id>', methods=['GET'])
def download(data_id):
    """Download a file."""
    full_path = database.get_output_data(id=data_id)
    filename = full_path.split('/')[-1]
    full_path = full_path.split(filename)[0]

    return send_from_directory(full_path, filename, as_attachment=True)

# * Download page
@app.route('/downloadInput/<path:data_id>', methods=['GET'])
def downloadInput(data_id):
    """Download a file."""
    full_path = database.get_input_dataset_from_output_id(id=data_id)
    filename = full_path.split('/')[-1]
    full_path = full_path.split(filename)[0]

    return send_from_directory(full_path, filename, as_attachment=True)

# http://localhost:5000/files
@app.route('/files', methods=['GET'])
def list_files():
    """Endpoint to list files."""
    files = ListOfdatasets(database).get_dicts()

    # return jsonify(uploaded_files)
    return render_template('list.html', list_of_files_info=files)

@app.route('/documentation', methods=['GET'])
def documentation():
    return render_template('documentation.html')
def check_upload_dir():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)






# * Main function

if __name__ == '__main__':
    check_upload_dir()
    # Development only: run "python app.py" and open http://localhost:5000
    server_port = os.environ.get('PORT', '5000')
    app.run(debug=False, port=server_port, host='0.0.0.0')



