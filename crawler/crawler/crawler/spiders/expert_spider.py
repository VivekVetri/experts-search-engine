import scrapy


class ExpertSpider(scrapy.Spider):
    name = "expert"
    start_urls = [
        'https://www.csail.mit.edu/person/costis-daskalakis',
    ]

    def parse(self, response):
        name = response.css('title::text').extract_first()
        yield {
            'name': name.css('span.text::text').extract_first()
        }

