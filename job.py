import re

import requests
from bs4 import BeautifulSoup


def job_search(location, technology):
    """Method to look for a job in the Internet."""
    page_number = 1
    job_links = []
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"}

    while True:
        nofluffjobs_url = f"https://nofluffjobs.com/pl/jobs/{location}/{technology}?criteria=city%3D{location}%20{technology}&page={page_number}"

        page = requests.get(nofluffjobs_url, headers=headers)
        json_data = page.json()
        print(json_data)
        soup = BeautifulSoup(page.content, 'html.parser')
        for a in soup.findAll('a', class_=re.compile("^posting-list-item posting-list-item--"), href=True):
            if a['href'] not in job_links:
                job_links.append(a['href'])
            else:
                break

        page_number += 1

    page_number = 1
    # TODO: search for a job on justjoin.it site