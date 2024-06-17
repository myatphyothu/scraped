from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Crawler(CrawlSpider):

    name = 'books_to_scrape'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://books.toscrape.com/']
    PROXY_SERVER = None

    rules = (
        Rule(LinkExtractor(allow='catalogue/category')),
        Rule(LinkExtractor(allow='catalogue', deny='category'), callback='parse_item')
    )

    def parse_item(self, response):
        title = response.css('.product_main h1::text').get()
        price = response.css('.price_color::text').get()
        stock = response.css('.availability::text')[1].get().strip()

        yield {'title': title, 'price': price, 'stock': stock}
