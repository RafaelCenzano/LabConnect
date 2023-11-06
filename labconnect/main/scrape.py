from bs4 import BeautifulSoup
import requests

def scrapeResearchCenters():
    url = "https://research.rpi.edu/research-centers"
    
    payload = []
    
    page = requests.get(url)
    
    if (page.status_code != 200): # safety
        return "Error: " + str(page.status_code)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    soup.find_all('a')
    for (i, a) in enumerate(soup.find_all('a')):
        #print(i, a)
        if a.get('href') != None:
            if a.get('href').startswith('/research-centers/'):
                if (a.get_text().strip() != "" and a.get_text().strip() != None):
                    #print(a.get_text())
                    payload.append(
                        {
                            "title": a.get_text(),
                        }
                    )
    
    return payload