from uwconnect_core.main.model.enrollment import *
from uwconnect_core.main.service.utils import get_file_path
import requests
import json

def get_courses(api_key):
    headers = { "x-api-key": api_key }
    response = requests.get('https://openapi.data.uwaterloo.ca/v3/Courses/1231', headers=headers)
    response_body = response.text

    # Convert response body from JSON to dictionary
    response_dict = json.loads(response_body)

    courses = []
    for i in response_dict:
        courses.append(i["subjectCode"] + i["catalogNumber"])
    
    return courses
        

def load_enrollment(api_key):
    faculties = None
    programs = None
    with open(get_file_path("program.txt")) as f:
        programs = f.read().strip().split('\n')

    with open(get_file_path("faculty.txt")) as f:
        faculties = f.read().strip().split('\n')

    courses = get_courses(api_key)

    Enrollment.drop_collection()
    enrollment = Enrollment(faculty=faculties, program=programs, course=courses)
    enrollment.save()
