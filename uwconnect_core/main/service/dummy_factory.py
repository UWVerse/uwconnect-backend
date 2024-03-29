from uwconnect_core.main.model.user import User, UserCredential
from uwconnect_core.main.model.enrollment import Enrollment
from uwconnect_core.main.model.hobbies import Hobbies

from datetime import datetime
import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger
import random
import string

"""
def get_list_hobbies():
    hobbies = Hobbies.objects().first()
    return list(hobbies['hobbies'])

def get_list_enrollment():
    enroll = Enrollment.objects().first()
    faculty = list(enroll['faculty'])
    program = list(enroll['program'])
    courses = list(enroll['course'])
    return faculty, program, courses
"""

def get_list_hobbies():
    hobbies = ['Tennis', 'Singing', 'Dancing', 'Acting', 'Stand-up comedy', 'Cooking', 'Baking', 'Basketball', 'Soccer', 'Yoga', 'Meditation', 'Traveling']
    return hobbies

def get_list_enrollment():
    faculty = ['Arts','Engineering','Environment','Health','Mathematics','Science']
    program = ['Combinatorics and Optimization','Communication Studies','Computational Mathematics','Computer Engineering','Computer Science','Computing and Financial Management','Data Science']
    courses = ['ECE650', 'ECE651', 'ECE653', 'ECE657', 'CS686', 'CS666', 'CS686', 'CO663', 'ECE656', 'ECE658']
    return faculty, program, courses

list_hobbies = get_list_hobbies()
list_faculty, list_program, list_courses = get_list_enrollment()

class RandomUserCredentialFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = UserCredential
        
    email = factory.Faker('email')
    password = factory.Faker("password", length=10)

class RandomUserFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(lambda o: f'{o.first_name.lower()}{o.last_name.lower()}{random.randint(0,10)}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@uwaterloo.ca')
    date_joined = factory.LazyFunction(datetime.now)
    image_url = factory.Faker('image_url')
    faculty = factory.LazyFunction(lambda: random.choice(list_faculty))
    program = factory.LazyFunction(lambda: random.choice(list_program))
    courses = factory.LazyFunction(lambda: random.sample(list_courses, k=random.randint(1, 5)))
    tags = factory.LazyFunction(lambda: random.sample(list_hobbies, k=random.randint(1, 10)))
    year = factory.LazyAttribute(lambda _: FuzzyInteger(1, 5).fuzz())
    #bio = factory.Faker('sentence')
    profile_visible = factory.Faker('boolean')
    gender = factory.LazyFunction(lambda: random.choice(['male', 'female', 'other']))

    @factory.post_generation
    def print_user(obj, create, extracted, **kwargs):
        #print(obj.email)
        pass