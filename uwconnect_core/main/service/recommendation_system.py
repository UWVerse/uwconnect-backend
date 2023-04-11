
from uwconnect_core.main.model.user import User
from mongoengine import *
from typing import Union, List
from uwconnect_core.main.service.utils import get_omega_config

def search_recommendation_db(user: User):
    """
    Search through the database with similar profile.
    We only search in the database that:
        any of the hobbies match
        any of the courses match
        program match
    """
    hobbies_to_match = user.tags
    courses_to_match = user.courses
    program = user.program
    email = user.email
    # Query the database for all records
    # Search only visible profiles, and must not be User himself/herself
    query = Q(profile_visible=True, email__ne=email)

    query &= Q(tags__in=hobbies_to_match) | Q(courses__in=courses_to_match) | Q(program=program)
    # ^ The __in operator is used in MongoDB queries to match any document that has a field whose value is contained in a given list of values.

    records = User.objects(query)
    return records

def get_recommendation(user: User, other_users: List[User], list_length: int, score_threshold: int):
    """
    Develop Recommendation algorithm. 
    The Recommendation API should return a suggested user list base on the current user profile and user's preference.
    param:
        user: current logged user
        other_users: other users in the db
        list_length: how many recommendations to be returned
        score_threshold: passing the threshold
    return:
    The recommendation user list should contains user name, user profile, user email.
    """
    config = get_omega_config()

    # Naive algorithm, need a rework later
    list_user = []
    for other_user in other_users:
        if (score_algorithm(user, other_user, config) > score_threshold):
            list_user.append(other_user)

        if len(list_user) >= list_length:
            break

    return list_user

def score_algorithm(user1: User, user2: User, config) -> int:
    """
    Score matching algorithm for Recommendation algorithm.
    param:
    user1, user2 : Users
    weight_params : dict from omegaconf
    return:
    A score between 2 users.
    """
    score = 0
    score += get_score(user1.gender, user2.gender, config.weight_params.gender)
    score += get_score(user1.faculty, user2.faculty, config.weight_params.faculty)
    score += get_score(user1.program, user2.program, config.weight_params.program)
    score += get_score(user1.year, user2.year, config.weight_params.year)
    score += get_score(user1.courses, user2.courses, config.weight_params.courses)
    score += get_score(user1.tags, user2.tags, config.weight_params.tags)
    
    return score

def get_score(item1: Union[int, float, str, list], item2: Union[int, float, str, list], weight: int) -> int:
    """
    Compute score for a specific item.
    For list, we find the common items in two list and return the score according to number of commons.
    return:
        score for that part
    """
    if isinstance(item1, str) and isinstance(item2, str):
        #"string"
        return weight if item1==item2 else 0
    elif isinstance(item1, (int, float)) and isinstance(item2, (int, float)):
        #"number"
        return weight if item1==item2 else 0
    elif isinstance(item1, list) and isinstance(item2, list):
        #"list"
        common_items = set(item1).intersection(set(item2)) #Convert the lists to sets and find the intersection
        return weight*len(common_items)
    else:
        return 0 # This mean user might not have initalized the setting
        #raise TypeError("The two item are not the same type")
