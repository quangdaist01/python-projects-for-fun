from selenium import webdriver
from selenium.webdriver import ChromeOptions
import config

class BookingAPI:
    def __init__(self, link):
        self.matched_hotels = []
        self._set_up_driver(link)
        self._set_selector()

    def __enter__(self):
        print("Finding hotels...")
        self.hotel_result = self._driver.find_elements_by_class_name("sr_item_content.sr_item_content_slider_wrapper")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Closing the browser")
        self.end_session()

    def _set_selector(self):
        self.HOTEL_NAME_CLASS = "sr-hotel__name"
        self.HOTEL_LINK_CLASS = "js-sr-hotel-link.hotel_name_link.url"
        self.RATING_CLASS = "bui-review-score__badge"
        self.NUM_RATING_CLASS = "bui-review-score__text"
        self.PRICE_CLASS = "bui-price-display__value.prco-inline-block-maker-helper"

    def _set_up_driver(self, link):
        USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        self._chrome_options = ChromeOptions()
        self._chrome_options.add_argument(f"user-agent={USER_AGENT}")
        self._chrome_options.add_argument("--headless")
        self._chrome_options.add_argument("--incognito")
        self._chrome_options.add_argument("--window-size=1920x1080")
        self._driver = webdriver.Chrome(options=self._chrome_options,
                                        executable_path=config.CHROMEDRIVER_PATH)
        self._driver.get(link)

    def _get_text(self, hotel, cls_name, attr=None):
        if attr == "href":
            return hotel.find_element_by_class_name(cls_name).get_attribute("href")
        else:
            return hotel.find_element_by_class_name(cls_name).get_attribute("innerText").replace("\n", "")

    def _convert(self, value, type):
        if type == "rating":
            return float(value.replace(",", "."))
        elif type == "num_rating":
            return int(''.join(filter(lambda i: i.isdigit(), value)))
        elif type == "price":
            return int(''.join(filter(lambda i: i.isdigit(), value))) if value else 0
        else:
            return 0


    def _is_suitable(self, value, criteria):
        if criteria == "name":
            return "hotel" in value.lower()
        if criteria in ("rating"):
            return True if self._convert(value, criteria) >= self.rates_score else False
        if criteria in ("num_rating"):
            return True if self._convert(value, criteria) >= self.min_num_rating else False
        if criteria in ("price"):
            return True if self._convert(value, criteria) <= self.price_limit else False

    def end_session(self):
        self._driver.quit();

    def get_hotels_info(self, rates_score=0, min_num_rating=0, price_limit=None, hotel_only=False):
        self.rates_score = rates_score
        self.min_num_rating = min_num_rating
        self.price_limit = price_limit
        for hotel in self.hotel_result:
            name = self._get_text(hotel, self.HOTEL_NAME_CLASS)
            if hotel_only and not self._is_suitable(name, "name"):
                continue
            rating = self._get_text(hotel, self.RATING_CLASS)
            if not self._is_suitable(rating, "rating"):
                continue
            num_rating = self._get_text(hotel, self.NUM_RATING_CLASS)
            if not self._is_suitable(num_rating, "num_rating"):
                continue
            price = self._get_text(hotel, self.PRICE_CLASS)
            if not self._is_suitable(price, "price"):
                continue
            link = self._get_text(hotel, self.HOTEL_LINK_CLASS, attr="href")

            print(name, rating, num_rating, price)
            self.matched_hotels.append((name, link, rating, num_rating, price))
        return self

    def render_raw(self):
        result = f"Điều kiện:\n\tĐiểm tối thiểu: {self.rates_score}\n\tSố lượng đánh giá tối thiểu: {self.min_num_rating}\n\tGiá tối ta: {self.price_limit}\n\n"
        for hotel in self.matched_hotels:
            name, _, rating, num_rating, price = hotel
            result += f"{name} || {rating} \n{num_rating} \n{price} \n\n"
        return result

    def render_html(self):
        html = f'''<html>
        <head>
        <h4>Điểm Review >= {self.rates_score}, Số lượng Review >= {self.min_num_rating}, Giá <= {self.price_limit}</h4>
        </head>
        <body>'''
        for hotel in self.matched_hotels:
            name, link, rating, num_rating, price = hotel
            html += f'''
            <a href='{link}'>{name}</a>
            <p>{rating}</p>
            <p>{num_rating}</p>
            <p>{price}</p>
            <hr>
            '''
        html += '''</body>
        </html>'''
        return html


if __name__ == "__main__":
    with BookingAPI(config.url) as bot:
        bot.get_hotels_info(hotel_only=True, min_num_rating=30, rates_score=7, price_limit=420000)
