# input Scrapy package
import scrapy

from scrapy import Spider

# define class for Spider
class Quotespider(scrapy.Spider):
    name = 'Quote'
    start_url = 'http://quotes.toscrape.com/page/1/'
    scrapy.Request(url=start_url)
    def parse(self,response):
       for quo in response.css('div.quote'):
           text=quo.css('span.text::text').extract()
           author=quo.css('small.author:text').extract()
           tag=quo.css('a.tag::text').extract()
           yield {text:text,'author':author,'tags':tag}
           print('hello')