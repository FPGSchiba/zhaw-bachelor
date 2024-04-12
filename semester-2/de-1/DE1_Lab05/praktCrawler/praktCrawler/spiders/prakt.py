import scrapy
from scrapy.linkextractors import LinkExtractor
import re


class PraktSpider(scrapy.Spider):
    name = "prakt"
    allowed_domains = ["www.hittnau.ch"]
    start_urls = ["https://www.hittnau.ch/"]

    def parse(self, response):
        try:
            current_category = response.url.split("/")[3]
        except KeyError:
            current_category = ''
        links = response.css('a')
        if bool(links):
            yield {'url': response.url,
                   'email_ad': list(set([re.search(r'.*mailto:(.+@.+?)"', str(item)).group(1) for item in response.css('a') if
                                bool(re.match('.*href="mailto:.+@.+"', str(item)))])),
                   'category': current_category}
        else:
            yield {'url': response.url, 'email_ad': [], 'category': current_category}
        links = LinkExtractor(allow_domains=self.allowed_domains).extract_links(response)
        for link in links:
            yield response.follow(link, self.parse)
