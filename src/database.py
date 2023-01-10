import pymongo
from pymongo.server_api import ServerApi
import os
import base64
from getpass import getpass
import gridfs
from dotenv import load_dotenv
from src.util import bcolors


load_dotenv("config/.env")
class Database():
    def __init__(self):
        self.db = self.connect_to_database()
        self.InputData = gridfs.GridFS(self.db, 'InputData')
        self.OutputData = gridfs.GridFS(self.db, 'OutputData')
        self.User = self.db["User"]
        self.input_path = "DATA/input/"
        self.output_path = "DATA/output/"

    def connect_to_database(self):
        '''Connect to the database, if the user has not saved the credential in env variable, ask for them.
        The mongodb databse is auth also with IP.
        '''
        #print("To connect to the database, please enter the following information:")
        # auto_login = input("Do you want connect with saved credential? (y/n): ")
        # if auto_login == "y":
        #     username = os.getenv("MONGO_USER")
        #     password = os.getenv("MONGO_PASS")
        #     mongo_host = os.getenv("MONGO_HOST")
        # else:
        #     mongo_host = input("Name of the mongo project: ")
        #     username = input("Username: ") 
        #     password = getpass()

        MONGO_URI = os.getenv("MONGO_URI")
            
        #connect to the database
        client = pymongo.MongoClient(MONGO_URI, server_api=ServerApi('1'))
        db = client['SDP']

        print(bcolors.OKGREEN + "Connected to the database" + bcolors.ENDC)
        return db

    def load_input_data(self, filename):
        username = filename.split("-")[0]
        path = "DATA/input/" + filename

        with open(path, "rb") as file:
            encoded = base64.b64encode(file.read())
        self.InputData.put(encoded, filename=filename, username=username)
    
    def load_output_data(self, filename, base_dataset_filename):
        username = filename.split("-")[0]
        username = username.split(":")[1]
        path = "DATA/output/" + filename

        with open(path, "rb") as file:
            encoded = base64.b64encode(file.read())
        self.OutputData.put(encoded, filename=filename, username=username, base_dataset=base_dataset_filename)

    def load_user(self,username,email,password):
        self.User.insert_one({"Username": username, "Email": email, "Password": password})

    def get_input_data(self, filename):
        username = filename.split("-")[0]
        path = "DATA/input/" + filename

        #if the file is already in the local machine do not retrive
        if os.path.exists(path):
            return 
        file = self.InputData.find_one(filter={"filename": filename, "username": username})
        with open(path, 'wb') as f:  
            f.write(base64.b64decode(file.read()))
        
    def get_output_data(self, filename):
        username = filename.split("-")[0]
        path = "DATA/output/" + filename

        #if the file is already in the local machine do not retrive
        if os.path.exists(path):
            return 
        file = self.OutputData.find_one(filter={"filename": filename, "username": username})
        with open(path, 'wb') as f:  
            f.write(base64.b64decode(file.read()))

    def get_all_input_data(self, username):
        '''Return a list of pointers of all the input dataset of the user.'''
        return self.InputData.find(filter={"username": username})
    def get_all_output_data(self):
        '''Return a list of pointers of all the output dataset of the user'''
        return self.OutputData.find()

    def get_user(self,username=None, email=None):
        '''Return the user with the given username or email'''
        if username is not None:
            return self.User.find_one({"Username": username})
        elif email is not None:
            return self.User.find_one({"Email": email})
        





    







