import scrapy


class ExpertSpider(scrapy.Spider):
    name = "expert"
    download_delay = 5
    start_urls = [
        # MIT Faculty & Advisors II - Computer Science (Theory)
        'https://www.eecs.mit.edu/people/faculty-advisors/35',
        # MIT Faculty & Advisors II - Computer Science (Systems)
        'https://www.eecs.mit.edu/people/faculty-advisors/32',
        # MIT Faculty & Advisors II - Computer Science (Artificial Intelligence)
        'https://www.eecs.mit.edu/people/faculty-advisors/34',
    ]

    def parse(self, response):
        # Follow links to each researcher's MIT web page
        faculty = response.css('div.people-list')[0]
        if faculty is not None:
            for href in faculty.css('span.field-content.card-title a::attr(href)'):
                yield response.follow(href, self.parse_faculty)

    def parse_faculty(self, response):
        page = response.url
        name = response.css('head title::text').extract_first()
        details = response.css('body').extract()
        yield {
            'page': page,
            'name': name,
            'details': details,
        }

