from uwconnect_core.main.model.hobbies import *
from uwconnect_core.main.service.utils import get_file_path

def load_hobbies():
    hobbies = None
    with open(get_file_path("hobbies.txt")) as f:
        hobbies = f.read().strip().split('\n')

    Hobbies.drop_collection()
    hobbies = Hobbies(hobbies=hobbies)
    hobbies.save()
