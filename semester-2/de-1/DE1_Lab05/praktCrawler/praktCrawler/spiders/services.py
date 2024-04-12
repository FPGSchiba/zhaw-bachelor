import scrapy
from scrapy.linkextractors import LinkExtractor

class ServicesSpider(scrapy.Spider):
    name = "services"
    allowed_domains = ["www.hittnau.ch"]
    start_urls = ["https://www.hittnau.ch"]

    def parse(self, response):
        if 'online-schalter' in response.url:
            yield {'url': response.url}
        links = LinkExtractor(allow_domains=self.allowed_domains).extract_links(response)
        for link in links:
            yield response.follow(link, self.parse)
