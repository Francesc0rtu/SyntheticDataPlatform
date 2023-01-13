import os
import zipfile

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_user_exist(database, username, email):
    user = database.get_user(username=username)
    mail = database.get_user(email=email)
    if user:
        msg = "Username already exists"
        return msg
    if mail:
        msg = "Email already exists"
        return msg
    return None

def zip_and_move(path, username, dataset_name):
    zip_filename = username + '-' + dataset_name + ".zip"
    destination_path = "DATA/input/" + zip_filename 
    with zipfile.ZipFile(destination_path, 'w') as zip_file:
        for root, dirs, files in os.walk(path):
            for file in files:
                zip_file.write(os.path.join(root, file), file)
    for _, _, files in os.walk(path):
        for file in files:
            os.remove(path +  file)
    return zip_filename
            
    
