
from uwconnect_core.main.model.user import User
from mongoengine import *
from typing import Union, List
from utils import get_omega_config

def get_recommendation(user: User, other_users: List[User], list_length: int, score_threshold: int):
    """
    Develop Recommendation algorithm. 
    The Recommendation API should return a suggested user list base on the current user profile and user's preference.
    param:
        user: current logged user
        other_users: other users in the db
        list_length: 
        score_threshold: 
    return:
    The recommendation user list should contains user name, user profile, user email.
    """
    config = get_omega_config()

    # Naive algorithm, need a rework later
    list_user = []
    for other_user in other_users:
        if (score_algorithm(user, other_user, config.weight_params) > score_threshold):
            list_user.append(other_user)

        if len(list_user) > list_length:
            break

    return list_user

def score_algorithm(user1: User, user2: User, weight_params) -> int:
    """
    Score matching algorithm for Recommendation algorithm.
    param:
    user1, user2 : Users
    weight_params : dict from omegaconf
    return:
    A score between 2 users.
    """
    score = 0
    score += get_score(user1.gender, user2.gender, weight_params.gender)
    score += get_score(user1.faculty, user2.faculty, weight_params.faculty)
    score += get_score(user1.program, user2.program, weight_params.program)
    score += get_score(user1.year, user2.year, weight_params.year)
    score += get_score(user1.courses, user2.courses, weight_params.courses)
    score += get_score(user1.tags, user2.tags, weight_params.tags)
    
    return score

def get_score(item1: Union[int, float, str, list], item2: Union[int, float, str, list], weight: int) -> int:
    """
    Compute score for a specific item.
    For list, we find the common items in two list and return the score according to number of commons.
    return:

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
