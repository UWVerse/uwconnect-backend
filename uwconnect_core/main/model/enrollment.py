from mongoengine import *


class Enrollment(Document):
    faculty = ListField(StringField())
    program = ListField(StringField())
    course = ListField(StringField())
