import string
import datetime
import uuid
from labconnect import db, create_app
from labconnect.models import *
from sqlalchemy.orm import contains_eager

app = create_app()



# helper functions
def generate_random_id():
    random_id = str(uuid.uuid4())
    return random_id

def findValidID():
    while True:
        id = generate_random_id()
        if not Opportunities.query.filter_by(id=id).first():
            return id

#filter to database

# FILTER DEPARTMENTS

def allFilters(filters):
    
    #TODO discuss how to filter by names and try to break this function down
    
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
        .join(Opportunities.application_due)
        .join(Opportunities.has_credit_comp)
        .join(Opportunities.has_upfront_pay_comp)
        .join(Opportunities.has_salary_comp)
        .filter(len(courses) == 0 or Courses.course_name.in_(courses))
        .filter(len(years) == 0 or ClassYears.class_year.in_(years))
        .filter(len(departments == 0) or Majors.major_name.in_(departments))
        .filter(len(semesters) == 0 or Semesters.season.in_(semesters))
        .filter(CreditCompInfo.number_of_credits >= filters["credit_comp"])
        .filter(HasUpfrontPayComp.usd >= filters["upfrontPay"])
        .filter(SalaryCompInfo.usd_per_hour >= filters["salary"])
        .options(
            contains_eager(Opportunities.recommends_courses),
            contains_eager(Opportunities.recommends_class_years),
            contains_eager(Opportunities.recommends_majors),
            contains_eager(Opportunities.active_semesters),
            contains_eager(Opportunities.application_due),
            contains_eager(Opportunities.has_credit_comp),
            contains_eager(Opportunities.has_upfront_pay_comp),
            contains_eager(Opportunities.has_salary_comp)
        )
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

def getLabRunner(rcs_id):
    stmt = (
        db.select(LabRunner).where(LabRunner.rcs_id == rcs_id)
    )
    
    result = db.session.execute(stmt).fetchall()
    return result

def getDepartment(department_name):
    stmt = (
        db.select(RPIDepartments).where(RPIDepartments.name == department_name)
    )
    
    result = db.session.execute(stmt).first()
    return result

def getCourses(course_names):
    stmt = (
        db.select(Courses)
        .filter(Courses.course_name.in_(course_names))
    )
    
    return db.session.execute(stmt).fetchall()

def getSemesters(semesters):
    stmt = (
        db.select(Semesters)
        .filter(len(semesters) == 0 or Semesters.season.in_(semesters))
    )
            
    return db.execute(stmt).fetchall()

def getYears(years):
    stmt = (
        db.select(ClassYears)
        .filter(len(years) == 0 or ClassYears.class_year.in_(years))
    )
            
    return db.execute(stmt).fetchall()

def getMajors(majors):
    stmt = (
        db.select(Majors)
        .filter(len(majors) == 0 or Majors.major_name.in_(majors))
    )
            
    return db.execute(stmt).fetchall()

def getDeadline(deadline):
    stmt = (
        db.select(ApplicationDueDates)
        .filter(ApplicationDueDates.date == deadline)
    )
    
    result = db.execute(stmt).fetchall()
    
    if result == []:
        new_deadline = ApplicationDueDates()
        new_deadline.date = datetime.datetime.now()
        return new_deadline
    else:
        return result

def getSalaryCompensation(salary_compensation):
    stmt = (
        db.select(SalaryCompInfo)
        .filter(SalaryCompInfo.usd_per_hour == salary_compensation)
    )
    
    result = db.execute(stmt).fetchall()
    
    if result == []:
        new_salary_compensation = SalaryCompInfo()
        new_salary_compensation.usd_per_hour = salary_compensation
        return new_salary_compensation
    else:
        return result

def getUpfrontCompensation(upfront_compensation):
    stmt = (
        db.select(UpfrontPayCompInfo)
        .filter(UpfrontPayCompInfo.usd == upfront_compensation)
    )
    
    result = db.execute(stmt).fetchall()
    
    if (result == []):
        new_upfront_compensation = UpfrontPayCompInfo()
        new_upfront_compensation.usd = upfront_compensation
        return new_upfront_compensation
    else:
        return result

def getCreditCompensation(courseCode, credit_compensation):
    stmt = (
        db.select(CreditCompInfo)
        .filter(CreditCompInfo.number_of_credits == credit_compensation
                or CreditCompInfo.course_code == courseCode)
    )
    
    result = db.execute(stmt).fetchall()
    
    if (result == []):
        new_credit_compensation = CreditCompInfo()
        new_credit_compensation.number_of_credits = credit_compensation
        new_credit_compensation.course_code = courseCode
        return new_credit_compensation
    else:
        return result



