import requests
from bs4 import BeautifulSoup
from jinja2 import Template


class TrungTamDayKem_Scrapy:
    def __init__(self, *args, **kwargs):
        self.response = requests.get('https://www.trungtamdaykem.com/lop-day-hien-co-dang-list.html')
        self.soup = BeautifulSoup(self.response.content, 'html.parser')
        self.table = self.soup.select("#main-content-3col > div > div.panel-body > table > tr")
        self.table.pop(0)
        self.kwargs = kwargs

    def _select_info(self, row):
        info = row.select('td')
        code, subject_time, loc, *_, tutor_gender, _ = info
        subject, time = subject_time.strong, subject_time.span
        package = list(map(lambda x: x.text, (code, subject, time, loc, tutor_gender)))
        return package

    def render_raw(self, return_dict=False):
        loc, gen, *_ = self.kwargs.values()
        matched_courses = {'location': loc, 'gender': gen, 'courses': []}
        for row in self.table:
            code, subject, time, location, tutor_gender = self._select_info(row)
            if loc not in location:
                continue
            if gen not in tutor_gender:
                continue
            matched_courses['courses'].append({'code': code, 'subject': subject, 'time': time, 'location': location})
        if return_dict:
            return matched_courses
        else:
            return ''.join([f'{code} || {subject} \n{time} \n{location} \n\n' for course in matched_courses['courses']])

    def render_html(self, file_path=None):
        html_data = self.render_raw(return_dict=True)
        with open(
                file_path or "C:/Users/quang/PycharmProjects/pythonProject3/Trungtamdaykem_Scraper/mail-portfolio-master/index.html",
                encoding='utf-8') as html:
            template = Template(html.read())
        return template.render(location=html_data['location'],
                               gender=html_data['gender'],
                               courses=html_data['courses'])


if __name__ == '__main__':
    result = TrungTamDayKem_Scrapy(loc="Tân Phú", gen="Sinh viên Nữ")
    courses = result.render_html()
    print(courses)
