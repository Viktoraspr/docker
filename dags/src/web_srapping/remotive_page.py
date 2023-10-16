import re
import requests

from bs4 import BeautifulSoup

# from src.web_srapping.html_text import html_text
# from src.web_srapping.html_text_2 import html_text_2


class Remotive:

    def __init__(self, words: list | tuple = ('data', 'engineering')):
        self.base_url = 'https://remotive.com/'
        self.tags = '%20'.join(words)
        self.jobs_url = f'{self.base_url}?query={self.tags}&tags={self.tags}'



    # Job page locators
#     location_locator = '.job-tile-location.tw-uppercase.tag-small.remotive-tag-light.tw-flex '
#     # location_locator = '.job-tile-location.tw-uppercase.tag-small.remotive-tag-light.tw-flex'
#     salary_locator = '.remotive-text-xsmaller.tw-flex.tw-flex-col.tw-m-auto'
#     # salary_locator = 'remotive-text-xsmaller tw-flex tw-flex-col tw-m-auto'
#     job_type = '.tw-flex_tw-flex-col_tw-m-auto'
#
#     def _scan_job_page(self, url: str):
#         # response = requests.get('https://remotive.com/remote-jobs/software-dev/backend-engineering-manager-1732134')
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'html.parser')
#
#         block_class = 'tw-hidden md:tw-block remotive-bg-light tw-w-full tw-mt-16 md:tw-w-2/5 lg:tw-w-1/4'
#         info_block = soup.find('div', class_=block_class)
#
#         salary_location = info_block.find_all('div', class_='remotive-text-xsmaller tw-flex tw-flex-col tw-m-auto')
#
#         salary_block = salary_location[0]
#         location_block = salary_location[1]
#
#         salary = salary_block.find_all('span')[1].text
#         location = location_block.find('span', class_='location-symbol').text
#
#         return {'salary': salary, 'location': location}
#
    def _scan_first_table(self):
        """
        Scans the first page
        :return: None
        """
        # First page locators
        jobs_locator = '.tw-cursor-pointer'
        job_title_locator = '.remotive-bold'
        url_locator = '.job-tile-apply.tw-hidden.remotive-btn-info.tw-mr-2.tw-ml-auto'
        date_locator = '.tw-text-xs.tw-mr-4'

        response = requests.get(self.jobs_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        jobs = soup.select(jobs_locator)
        for ids, job in enumerate(jobs):
            title_job = job.select_one(job_title_locator).get_text()
            job_url = job.select_one(url_locator).get('href', None)
            print(job_url)

            date = None
            try:
                date = job.select_one(date_locator).get_text(strip=True)
            except AttributeError:
                pass

            data = {
                'portal': 'Remotive',
                'job_id': int(re.findall(r'\d+', job_url)[0]),
                'title': title_job,
                'job_url': job_url,
                'date': date,
            }
            print(data)

    def run_the_scan(self):
        self._scan_first_table()
