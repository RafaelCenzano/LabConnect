from flask import abort, render_template

from . import main_blueprint

from labconnect import db
from labconnect.models import *
from sqlalchemy.orm import contains_eager



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

def filterByYear(result,years):
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


# Apply Department filters
def filterByDeparments(result,departments):
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


def filterBySemester(result,semesters):
    # stmt = db.select(Opportunities)
    # result = db.session.execute(stmt)
    # allOpportunities = result.fetchall()
    
    # valid_semesters = ["summer", "winter", "spring"]

# Assuming you have a session object named 'db.session'
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
    

# result = db.session.execute(stmt)
# filtered_opportunities = result.fetchall()
      

@main_blueprint.route("/")
def index():
    return render_template("index.html")


@main_blueprint.route("/opportunities")
def positions():
    return render_template("opportunitys.html")


@main_blueprint.route("/opportunity/<int:id>")
def opportunity(id: int):
    return render_template("opportunity_details.html")


@main_blueprint.route("/profile/<string:rcs_id>")
def profile(rcs_id: str):
    return render_template("profile.html")


@main_blueprint.route("/department/<string:department>")
def department(department: str):
    return render_template("department.html")


@main_blueprint.route("/discover")
def discover():
    return render_template("discover.html")


@main_blueprint.route("/professor/<string:rcs_id>")
def professor(rcs_id: str):
    # test code until database code is added
    if "bob" == rcs_id:
        return render_template("professor.html")
    abort(500)


@main_blueprint.route("/create_post")
def create_post():
    return render_template("posting.html")


@main_blueprint.route("/login")
def login():
    return render_template("sign_in.html")


@main_blueprint.route("/information")
@main_blueprint.route("/info")
def information():
    return render_template("URP_Basic_Information_Page.html")


@main_blueprint.route("/tips")
def tips():
    return render_template("tips_and_tricks.html")
