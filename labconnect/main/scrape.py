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
                "image": image.get('src'),
            }
        )
    
    return payload


    
    # for i, a in enumerate(soup.find_all('a')):
    #     if a.get('href') is not None and a.get('href').startswith('/research-centers/') and a.get_text().strip() != "":
    #         payload.append(
    #             {
    #                 "title": a.get_text(),
    #                 "image": images[i].get('src'),
    #             }
    #         )
                

print(scrapeResearchCenters())