from src.synthetic_generator import Synthetic_data
from src.database import Database
import zipfile
import shutil
import os


def generate_synthetic_data(filename, description, input_openess):
    '''From filename the function generates a synthetic dataset and upload the input and the output dataset in the database.
    All the local data are deleted after the process.
    '''

    # Unzip the dataset
    with zipfile.ZipFile("DATA/input/" + filename, 'r') as zip_ref:
        zip_ref.extractall("DATA/input/tmp/" + filename.split(".")[0])
    external_link = None
    if input_openess == "Open":
        external_link = json.load(open("DATA/input/tmp/" + filename.split(".")[0] + "/external_link.json", "r"))["dataset link"]

    # Generate synthetic data
    synthetic_data = Synthetic_data()
    synthetic_data.load_input_data(filename.split(".")[0])
    synthetic_data.generate_synthetic_data()
    synthetic_data.save_output_data()

    # Zip the result
   
    with zipfile.ZipFile("DATA/output/" + "Synt:" + filename, 'w') as zip_ref:
        for (_, _, filenames) in os.walk("DATA/output/tmp/" + "Synt:" + filename.split(".")[0]):
            for file_name in filenames:
                zip_ref.write("DATA/output/tmp/" + "Synt:" + filename.split(".")[0] + "/" + file_name, file_name)

    # Delete the temporary folder
    shutil.rmtree("DATA/output/tmp/" + "Synt:" + filename.split(".")[0])
    shutil.rmtree("DATA/input/tmp/" + filename.split(".")[0])

    # Load the result into the database
    db = Database()
    db.load_input_data(filename, description, input_openess, external_link)
    db.load_output_data("Synt:" + filename, base_dataset_availability=input_openess, description=description)

    # Delete the input dataset
    os.remove("DATA/input/" + filename)
    # Delete the output dataset
    os.remove("DATA/output/" + "Synt:" + filename)

    