import string
import uuid
from labconnect import db
from labconnect.models import *
from sqlalchemy.orm import contains_eager

# helper functions
def generate_random_id():
    random_id = str(uuid.uuid4())
    return random_id

#filter to database

# FILTER DEPARTMENTS

def allFilters(filters):
    courses = filters["courses"]
    departments = filters["departments"]
    semesters = filters["semesters"]
    years = filters["years"]
    stmt = (
        db.select(Opportunities)
        .join(Opportunities.recommends_courses)
        .join(Opportunities.recommends_class_years)
        .join(Opportunities.recommends_majors)
        .join(Opportunities.active_semesters)
        .options(
            contains_eager(Opportunities.recommends_courses),
            contains_eager(Opportunities.recommends_class_years),
            contains_eager(Opportunities.recommends_majors),
            contains_eager(Opportunities.active_semesters),
        )
        .filter(Courses.course_name.in_(courses))
        .filter(ClassYears.class_year.in_(years))
        .filter(Majors.major_name.in_(departments))
        .filter(Semesters.season.in_(semesters))
    )
    
    result = db.session.execute(stmt)
    results = result.fetchall()
    return results

def filterByCourses(courses):
    stmt = (
        db.select(Opportunities)
        .join(Opportunities.recommends_courses)
        .options(
            contains_eager(Opportunities.recommends_courses),
        )
        .join(Opportunities.recommends_courses)
        .filter(Courses.course_code.in_(courses))
    )
    
    result = db.session.execute(stmt)
    filtered_opportunities = result.fetchall()
    return filtered_opportunities

# or relationship between years
def filterByYear(years):
    stmt = (
        db.select(Opportunities)
        .join(Opportunities.recommends_class_years)
        .options(
            contains_eager(Opportunities.recommends_class_years),
        )
        .join(Opportunities.recommends_class_years)
        .filter(ClassYears.class_year.in_(years))
    )
    
    result = db.session.execute(stmt)
    filtered_opportunities = result.fetchall()
    return filtered_opportunities

# OR relationship between departments
def filterByDeparments(departments): 
    stmt = (
        db.select(Opportunities)
        .join(Opportunities.recommends_majors)
        .options(
            contains_eager(Opportunities.recommends_majors),
        )
        .join(Opportunities.recommends_majors)
        .filter(Majors.major_name.in_(departments))
    )
    
    result = db.session.execute(stmt)
    filtered_opportunities = result.fetchall()
    return filtered_opportunities


# OR relationship between semesters
def filterBySemester(semesters):
    stmt = (
        db.select(Opportunities)
        .join(Opportunities.active_semesters)
        .options(
            contains_eager(Opportunities.active_semesters),
        )
        .join(Opportunities.recommends_majors)
        .filter(Semesters.season.in_(semesters))
    )
    result = db.session.execute(stmt)
    filtered_opportunities = result.fetchall()
    return filtered_opportunities


# FILTER LABRUNNERS
def filterLabRunnerByDepartment(department_name):
    stmt = (
        db.select(LabRunner)
        .join(LabRunner.rpi_departments)
        .options(
            contains_eager(LabRunner.rpi_departments),
        )
        .join(LabRunner.rpi_departments)
        .filter(RPIDepartments.name.in_(department_name))
    )
    
    result = db.session.execute(stmt)
    filtered_labrunners = result.fetchall()
    return filtered_labrunners


def filterLabRunnerByName(name):
    stmt = (
        db.select(LabRunner)
        .filter(LabRunner.name.in_(name))
    )
    
    result = db.session.execute(stmt)
    filtered_labrunners = result.fetchall()
    return filtered_labrunners


def filterLabRunnerByRCSID(rcs_id):
    stmt = (
        db.select(LabRunner)
        .filter(LabRunner.rcs_id.in_(rcs_id))
    )
    
    result = db.session.execute(stmt)
    filtered_labrunners = result.fetchall()
    return filtered_labrunners


# ADD TO DATABASE

def addUser(rcsid: str, name: str, department_name: str):
    # Create a new LabRunner
    user = LabRunner(rcs_id=rcsid, name=name)

    # Query the RPIDepartments to find the department by name
    department = RPIDepartments.query.filter_by(name=department_name).first()

    # Check if the department exists
    if department:
        # Add the department to the LabRunner's departments
        user.rpi_departments.append(department)

        # Add the LabRunner to the session and commit the changes
        db.session.add(user)
        db.session.commit()
        print(f"User {name} added to department {department_name}")
    else:
        print(f"Department {department_name} does not exist. User not added.")

# TODO: ask team how to handle collisions between ids

def getCourses(course_names):
    courses = []
    for course_name in course_names:
        course = Courses.query.filter_by(name=course_name).first()
        if not course:
            # Create a new course if it doesn't exist
            course = Courses(name=course_name)
            db.session.add(course)
        courses.append(course)

    db.session.commit()
    return courses

def getSemesters(semesters):
    filtered_semesters = []
    for name in semesters:
        semester = Semesters.query.filter_by(name=name).first()
        if not semester:
            continue
        else:
            filtered_semesters.append(semester)
            
    return filtered_semesters

def getYears(years):
    filtered_years = []
    for year in years:
        year = ClassYears.query.filter_by(name=year).first()
        if not year:
            continue
        else:
            filtered_years.append(year)
            
    return filtered_years

def getMajors(majors):
    filtered_majors = []
    for major in majors:
        major = Majors.query.filter_by(name=major).first()
        if not major:
            continue
        else:
            filtered_majors.append(major)
            
    return filtered_majors

#TODO: ask team about this and fill in the missing tables
def addOpportunity(rcsid:string, name:string, description:string, active_status:bool, recommended_experience:string, courses, majors, semesters, deadline):
    
    author = filterLabRunnerByRCSID(rcsid)
    majors = getMajors(majors)
    semesters = getSemesters(semesters)
    courses = getCourses(courses)
    
    if not author:
        print(f"User {rcsid} does not exist. Opportunity not added.")
        return
    
    # Create a new Opportunity
    id = generate_random_id()
    opportunity = Opportunities()
    opportunity.id = id
    opportunity.name = name
    opportunity.description = description
    opportunity.active_status = active_status
    opportunity.recommended_experience = recommended_experience
    opportunity.lab_runners.append(author[0])
    opportunity.recommends_majors = majors
    opportunity.recommends_courses = courses
    opportunity.active_semesters = semesters
    opportunity.application_due = deadline
    
    db.session.add(opportunity)
    db.session.commit()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    