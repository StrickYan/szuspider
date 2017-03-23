import scrapy

class SzuSpider(scrapy.Spider):
    name = "szu"
    download_path = '/tmp/szunews/'

    def start_requests(self):
        urls = [
            'http://www.szu.edu.cn/board/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = self.download_path + 'szu-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        
        for next_page in response.css('a[href*=view]::attr(href)').extract():
            id = int(next_page.split('=')[1]) #获取id值 view.asp?id=XX, 公文通类型的id值为6位数
            if id < 100000:
                continue
            if next_page is not None:
                #print(next_page)
                next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_news)   

     
    def parse_news(self, response):
         page = response.url.split("/")[-1]
         id = int(page.split('=')[1])
         filename = self.download_path + 'szu-news-%s.html' % id
         with open(filename, 'wb') as f:
             f.write(response.body)
         self.log('Saved file %s' % filename)

        #for one in response.css('td.fontcolor3'):
        #    if one.css('font::attr(size)').extract_first() == 4:
        #        yield {

        #            'title': one.css('font::text').extract_first(),
        #        }
