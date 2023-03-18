from mongoengine import *
from datetime import datetime

    
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
    """
    User attributes
        image_url: url to profile image
        profile_visible: Only profile_visible=True can be matched, otherwise no.
        tags: list of hobbies
        year: range between 1 to 5
    """
    email = EmailField(required="true", validation=validate_email_whitelist(domain_whitelist=["uwaterloo.ca"]))
    #username = StringField(regex="[A-Za-z0-9_ ]+", min_length=6, max_length=32)
    username = StringField(regex="[A-Za-z0-9_ ]+")
    first_name = StringField(regex="[A-Za-z ]+")
    last_name = StringField(regex="[A-Za-z ]+")
    gender = StringField(max_length=16)
    image_url = StringField()
    faculty = StringField()
    program = StringField()
    year = IntField()
    courses = ListField(StringField())
    tags = ListField(StringField())
    #bio = StringField(max_length=1024)
    date_joined = DateTimeField(default=datetime.now)
    profile_visible = BooleanField()


    def validate_profile(self):
        User.email.validation(self.email)
        User.username.validate(self.username)
        User.first_name.validate(self.first_name)
        User.last_name.validate(self.last_name)
        User.gender.validate(self.gender)
        User.image_url.validate(self.image_url)
        User.faculty.validate(self.faculty)
        User.program.validate(self.program)
        User.year.validate(self.year)
        User.courses.validate(self.courses)
        User.tags.validate(self.tags)
        #User.bio.validate(self.bio)
        User.date_joined.validate(self.date_joined)
        User.profile_visible.validate(self.profile_visible)
        
    def get_uid(self):
        return self.email.split('@')[0]

    
