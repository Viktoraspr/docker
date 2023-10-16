import re
import requests
from bs4 import BeautifulSoup

from dags.src.database.database import Job
from dags.src.database.database_management import DBConnection


class CvOnline:
    def __init__(self, jobs: list = None):
        if jobs:
            self.jobs = '%20'.join(jobs)
        else:
            self.jobs = 'data%20engineer'
        self.db = DBConnection()

    def __extract_page(self, page):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/117.0.0.0 Safari/537.36'}
        url = f'https://www.cvonline.lt/lt/search?limit=20&offset={page}' \
              f'&categories%5B0%5D=INFORMATION_TECHNOLOGY&keywords%5B0%5D={self.jobs}' \
              f'&towns%5B0%5D=540&fuzzy=true&suitableForRefugees=false&isHourlySalary=false&isRemoteWork=false' \
              f'&isQuickApply=false'
        print(url)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def __transport_data(self, soup):
        jobs = soup.findAll('li', class_='jsx-1871295890 jsx-78775730 vacancies-list__item false')
        id_locator = '3024910437'
        for job in jobs:
            url = job.find('a', class_=f'jsx-{id_locator}').get('href', None)
            if self.db.check_if_job_exists_in_db(url):
                continue
            title = job.find('span', class_=f'jsx-{id_locator} vacancy-item__title').text
            company = job.find('div', class_=f'jsx-{id_locator} vacancy-item__column').text
            region = job.find('div', class_=f'jsx-{id_locator} vacancy-item__column vacancy-item__locations').text
            salary = job.find('span', class_=f'jsx-{id_locator} vacancy-item__salary-label').text
            job_ = Job(portal='CVOnline', company=company, job_title=title, link_to_job=url, region=region,
                       salary=int(re.findall(r'\d+', salary)[0]))
            self.db.add_value_to_db(job_)

    def run_scrap(self):
        soup = self.__extract_page(0)
        self.__transport_data(soup)
        self.db.close_session()
