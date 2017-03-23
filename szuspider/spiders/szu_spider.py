import scrapy
import json

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
        filename = self.download_path + 'html/%s.html' % page
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
        html_file_name = self.download_path + 'html/%s.html' % id
        with open(html_file_name, 'wb') as f:
            f.write(response.body)
        self.log('Saved html file %s' % html_file_name)

        save_data = {} 
        save_data['id'] = id
        save_data['title'] = response.css("b font[size='4']").extract_first()
        save_data['content'] = response.css("table[width='85%']").extract_first()
        #print(save_data)
        json_file_name = self.download_path + 'json/%s.json' % id
        self.EncodingJson(json_file_name, save_data)
        self.log('Saved json file %s' % json_file_name)

    @staticmethod
    def DecodingJson(json_file):
        dic = {}
        jfile = open(json_file)

        while True:
            line = jfile.readline()
            if len(line) == 0:
                break
            decode_file = json.loads(line)
            for key, value in decode_file.items():
                dic[key] = value

        jfile.close()
        return dic 
    
    @staticmethod
    def EncodingJson(file_name, data):
        out_json_file = open(file_name,"w")
        json_data = json.dumps(data, sort_keys = True) 
        out_json_file.truncate()
        out_json_file.write(json_data)
        out_json_file.close()

