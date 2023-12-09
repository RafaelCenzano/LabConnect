from flask import abort, render_template

from . import main_blueprint

from labconnect import db, create_app
from labconnect.models import *
from sqlalchemy.orm import contains_eager
from sqlalchemy import *



# def allFilters(filters):
#     courses = filters["courses"]
#     departments = filters["departments"]
#     semesters = filters["semesters"]
#     years = filters["years"]
#     stmt = (
#         db.select(Opportunities)
#         .join(Opportunities.recommends_courses)
#         .join(Opportunities.recommends_class_years)
#         .join(Opportunities.recommends_majors)
#         .join(Opportunities.active_semesters)
#         .options(
#             contains_eager(Opportunities.recommends_courses),
#             contains_eager(Opportunities.recommends_class_years),
#             contains_eager(Opportunities.recommends_majors),
#             contains_eager(Opportunities.active_semesters),
#         )
#         .filter(Courses.course_name.in_(courses))
#         .filter(ClassYears.class_year.in_(years))
#         .filter(Majors.major_name.in_(departments))
#         .filter(Semesters.season.in_(semesters))
#     )
    
#     result = db.session.execute(stmt)
#     results = result.fetchall()
#     return results

# def filterByCourses(courses):
#     stmt = (
#         db.select(Opportunities)
#         .join(Opportunities.recommends_courses)
#         .options(
#             contains_eager(Opportunities.recommends_courses),
#         )
#         .join(Opportunities.recommends_courses)
#         .filter(Courses.course_code.in_(courses))
#     )
    
#     result = db.session.execute(stmt)
#     filtered_opportunities = result.fetchall()
#     return filtered_opportunities

# # or relationship between years
# def filterByYear(years):
#     stmt = (
#         db.select(Opportunities)
#         .join(Opportunities.recommends_class_years)
#         .options(
#             contains_eager(Opportunities.recommends_class_years),
#         )
#         .join(Opportunities.recommends_class_years)
#         .filter(ClassYears.class_year.in_(years))
#     )
    
#     result = db.session.execute(stmt)
#     filtered_opportunities = result.fetchall()
#     return filtered_opportunities


# # OR relationship between departments
# def filterByDeparments(departments): 
#     stmt = (
#         db.select(Opportunities)
#         .join(Opportunities.recommends_majors)
#         .options(
#             contains_eager(Opportunities.recommends_majors),
#         )
#         .join(Opportunities.recommends_majors)
#         .filter(Majors.major_name.in_(departments))
#     )
    
#     result = db.session.execute(stmt)
#     filtered_opportunities = result.fetchall()
#     return filtered_opportunities


# # OR relationship between semesters
# def filterBySemester(semesters):
#     stmt = (
#         db.select(Opportunities)
#         .join(Opportunities.active_semesters)
#         .options(
#             contains_eager(Opportunities.active_semesters),
#         )
#         .join(Opportunities.recommends_majors)
#         .filter(Semesters.season.in_(semesters))
#     )
#     result = db.session.execute(stmt)
#     filtered_opportunities = result.fetchall()
#     return filtered_opportunities
    
@main_blueprint.route("/dbtest")
def dbtest():
    a = testLabRunner("taluka")
    
    return db.session.execute(a).fetchall();     

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
