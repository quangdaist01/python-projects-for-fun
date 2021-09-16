from bs4 import BeautifulSoup
import requests


class NguyenKimCategoryScraper:
    """
    Scrape products details from https://www.nguyenkim.com/[category]/
    Make sure
    """

    def __init__(self, url="", features_to_parse=[]):
        response = requests.get(url) if url else requests.get("https://www.nguyenkim.com/may-nuoc-nong")
        self.soup = BeautifulSoup(response.text, "html.parser")
        self.product_links = self._parse_product_links()
        self.pagination_links = [url]  # + self._parse_pagination_links()
        self.product_info = list()
        self.features_to_parse = features_to_parse or ["Xuất xứ:", "Công suất máy nước nóng:", "Nhiệt độ:"]

    # TODO: Reduce memory usage

    def _parse_product_links(self) -> list:
        links = list()
        products = self.soup.find(id="pagination_contents")
        for product in products:
            title = product.find(class_="product-title")
            if title is not None:
                link = title.select_one("a[href]").get("href")
                links.append(link)
        return links

    def _parse_pagination_links(self) -> list:
        pass

    # TODO: Parse pagination links

    def _parse_single_product(self, link: str) -> dict:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, "html.parser")
        title = str(soup.find(class_="product_info_name").string)
        price = str(soup.find(class_="product_info_price_value-final").string)
        product = {"Title:": title, "Price:": price}
        product_details = soup.find(class_="productSpecification_table").tbody
        for row in product_details:
            feature, value = [i.strip() for i in row.strings]
            if feature in self.features_to_parse:
                product.update({feature: value})
        return product

    # TODO: Avoid missing feature when extracting

    def parse_products(self) -> None:
        for link in self.product_links:
            print(self._parse_single_product(link))
            # self.product_info.append(link)

    def find_products(self, string="") -> list:
        pass


NguyenKimCategoryScraper().parse_products()