# ADD TO DATABASE
def addUser(rcsid: str, name: str, department_name: str):
    # Create a new LabRunner
    user = getLabRunner(rcsid)
    
    if user:
        return 
    
    user = LabRunner(rcs_id=rcsid, name=name)
    
    db.session.add(user)
    db.session.commit()

    # Query the RPIDepartments to find the department by name
    department = getDepartment(department_name)

    # Check if the department exists
    if department:
        # Add the department to the LabRunner's departments
        user = getLabRunner(rcsid)
        user.rpi_departments.append(department)

        # Add the LabRunner to the session and commit the changes
        db.session.add(user)
        db.session.commit()
        print(f"User {name} added to department {department_name}")
    else:
        print(f"Department {department_name} does not exist. User not added.")

    

#TODO: ask team about this and fill in the missing tables
def addOpportunity(rcsid:string, name:string, description:string, active_status:bool, recommended_experience:string, courses, majors, semesters, upfrontPay, salary, courseCode, creditComp,  deadline):
    
    author = getLabRunner(rcsid)
    majors = getMajors(majors)
    semesters = getSemesters(semesters)
    courses = getCourses(courses)
    dueDate = getDeadline(deadline)
    salary = getSalaryCompensation(salary)
    upfrontPay = getUpfrontCompensation(upfrontPay)
    credits = getCreditCompensation(courseCode, creditComp)
    
    if not author:
        print(f"User {rcsid} does not exist. Opportunity not added.")
        return
    
    author = author[0]
    
    # Create a new Opportunity
    id = findValidID()

    opportunity = Opportunities()
    
    # direct variables
    opportunity.id = id
    opportunity.name = name
    opportunity.description = description
    opportunity.active_status = active_status
    opportunity.recommended_experience = recommended_experience
    
    # relationships
    opportunity.lab_runners.append(author)
    opportunity.recommends_majors.append(majors)
    opportunity.recommends_courses.append(courses)
    opportunity.active_semesters.append(semesters)
    opportunity.application_due.append(dueDate)
    opportunity.has_salary_comp.append(salary)
    opportunity.has_upfront_pay_comp.append(upfrontPay)
    opportunity.has_credit_comp.append(credits)
    
    db.session.add(opportunity)
    
    author.promoted_opportunities.append(opportunity)
    
    db.session.commit()
    
# add a new contact link to the database
def addContactLink(rcsid:string, link:string, type:string):
    
    # find the labrunner
    labrunner = getLabRunner(rcsid)
    
    # if the labrunner doesn't exist, return
    if not labrunner:
        print(f"User {rcsid} does not exist. Link not added.")
        return
    
    # create a new contact link
    contact_link = ContactLinks()
    contact_link.link = link
    contact_link.type = type
    
    # add the contact link to the labrunner
    labrunner[0].contact_links.append(contact_link)
    
    #commit the changes
    db.session.commit()
    

# testing to see if everything works  
    
with app.app_context():
    # add a user to the database
    a = getLabRunner("led")
    print(a)
    
    addUser("wowza", "Liam Dwyer", "Computer Science")
    a = getLabRunner("wowza")
    print(a)
    
    # write a suite of tests for my functions
    # add a new opportunity to the database
    addOpportunity("wowza", "test", "test", True, "test", ["CSCI 1100"], ["Computer Science"], ["Fall"], 0, 0, "CSCI 1100", 0, datetime.datetime.now())
    a = Opportunities.query.all()
    print(a)
    
    # add a new contact link to the database
    addContactLink("wowza", "www.google.com", "test")
    a = ContactLinks.query.all()
    print(a)
    
    # filter by courses
    a = filterByCourses(["CSCI 1100"])
    print(a)
    
    # filter by years
    a = filterByYear(["2021"])
    print(a)
    
    # filter by departments
    a = filterByDeparments(["Computer Science"])
    print(a)
    
    # filter by semesters
    a = filterBySemester(["Fall"])
    print(a)
    
    # filter by all
    a = allFilters({"courses": ["CSCI 1100"], "departments": ["Computer Science"], "semesters": ["Fall"], "years": ["2021"], "credit_comp": 0, "upfrontPay": 0, "salary": 0})
    print(a)
    
    # get a labrunner
    a = getLabRunner("wowza")
    print(a)
    
    # get a department
    a = getDepartment("Computer Science")
    print(a)
    
    # get a course
    a = getCourses(["CSCI 1100"])
    print(a)
    
    # get a semester
    a = getSemesters(["Fall"])
    print(a)
    
    # get a year
    a = getYears(["2021"])
    print(a)
    
    # get a major
    a = getMajors(["Computer Science"])
    print(a)
    
    # get a deadline
    a = getDeadline(datetime.datetime.now())
    print(a)
    
    # get a salary compensation
    
    a = getSalaryCompensation(0)
    print(a)
    
    # get an upfront compensation
    a = getUpfrontCompensation(0)
    print(a)
    
    # get a credit compensation
    a = getCreditCompensation("CSCI 1100", 0)
    print(a)
    
    # get a contact link
    a = ContactLinks.query.all()
    print(a)
    
    # get an opportunity
    a = Opportunities.query.all()
    print(a)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    