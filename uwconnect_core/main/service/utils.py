import json
import os
import omegaconf
from bson.json_util import loads, dumps

def document_to_dict(doc):
    data = json.loads(doc.to_json())
    # Convert $date value to datetime object
    if "date_joined" in data:
        data['date_joined'] = loads(dumps(data['date_joined']))
    return data

def document_to_dict_batch(queryset):
    return [document_to_dict(doc) for doc in queryset]


def get_file_path(filename):
    """
    search file across whole repo and return abspath
    """
    for root, dirs, files in os.walk(r'.'):
        for name in files:
            if name == filename:
                return os.path.abspath(os.path.join(root, name))
    raise FileNotFoundError(filename, "not found.")


def get_omega_config():
    """
    Load omega_config that contain score weighting for recommendation system
    """
    omega_config = get_file_path("matching_weights.yml")
    omega_config = omegaconf.OmegaConf.load(omega_config)
    return omega_config