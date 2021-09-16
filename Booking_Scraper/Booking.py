from selenium import webdriver
from selenium.webdriver import ChromeOptions
from rich.console import Console
from rich.table import Table
import config


class BookingAPI:
    def __init__(self, min_reviews_score=0, min_reviews_number=0, max_price=None, hotel_only=False):
        self._set_attrs(min_reviews_score=min_reviews_score,
                        min_reviews_number=min_reviews_number,
                        max_price=max_price,
                        hotel_only=hotel_only)
        self.all_hotels = []
        self.extracted_hotels = []

    def __enter__(self):
        print("Finding hotels...")
        self._set_up_driver()
        self._set_selector()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing the browser")
        self._driver.quit();

    def _set_attrs(_self, **kwargs):
        for k, v in kwargs.items():
            setattr(_self, k, v)

    def _set_selector(self):
        self.HOTEL_NAME_CLASS = "sr-hotel__name"
        self.HOTEL_LINK_CLASS = "js-sr-hotel-link.hotel_name_link.url"
        self.REVIEWS_SCORE_CLASS = "bui-review-score__badge"
        self.REVIEWS_NUMBER_CLASS = "bui-review-score__text"
        self.PRICE_CLASS = "bui-price-display__value.prco-inline-block-maker-helper"

    def _set_up_driver(self):
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        self._chrome_options = ChromeOptions()
        self._chrome_options.add_argument(f"user-agent={USER_AGENT}")
        self._chrome_options.add_argument("--headless")
        self._chrome_options.add_argument("--incognito")
        self._chrome_options.add_argument("--window-size=1920x1080")
        self._driver = webdriver.Chrome(options=self._chrome_options,
                                        executable_path=config.CHROMEDRIVER_PATH)

    def _get_text(self, hotel, cls_name, get_link=False):
        if get_link:
            return hotel.find_element_by_class_name(cls_name).get_attribute("href")
        else:
            return hotel.find_element_by_class_name(cls_name).get_attribute("innerText").replace("\n", "")

    def _parse_numeric(self, value, type):
        if type == "reviews score":
            return float(value.replace(",", "."))
        elif type == "reviews number":
            return int(''.join(filter(lambda i: i.isdigit(), value)))
        elif type == "price":
            return int(''.join(filter(lambda i: i.isdigit(), value))) if value else 0
        else:
            return 0

    def _is_suitable(self, value, criteria):
        if criteria == "name":
            return "hotel" in value.lower()
        if criteria == "reviews score":
            return True if self._parse_numeric(value, criteria) >= self.min_reviews_score else False
        if criteria == "reviews number":
            return True if self._parse_numeric(value, criteria) >= self.min_reviews_number else False
        if criteria == "price":
            return True if self._parse_numeric(value, criteria) <= self.max_price else False

    def _get_all_hotels(self, link):
        self._driver.get(link)
        self._driver.implicitly_wait(5)
        all_hotels = (
            self._driver.find_elements_by_class_name("sr_item_content.sr_item_content_slider_wrapper"))
        return all_hotels

    def _filter_and_extractInfo(self, hotels):
        extracted_hotels = []
        for hotel in hotels:
            name = self._get_text(hotel, self.HOTEL_NAME_CLASS)
            if self.hotel_only and not self._is_suitable(name, "name"):
                continue
            reviews_score = self._get_text(hotel, self.REVIEWS_SCORE_CLASS)
            if not self._is_suitable(reviews_score, "reviews score"):
                continue
            reviews_number = self._get_text(hotel, self.REVIEWS_NUMBER_CLASS)
            if not self._is_suitable(reviews_number, "reviews number"):
                continue
            price = self._get_text(hotel, self.PRICE_CLASS)
            if not self._is_suitable(price, "price"):
                continue
            link = self._get_text(hotel, self.HOTEL_LINK_CLASS, get_link=True)
            extracted_hotels.append((name, link, reviews_score, reviews_number, price))
        return extracted_hotels

    def get_filtered_hotels(self, link):
        all_hotels = self._get_all_hotels(link)
        result = self._filter_and_extractInfo(all_hotels)
        self.extracted_hotels.extend(result)
        return self

    def renderRaw(self):
        result = f"Điều kiện:\n\tĐiểm tối thiểu: {self.min_reviews_score}\n\tSố lượng đánh giá tối thiểu: {self.min_reviews_number}\n\tGiá tối ta: {self.max_price}\n\n"
        for hotel in self.extracted_hotels:
            name, _, reviews_score, reviews_number, price = hotel
            result += f"{name} || {reviews_score} \n{reviews_number} \n{price} \n\n"
        return result

    def prettify_terminal(self):
        console = Console()
        table = Table(title="Danh sách các khách sạn phù hợp trên Booking.com")
        table.add_column("Tên", style="cyan")
        table.add_column("Điểm reviews", justify="center", style="green")
        table.add_column("Số reviews", justify="center", style="magenta")
        table.add_column("Giá", justify="center", style="yellow")
        for hotel in self.extracted_hotels:
            name, _, reviews_score, reviews_number, price = hotel
            table.add_row(name, reviews_score, reviews_number, price)
        console.print(table)

    def render_html(self):
        html = f'''<html>
        <head>
        <h4>Điểm Review >= {self.min_reviews_score}, Số lượng Review >= {self.min_reviews_number}, Giá <= {self.max_price}</h4>
        </head>
        <body>'''
        for hotel in self.extracted_hotels:
            name, link, reviews_score, reviews_number, price = hotel
            html += f'''
            <a href='{link}'>{name}</a>
            <p>{reviews_score}</p>
            <p>{reviews_number}</p>
            <p>{price}</p>
            <hr>
            '''
        html += '''</body>
        </html>'''
        return html


if __name__ == "__main__":
    with BookingAPI(hotel_only=True, min_reviews_number=30, min_reviews_score=7, max_price=420000) as bot:
        bot.get_filtered_hotels(config.url)
        bot.prettify_terminal()
