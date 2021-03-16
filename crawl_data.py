import requests
from bs4 import BeautifulSoup


class TrungTamDayKem_Crawler:
    def __init__(self):
        self.response = requests.get('https://www.trungtamdaykem.com/lop-day-hien-co-dang-list.html')
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.table = self.soup.select("#main-content-3col > div > div.panel-body > table > tr")
        self.table.pop(0)

    def find_courses(self, loc=None, gen=None):
        matched_courses = ''
        for row in self.table:
            info = row.select('td')
            code = info[0].text
            subject = info[1].strong.text
            time = info[1].span.text
            location = info[2].text
            tutor_gender = info[6].text
            if loc is not None:
                if loc not in location:
                    continue
            if gen is not None:
                if gen not in tutor_gender:
                    continue
            matched_courses += f'{code} || {subject} \n{time} \n{location} \n\n'
        return matched_courses


result = TrungTamDayKem_Crawler()
print(result.find_courses(loc="Thủ Đức", gen="Sinh viên Nam"))
