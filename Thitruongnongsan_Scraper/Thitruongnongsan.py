from selenium import webdriver
import datetime
from dateutil import parser
import json


class NongSanScraper:
    """
    Scrape agricultural products data on http://thitruongnongsan.gov.vn/
    """

    def __init__(self):
        # self.driver = webdriver.Chrome(executable_path="chromedriver.exe")
        self.driver = webdriver.Chrome(executable_path="/Chapter01/chromedriver.exe")
        self.driver.get("http://thitruongnongsan.gov.vn/vn/nguonwmy.aspx/")

    @staticmethod
    def _is_date_within(date, *, days_ago):
        duration = datetime.timedelta(days=30)
        return datetime.datetime.now() - date <= duration

    @staticmethod
    def _append_jsonl_file(data: dict) -> None:
        with open("results.jsonl", "a+", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")

    def _parse_each_category(self, *, export=False) -> None:
        table = self.driver.find_elements_by_css_selector("table.mGrid > tbody > tr:not(.pgr)")
        for row in table:
            name, market, date, price = [item.text for item in row.find_elements_by_css_selector("td")]
            date = parser.parse(date)
            if self._is_date_within(date, days_ago=30):
                result = {"Ten_mat_hang": name, "Thi_thuong": market, "Ngay": str(date.date()), "Gia": price}
                self._append_jsonl_file(result) if export else print(result)

    def parse(self, *, export=False):
        categories = self.driver.find_elements_by_css_selector(
            "select[name='ctl00$maincontent$mathangnongsan'] > option")
        for index in range(1, len(categories)):
            categories = self.driver.find_elements_by_css_selector(
                "select[name='ctl00$maincontent$mathangnongsan'] > option")
            categories[index].click()
            try:
                self.driver.find_element_by_css_selector("[name='ctl00$maincontent$Xem']").click()
                self._parse_each_category(export=export)
            except:
                continue
        self.driver.quit()


NongSanScraper().parse(export=True)
