from bs4 import BeautifulSoup
import requests

resources = {
    "Center for Biotechnology and Interdisciplinary Studies (CBIS)": {
        "faculty": "https://biotech.rpi.edu/faculty",
    },
    "Center for Computational Innovations (CCI)":{
        "faculty:" "https://cci.rpi.edu/faculty",
    },
    "Center for Materials, Devices, and Integrated Systems (CMDIS)": {
        
    },
    "Experimental Media and Performing Arts Center (EMPAC)": {
        
    },
    "Institute for Data Exploration and Applications (IDEA)": {
        
    },
    "Institute for Energy, the Built Environment, and Smart Systems (EBESS)": {
        
    },
    "Center for Architecture Science and Ecology (CASE)": {
        
    },
    "Center for Automation Technologies and Systems (CATS)": {
        
    }, 
    "Center for Future Energy Systems (CFES)": {
        
    }, 
    "Center for Modeling, Simulation and Imaging in Medicine (CEMSIM)": {
        
    }, 
    "Cognitive and Immersive Systems Lab (CISL)": {
        
    },
    "Darrin Fresh Water Institute (DFWI)" : {
        
    }, 
    "Network Science and Technology Center (NeST)": {
        
    }
    
    
    
    
}

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
                "image": image.get('src'),
            }
        )
    
    return payload

def getProfessors(url):
    page = requests.get(url)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    
    links = soup.find_all('a')
    professorLinks = []
    
    for link in links:
        if (link.get('href') is not None and link.get('href').startswith('https://faculty.rpi.edu') and link.get_text().strip() != ""):
            professorLinks.append(link)
            
    payload = []
    
    for link in professorLinks:
        load = {}
        load["link"] = link.get('href')
        link = link.find_all('img')[0]
        load["name"] = link.get('alt')
        payload.append(load)
        
    print(payload)
    


    
    # for i, a in enumerate(soup.find_all('a')):
    #     if a.get('href') is not None and a.get('href').startswith('/research-centers/') and a.get_text().strip() != "":
    #         payload.append(
    #             {
    #                 "title": a.get_text(),
    #                 "image": images[i].get('src'),
    #             }
    #         )
                

#print(scrapeResearchCenters())
getProfessors("https://biotech.rpi.edu/faculty")