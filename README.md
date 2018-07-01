# SZU Spider
* a spider for szu news
* 深圳大学校内搜索引擎爬虫模块源码，爬取公文通，保存为Json格式的本地文本
* 索引模块及查询模块源码见 [ins](https://github.com/StrickYan/ins)

## 定时脚本
```
# 每隔一小时抓取 szu 公文通信息（最近7天）
30 * * * * source ~/.bash_profile; cd /home/wwwroot/default/szuspider && /usr/local/bin/scrapy crawl szu -s LOG_FILE=/tmp/szunews/logs/logs-crawl-szu-news/crawl.log.`/bin/date "+\%Y-\%m-\%d~\%H:\%M:\%S"`

# 每隔一个小时更新索引
00 * * * * source ~/.bash_profile; curl http://localhost:8080/ins/createIndex > /tmp/szunews/logs/logs-create-index/`/bin/date "+\%Y-\%m-\%d~\%H:\%M:\%S"`.log
```

## 捐赠
  <img src="https://raw.githubusercontent.com/StrickYan/sixchat/master/md_img/Alipay.jpeg" width="200px" />
  <img src="https://raw.githubusercontent.com/StrickYan/sixchat/master/md_img/WePay.jpeg" width="200px" />
