import scrapy
import json
import mysql.connector
import time
import re


class SzuFromDBSpider(scrapy.Spider):
    name = "szu_from_db"
    download_path = '/tmp/szunews/'

    def start_requests(self):
        urls = []
        conn = mysql.connector.connect(user='szu_spider_w', password='7ca16ef1d8304bc891a78074d2ddf15c',
                                       database='search_engine')
        cursor = conn.cursor()
        sql = "select view_id from `szu_news`"
        cursor.execute(sql)
        rets = cursor.fetchall()
        for ret in rets:
            url = "http://www1.szu.edu.cn/board/view.asp?id=" + str(ret[0])
            # print(url)
            urls.append(url)
            # print(urls)
        cursor.close()
        conn.close()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1]
        news_id = int(page.split('=')[1])
        html_file_name = self.download_path + 'html/%s.html' % news_id
        with open(html_file_name, 'wb') as f:
            f.write(response.body)
        self.log('Saved html file %s' % html_file_name)

        # 根据html规则拆取数据
        save_data = {
            'id': news_id,
            'title': response.css("b font[size='4']::text").extract_first().replace("\u3000", "")
        }
        if save_data['title'] is None or save_data['title'] == '':
            save_data['title'] = response.css("b font[size='4'] b::text").extract_first()
        if save_data['title'] is None or save_data['title'] == '':
            save_data['title'] = response.css("b font[size='4'] font::text").extract_first()
        if save_data['title'] is None or save_data['title'] == '':
            save_data['title'] = response.css("b font[size='4'] b font::text").extract_first()

        temp = response.css("td[height='30'] font[color='#808080']::text").extract_first()  # from 和 date 行
        save_data['from'] = temp.split('\u3000')[0]  # 拆分temp,得到from,date
        save_data['date'] = temp.split('\u3000')[1]

        # 将日期转为双位数字存储
        save_data['date'] = time.mktime(time.strptime(save_data['date'], '%Y-%m-%d %H:%M:%S'))
        save_data['date'] = time.localtime(save_data['date'])
        save_data['date'] = time.strftime('%Y-%m-%d %H:%M:%S', save_data['date'])

        save_data['click_in_content'] = response.css("td[height='40']::text").extract_first()
        save_data['click_in_content'] = re.findall(r"\d+\.?\d*", save_data['click_in_content'])[-1]

        # 过滤 content 的 html 标签
        save_data['content'] = response.css("table[width='86%'] tr").extract()[2]
        dr = re.compile(r'<[^>]+>', re.S)
        save_data['content'] = dr.sub('', save_data['content']).replace("\r\n", "")
        save_data['content'] = ' '.join(save_data['content'].split())

        if save_data['title'] is None or save_data['title'] == '':
            return
        if save_data['content'] is None or save_data['content'] == '':
            return

        json_file_name = self.download_path + 'json/%s.json' % news_id
        self.encoding_json(json_file_name, save_data)  # 转换为json格式保存本地文件
        self.log('Saved json file %s' % json_file_name)

        save_data['content'] = response.css("table[width='86%']").extract_first().replace("86%", "100%")
        self.szu_news_to_db(save_data)  # 数据入库

    @staticmethod
    def szu_news_to_db(data):
        conn = mysql.connector.connect(user='szu_spider_w', password='7ca16ef1d8304bc891a78074d2ddf15c',
                                       database='search_engine')
        cursor = conn.cursor()
        sql = "select count(*) from `szu_news` where `view_id` = %s"
        cursor.execute(sql, (data['id'],))
        ret = cursor.fetchone()
        # print(ret[0])
        if ret[0] == 0:
            sql = "insert into `szu_news` (`view_id`, `title`, `content`, `from`, `date`, `create_time`, `click_in_content`) values (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, [data['id'], data['title'], data['content'], data['from'], data['date'], time.time(),
                                 data['click_in_content']])
        else:
            sql = "update `szu_news` set `title`=%s, `content`=%s, `from`=%s, `date`=%s, `click_in_content`=%s where `view_id`=%s"
            cursor.execute(sql, [data['title'], data['content'], data['from'], data['date'], data['click_in_content'],
                                 data['id']])
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def decoding_json(json_file):
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
    def encoding_json(file_name, data):
        out_json_file = open(file_name, "w", encoding="utf-8")
        json_data = json.dumps(data, sort_keys=True, ensure_ascii=False)
        out_json_file.truncate()
        out_json_file.write(json_data)
        out_json_file.close()
