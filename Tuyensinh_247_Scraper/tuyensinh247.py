import operator
import requests
from bs4 import BeautifulSoup


class TuyenSinh247():

    def __init__(self, uni_code, year):
        self.uni_code = uni_code
        self.year = year
        self._URL = f'https://diemthi.tuyensinh247.com/diem-chuan/i-{uni_code}.html?y={year}'
        self._response = self._get_response()
        self._soup = BeautifulSoup(self._get_response().content, 'html.parser')


    def _get_response(self):
        return requests.get(self._URL)

    def get_table(self):
        table = self._soup.find(class_='tab active').select_one("table").contents
        return table

    def get_university_name(self):
        name = self._soup.find(class_='link_fooder last').contents
        return name[1].select_one('span').contents[0].split("–")[0]

if __name__ == '__main__':
    data = TuyenSinh247("TAG", 2019)
    name = data.get_university_name()