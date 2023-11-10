from flask import render_template, Response, abort

from . import main_blueprint

from bs4 import BeautifulSoup
import requests

def scrapeResearchCenters():
    url = "https://research.rpi.edu/research-centers"
    
    payload = []
    
    page = requests.get(url)
    
    if (page.status_code != 200): # Safety check for a successful response
        return "Error: " + str(page.status_code)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    images = soup.find_all('img')
    links = soup.find_all('a')
    
    titles = []
    
    for link in links:
        valid = link.get('href') is not None and link.get('href').startswith('/research-centers/') and link.get_text().strip() != ""
        if valid:
            titles.append(link.get_text())
    
    print("Images: ")
    for image in images:
        if image.get('src').startswith('/sites/default/files/styles/research_') == False:
            images.remove(image)
        else:
            None
            
    if (len(images) != len(titles)):
        return "Error: Length of images and titles do not match"
    
    for title,image in zip(titles,images):
        payload.append(
            {
                "title": title,
                "image": "https://research.rpi.edu/research-centers" + image.get('src'),
            }
        )
    
    return payload


@main_blueprint.route("/")
def index():
    return render_template("index.html")


@main_blueprint.route("/positions")
def positions():
    return render_template("positions.html")


@main_blueprint.route("/profile/<string:rcs_id>")
def profile(rcs_id: str):
    return render_template("profile.html")


@main_blueprint.route("/department/<string:department>")
def department(department: str):
    return render_template("department.html")


@main_blueprint.route("/discover")
def discover():
    return render_template("discover.html")

@main_blueprint.route("/discover/researchCenters")
def discover_research_centers():
    centers = scrapeResearchCenters()
    return render_template("discover_research_centers.html", researchCenters=centers)

@main_blueprint.route("/discover/researchCenters/<string:center_name>")
def display_research_center():
    return render_template("research_center.html")


@main_blueprint.route("/professor/<string:rcs_id>")
def professor(rcs_id: str):
    # test code until database code is added
    if "bob" == rcs_id:
        return render_template("professor.html")
    abort(500)


@main_blueprint.route("/create_post")
def create_post():
    return render_template("posting.html")

@main_blueprint.route("/report_bug")
def report_bug():
    return render_template("report_bug.html")


@main_blueprint.route("/login")
def login():
    return render_template("sign_in.html")

@main_blueprint.route("/basic_information")
def basic_information():
    return render_template("URP_Basic_Information_Page.html")
