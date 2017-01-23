import scrapy

class SzuSpider(scrapy.Spider):
    name = "szu"

    def start_requests(self):
        urls = [
            'http://www.szu.edu.cn/board/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #page = response.url.split("/")[-2]
        #filename = 'szu-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)
        for onelink in response.css('tr+a.fontcolor3::attr(href)'):
            next_page = onelink.extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse)   

        for one in response.css('td.fontcolor3'):
            if one.css('font::attr(size)').extract_first() == 4:
                yield {
                    'title': one.css('font::text').extract_first(),
                }
