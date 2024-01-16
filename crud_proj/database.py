from run import db
from datetime import datetime


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_updated = db.Column(db.DateTime, default=datetime.now)
    description = db.Column(db.String(255))
    image_path = db.Column(db.String(100))
    on_discount = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    discount_price = db.Column(db.Integer, nullable=False)


# Insert one course into database
def insertCourseIntoDatabase(course):
    try:
        course = Course(description=course["description"], image_path=course["image_path"],
                        on_discount=course["on_discount"],
                        price=course["price"], title=course["title"], discount_price=course["discount_price"])
        db.session.add(course)
        db.session.commit()
        return resToDict(course)
    except Exception as e:
        print(str(e))
        return []


# Insert more than one course into database
def insertCoursesIntoDatabase(courses):
    for i in range(len(courses)):
        if not insertCourseIntoDatabase(courses[i]):
            return False
    return True


def getAllCourse():
    coursesObj = Course.query.all()
    # print(courses)
    courses = []
    for course in coursesObj:
        courses.append(resToDict(course))
    return courses


def coursesCount():
    return int(Course.query.count())


def getCourseById(id):
    course = Course.query.get(id)
    if not course:
        return []
    # print(course)
    return resToDict(course)


def getCoursesByIds(startId, endId):
    coursesObj = Course.query.filter(Course.id.between(startId, endId))
    courses = multiResToDict(coursesObj, endId - startId)
    return courses


def containWordInTitle(word):
    coursesObj = Course.query.filter(Course.title.like("%" + word + "%")).all()
    courses = multiResToDict(coursesObj, len(coursesObj))
    # print(courses)
    return courses


def updateCourseById(id, description, image_path, on_discount, price, title, discount_price):
    try:
        course = Course.query.get(id)
        course.date_updated = datetime.now()
        course.description = description if description else course.description
        course.image_path = image_path if image_path else course.image_path
        course.on_discount = on_discount if on_discount else course.on_discount
        course.price = price if price else course.price
        course.title = title if title else course.title
        course.discount_price = discount_price if discount_price else course.discount_price
        db.session.commit()
        return resToDict(course)
    except Exception as e:
        print(str(e))
        return []


def deleteCourseById(id):
    try:
        Course.query.filter_by(id=id).delete()
        db.session.commit()
        return True
    except Exception as e:
        print(str(e))
        return False


# One responce to dict
def resToDict(response):
    result = {}
    result["id"] = int(response.id)
    result["date_created"] = str(response.date_created)
    result["date_updated"] = str(response.date_updated)
    result["description"] = str(response.description)
    result["discount_price"] = int(response.discount_price)
    result["image_path"] = str(response.image_path)
    result["on_discount"] = bool(response.on_discount)
    result["price"] = int(response.price)
    result["title"] = str(response.title)
    return result


# Multiple responsec to dict
def multiResToDict(responses, noOfResp):
    results = []
    for i in range(noOfResp):
        results.append(resToDict(responses[i]))
    return results
