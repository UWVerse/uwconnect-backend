import json


def document_to_dict(doc):
    return json.loads(doc.to_json())


def document_to_dict_batch(queryset):
    return [document_to_dict(doc) for doc in queryset]