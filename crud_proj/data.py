"""Routines associated with the application data.
"""
import json


def load_data():
    """Load the data from the json file.
    """
    file = open("json/course.json")
    courses = json.load(file)
    # print(courses)
    return courses
