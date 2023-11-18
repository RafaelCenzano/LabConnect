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



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    