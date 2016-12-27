import scrapy
from scrapy import Selector
from selenium import webdriver

class ChemSpider(scrapy.Spider):
    name = 'ChemPull'
    start_urls = ['http://www.lenntech.com/periodic-chart-elements/atomic-number.htm']
    handle_httpstatus_list = [301, 302]

    def __init__(self):
        self.driver = webdriver.Firefox()
    

    def parse(self, response):
        self.driver.get(response.url)
        riceSRC = self.driver.page_source

        full = ""

        for a in Selector(text=riceSRC).xpath('//tr'):
            name = a.xpath('./td[@class="xl25"]/a/strong/text()').extract_first()
            sym = a.xpath('./td[@class="xl24" and @height!="32"]/strong/text()').extract_first()
            if name != None:
                full += "'" + name + "': '" + sym + "', "

        print(full)
