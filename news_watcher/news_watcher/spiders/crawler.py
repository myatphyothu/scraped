import scrapy
from bs4 import BeautifulSoup


class Crawler(scrapy.Spider):

    name = 'news_watcher'
    allowed_domains = ['caeh.ca']
    start_urls = ['https://caeh.ca/category/news']

    PROXY_SERVER = None

    def parse(self, response):
        links_css = response.css('div.postHeadline a::attr(href)')
        for css in links_css:
            yield response.follow(css.get(), callback=self.parse_news)

    def drilldown_content(self, response):
        raw_content = ''.join(response.css('div.entry p').getall())
        return BeautifulSoup(raw_content).get_text()

    def parse_news(self, response):
        title = response.css('p.postTitle::text').get().strip()
        url = response.request.url

        content = self.drilldown_content(response)

        yield {
            'title': title,
            'url': response.request.url,
            'content': content
        }

