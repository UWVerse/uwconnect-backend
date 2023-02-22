from mongoengine import *


    
def validate_email_whitelist(domain_whitelist):
    def func(email):
        user_part, domain_part = email.rsplit("@", 1)
        if domain_part not in domain_whitelist:
            raise ValidationError
    return func

class UserCredential(Document):
    email = EmailField(required="true", validation=validate_email_whitelist(domain_whitelist=["uwaterloo.ca"]))
    password = StringField(required=True)
    def validate_profile(self):
        User.email.validation(self.email)

class User(Document):
    email = EmailField(required="true", validation=validate_email_whitelist(domain_whitelist=["uwaterloo.ca"]))

    username = StringField(regex="[A-Za-z0-9_ ]+", min_length=6, max_length=32)
    gender = StringField(max_length=16)
    faculty = StringField()
    program = StringField()
    year = IntField()
    courses = ListField(StringField(regex="[A-Z]+[0-9]+[A-Z]*"))
    tags = ListField(StringField())
    bio = StringField(max_length=1024)


    def validate_profile(self):
        User.email.validation(self.email)
        User.username.validate(self.username)
        User.gender.validate(self.gender)
        User.faculty.validate(self.faculty)
        User.program.validate(self.program)
        User.year.validate(self.year)
        User.courses.validate(self.courses)
        User.tags.validate(self.tags)
        User.bio.validate(self.bio)

