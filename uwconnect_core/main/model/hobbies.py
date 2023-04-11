from mongoengine import *


class Hobbies(Document):
    hobbies = ListField(StringField())
