import json
import os

def document_to_dict(doc):
    return json.loads(doc.to_json())


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