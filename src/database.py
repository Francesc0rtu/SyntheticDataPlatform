import pymongo
from bson.objectid import ObjectId
from pymongo.server_api import ServerApi
import os
import base64
from getpass import getpass
import gridfs
from dotenv import load_dotenv
from src.util import bcolors
from dotenv import load_dotenv

load_dotenv()


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

        MONGO_URI = os.getenv("MONGO_URI")

            
        #connect to the database
        client = pymongo.MongoClient(MONGO_URI, server_api=ServerApi('1'))
        try:
            client.server_info()
        except:
            print(bcolors.FAIL + "Unable to connect to the database" + bcolors.ENDC)
            exit(1)
        db = client['SDP']

        print(bcolors.OKGREEN + "Connected to the database" + bcolors.ENDC)
        return db

    def load_input_data(self, filename, description, openess):
        username = filename.split("-")[0]
        path = "DATA/input/" + filename

        with open(path, "rb") as file:
            encoded = base64.b64encode(file.read())
        self.InputData.put(encoded, filename=filename, username=username, description=description, openess=openess)
    
    def load_output_data(self, filename, base_dataset_availability, description):
        username = filename.split("-")[0]
        username = username.split(":")[1]
        path = "DATA/output/" + filename

        with open(path, "rb") as file:
            encoded = base64.b64encode(file.read())
        self.OutputData.put(encoded, filename=filename, username=username, base_dataset=base_dataset_availability, description=description)

    def load_user(self,username,email,password):
        self.User.insert_one({"Username": username, "Email": email, "Password": password})

    def get_input_data(self, filename):
        username = filename.split("-")[0]
        path = "DATA/input/" + filename

        #if the file is already in the local machine do not retrive
        if os.path.exists(path):
            return path
        file = self.InputData.find_one(filter={"filename": filename, "username": username})
        with open(path, 'wb') as f:  
            f.write(base64.b64decode(file.read()))

        return path
        
    def get_output_data(self, filename=None, id=None):
        if filename is not None:
            username = filename.split("-")[0]
            path = "DATA/output/" + filename

            #if the file is already in the local machine do not retrive
            if os.path.exists(path):
                return path
            file = self.OutputData.find_one(filter={"filename": filename, "username": username})
            with open(path, 'wb') as f:  
                f.write(base64.b64decode(file.read()))

        if id is not None:
            file = self.OutputData.find_one({"_id": ObjectId(id)})
            username = file.filename.split("-")[0]
            path = "DATA/output/" + file.filename

            #if the file is already in the local machine do not retrive
            if os.path.exists(path):
                return path
            with open(path, 'wb') as f:  
                f.write(base64.b64decode(file.read()))
            return path

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

    def check_input_data_exist(self, filename):
        if self.InputData.exists({"filename": filename}):
            return True
        return False
    
    def get_input_dataset_from_output_id(self, id, external=False):
        file = self.OutputData.find_one({"_id": ObjectId(id)})
        if external is False:
            filename = file.filename.split(":")[1]
            path =  self.get_input_data(filename)
            return path, file

        if external is True:
            path = None
            filename = file.filename.split(":")[1]
            username = filename.split("-")[0]
            file = self.InputData.find_one(filter={"filename": filename, "username": username})
            return path, file






class ListOfdatasets():
    def __init__(self, database, datasets="output"):
        self.database = database
        if datasets == "input":
            self.pointer = self.database.get_all_input_data()
        else:
            self.pointer = self.database.get_all_output_data()
    
    def get_dicts(self):
        output_list = []
        for dataset in self.pointer:
            dataset_dict = {"Dataset_Name": dataset.filename.split("-")[1],
                            "User": dataset.username, 
                            "Size": dataset.length, 
                            "Upload_Data" : dataset.uploadDate,
                            "Description": dataset.description,
                            "Base_Dataset": dataset.base_dataset,
                            "Dataset_id": dataset._id}
            output_list.append(dataset_dict)
        return output_list

        





    
####### IMPLEMENT
# URI
# dataset/






