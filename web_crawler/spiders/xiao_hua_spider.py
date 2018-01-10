#encoding:utf-8
from time import sleep

import scrapy

from scrapy.selector import HtmlXPathSelector
from ..dingTalkUtils import send_photo,send_text
class XiaoHuaSpider(scrapy.spiders.Spider):
    name = "xiao_hua"
    allowed_domains = ["xiaohua.com"]
    start_urls = [
        "http://www.xiaohuar.com/hua/",
    ]

    def parse(self, response):
        #print(response, type(response))
        # from scrapy.http.response.html import HtmlResponse
        #print(response.body_as_unicode())

        hxs = HtmlXPathSelector(response)
        print hxs
        print response.url

        items = hxs.select('//div[@class="item_list infinite_scroll"]/div')
        print items
        for i in range(len(items)):
            src = hxs.select(
                '//div[@class="item_list infinite_scroll"]/div[%d]//div[@class="img"]/a/img/@src' % i).extract()
            name = hxs.select(
                '//div[@class="item_list infinite_scroll"]/div[%d]//div[@class="img"]/span/text()' % i).extract()
            school = hxs.select(
                '//div[@class="item_list infinite_scroll"]/div[%d]//div[@class="img"]/div[@class="btns"]/a/text()' % i).extract()
            print src
            if src:
                ab_src = "http://www.xiaohuar.com" + src[0]
                file_name = "%s_%s.jpg" % (
                school[0].encode('utf-8'), name[0].encode('utf-8'))
                send_photo(str(ab_src), str(file_name), "校花")