from mongoengine import Document, StringField, EmailField


class User(Document):
    email = EmailField(domain_whitelist=["@uwaterloo.ca"])
    password = StringField(required=True)

