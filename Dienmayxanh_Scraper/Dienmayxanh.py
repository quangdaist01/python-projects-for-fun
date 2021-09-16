from selenium import webdriver
import json


class DienMayXanhScraper:
    """
    Parse comments and ratings of Iphones on
    https://www.dienmayxanh.com/dien-thoai-apple-iphone
    """

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")
        self.driver.get("https://www.dienmayxanh.com/dien-thoai-apple-iphone/")
        self.phones = self.driver.find_elements_by_xpath('//*[@id="categoryPage"]/div[3]/ul/li/a[1]')

    def _go_to_first_tab(self) -> None:
        self.driver.switch_to.window(self.driver.window_handles[0])

    def _go_to_new_tab(self, *args, link=None) -> None:
        self.driver.execute_script(f'''window.open("{link}","new_window");''')
        self.driver.switch_to.window(self.driver.window_handles[1])

    @staticmethod
    def _append_jsonl_file(data: dict) -> None:
        with open("results.jsonl", "a+", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)
            f.write("\n")

    def parse(self, *args, export=False) -> None:
        for phone in self.phones:
            self._go_to_new_tab(link=phone.get_attribute("href"))
            self.driver.find_element_by_link_text("Xem tất cả đánh giá").click()
            comments = self.driver.find_elements_by_css_selector("div[class='comment__item par']")
            for comment in comments:
                text = comment.find_element_by_class_name("cmt-txt").text
                rating = len(comment.find_elements_by_class_name("icon-star"))
                result = {"text": text, "rating": rating}
                self._append_jsonl_file(result) if export else print(result)
            self._go_to_first_tab()
        self.driver.quit()


DienMayXanhScraper().parse()
