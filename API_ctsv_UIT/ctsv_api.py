from requests import get
from bs4 import BeautifulSoup
from datetime import datetime

# TODO:
# - Viết code tự động gửi mail khi có bài viết mới. ko thì ko gửi
demo_date = datetime.strptime("1/6/2021", '%d/%m/%Y').date()


class CTSV_API:
    def __init__(self):
        response = get("https://ctsv.uit.edu.vn/")
        soup = BeautifulSoup(response.text, "html.parser")
        self.current_date = datetime.now().date()
        self.raw_content = soup.select_one(
            "#block-views-front-page-block-block-3 > div > div > div.view-content > table > tbody").contents
        self.all_articles = self._remove_redundant_newlineIn(self.raw_content)

    @staticmethod
    def convert_date(str_date):
        return datetime.strptime(str_date, '%d/%m/%Y').date()

    @staticmethod
    def _remove_redundant_newlineIn(content):
        return [article for article in content if article != "\n"]

    def get_title_link_date(self, article_item):
        title_tag = article_item.select_one("td").contents[1]
        date_line = article_item.select_one("td").contents[2]  # Format: " -     dd/mm/yyyy"
        return title_tag.text, title_tag.get("href"), date_line.split().pop()

    def has_new_articles(self):
        newest_ariticle = self.all_articles[0]
        *_, date = self.get_title_link_date(newest_ariticle)
        if self.convert_date(date) == self.current_date:
        # if self.convertDate(date) == demo_date:
            return True
        return False

    def get_newest_articles(self, type ="raw"):
        new_articles = []
        for item in self.all_articles:
            title, link, date = self.get_title_link_date(item)
            if self.convert_date(date) == self.current_date:
            # if self.convertDate(date) == demo_date:
                new_articles.append((title, link, date))
        if type == "raw":
            return self._render_raw(new_articles)
        elif type == "html":
            return self._render_html(new_articles)
        else:
            None

    @staticmethod
    def _render_raw(articles):
        raw_text = ""
        for title, link, date in articles:
            raw_text += date + "\n" + title + "\n" + "ctsv.uit.edu.vn" + link  + "\n\n"
        return raw_text

    @staticmethod
    def _render_html(articles):
        pass

if __name__=="__main__":
    bot = CTSV_API()
    moi_nhat = bot.has_new_articles()
    article_list = bot.get_newest_articles()
    print(article_list)

