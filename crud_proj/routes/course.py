"""Routes for the course resource.
"""

from run import app
from flask import jsonify
from flask import request

from run import db
from database import Course
from database import insertCoursesIntoDatabase
from database import getCourseById
from database import getCoursesByIds
from database import coursesCount
from database import containWordInTitle
from database import insertCourseIntoDatabase
from database import updateCourseById
from database import deleteCourseById
import data


@app.route("/insertData", methods=['GET'])
def insertData():
    Course()
    db.create_all()
    courses = data.load_data()
    res = insertCoursesIntoDatabase(courses)
    return jsonify(res)


@app.route("/course/<int:id>", methods=['GET'])
def get_course(id):
    """Get a course by id.

    :param int id: The record id.
    :return: A single course (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------   
    1. Bonus points for not using a linear scan on your data structure.
    """
    # YOUR CODE HERE
    course = getCourseById(id)
    if not course:
        return jsonify({"message": "course {} does not exist".format(id)}), 404
    return jsonify(course), 200


@app.route("/course", methods=['GET'])
def get_courses():
    """Get a page of courses, optionally filtered by title words (a list of
    words separated by commas".

    Query parameters: page-number, page-size, title-words
    If not present, we use defaults of page-number=1, page-size=10

    :return: A page of courses (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    ------------------------------------------------------------------------- 
    1. Bonus points for not using a linear scan, on your data structure, if
       title-words is supplied
    2. Bonus points for returning resulted sorted by the number of words which
       matched, if title-words is supplied.
    3. Bonus points for including performance data on the API, in terms of
       requests/second.
    """
    # YOUR CODE HERE
    titleWord = request.args.get('title-word')
    pageNumber = int(request.args.get('page-number')) if request.args.get('page-number') else 1
    pageSize = int(request.args.get('page-size')) if request.args.get('page-size') else 10
    totalNoCourses = coursesCount()
    result = {"data": [],
              "metadata": {
                  "page_count": totalNoCourses // pageSize,
                  "page_size": pageSize,
                  "page_number": pageNumber,
                  "record_count": totalNoCourses,
              }}

    if not titleWord:
        start = pageSize * (pageNumber - 1) + 1
        end = start + pageSize
        result["data"] = getCoursesByIds(start, end)
    else:
        pass
        wordList = titleWord.split(',')
        for word in wordList:
            result["data"].append(containWordInTitle(word))

    return jsonify(result), 200


@app.route("/course", methods=['POST'])
def create_course():
    """Create a course.
    :return: The course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the POST body fields
    """
    #
    inputDetails = request.get_json()
    description = inputDetails.get('description')
    image_path = inputDetails.get('image_path')
    on_discount = inputDetails.get('on_discount')
    price = inputDetails.get('price')
    title = inputDetails.get("title")
    discount_price = inputDetails.get('discount_price')

    if not title or not price or not discount_price or not description or on_discount is None:
        return jsonify({"message": "Enter all required the fields"}), 406

    result = insertCourseIntoDatabase(
        {"description": description, "image_path": image_path, "on_discount": on_discount, "price": price,
         "title": title, "discount_price": discount_price})
    if not result:
        return jsonify({"Error": "Something went wrong"}), 500
    else:
        return jsonify({"data": result}), 201


@app.route("/course/<int:id>", methods=['PUT'])
def update_course(id):
    """Update a a course.
    :param int id: The record id.
    :return: The updated course object (see the challenge notes for examples)
    :rtype: object
    """

    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    1. Bonus points for validating the PUT body fields, including checking
       against the id in the URL

    """
    # YOUR CODE HERE
    course = getCourseById(id)
    if not course:
        return jsonify({"message": "The id does match payload"}), 400

    inputDetails = request.get_json()
    description = inputDetails.get('description') if inputDetails.get('description') else None
    image_path = inputDetails.get('image_path') if inputDetails.get('image_path') else None
    on_discount = inputDetails.get('on_discount') if inputDetails.get('on_discount') else None
    price = inputDetails.get('price') if inputDetails.get('price') else None
    title = inputDetails.get("title") if inputDetails.get("title") else None
    discount_price = inputDetails.get('discount_price') if inputDetails.get('discount_price') else None

    result = updateCourseById(id, description, image_path, on_discount, price, title, discount_price)

    if not result:
        return jsonify({"Error": "Something went wrong"}), 500
    else:
        return jsonify({"data": result}), 200


@app.route("/course/<int:id>", methods=['DELETE'])
def delete_course(id):
    """Delete a course
    :return: A confirmation message (see the challenge notes for examples)
    """
    """
    -------------------------------------------------------------------------
    Challenge notes:
    -------------------------------------------------------------------------
    None
    """
    # YOUR CODE HERE
    course = getCourseById(id)
    if not course:
        return jsonify({"message": "Course {} does not exist".format(id)}), 404

    isDeleted = deleteCourseById(id)
    if isDeleted:
        return jsonify({"message": "The specified course was deleted"}), 200
    else:
        return jsonify({"Error": "Something went wrong"}), 500
