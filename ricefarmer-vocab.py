import scrapy
from scrapy import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

inc = 0 #so that decideAndClick is entered only when all parseThes are finished
syns = [0, 1, 2, 3, 4] #sets of synonyms of the vocabulary words

class RiceSpider(scrapy.Spider):
    name = 'RiceFarmer'
    start_urls = ['http://freerice.com/user/login']
    handle_httpstatus_list = [301, 302]

    def __init__(self):
        self.driver = webdriver.Firefox()
    

    def parse(self, response):
        self.driver.get(response.url)

        xButton = self.driver.find_element_by_xpath('//a[@id="wfp-ew-dialog-close"]')
        xButton.click() #close ad

        self.driver.execute_script('document.getElementById("edit-name").style.display = "block"') #force visibility
        username = self.driver.find_element_by_xpath('//input[@id="edit-name"]')
        username.send_keys('username')

        pw = self.driver.find_element_by_xpath('//input[@id="edit-pass"]')
        pw.send_keys('password')
        pw.submit()

        self.driver.get('http://freerice.com')
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="block-means-vocab"]/div/div[@class="item-list"]/ul/li/a')))
        yield scrapy.Request('http://freerice.com', callback = self.parseRice)


    def parseRice(self, response):
        riceSRC = self.driver.page_source

        vocab = [0,1,2,3,4]

        vocab[0] = Selector(text=riceSRC).xpath('//div[@id="question-title"]/a/b/text()').extract()[0]
        vocab[1] = Selector(text=riceSRC).xpath('//div[@class="block-means-vocab"]/div/div[@class="item-list"]/ul/li/a/text()').extract()[0]
        vocab[2] = Selector(text=riceSRC).xpath('//div[@class="block-means-vocab"]/div/div[@class="item-list"]/ul/li/a/text()').extract()[1]
        vocab[3] = Selector(text=riceSRC).xpath('//div[@class="block-means-vocab"]/div/div[@class="item-list"]/ul/li/a/text()').extract()[2]
        vocab[4] = Selector(text=riceSRC).xpath('//div[@class="block-means-vocab"]/div/div[@class="item-list"]/ul/li/a/text()').extract()[3]

        yield scrapy.Request("http://www.thesaurus.com/browse/" + vocab[0], callback = self.parseThes, meta={'num': 0, 'dont_redirect': True})
        yield scrapy.Request("http://www.thesaurus.com/browse/" + vocab[1], callback = self.parseThes, meta={'num': 1, 'dont_redirect': True})
        yield scrapy.Request("http://www.thesaurus.com/browse/" + vocab[2], callback = self.parseThes, meta={'num': 2, 'dont_redirect': True})
        yield scrapy.Request("http://www.thesaurus.com/browse/" + vocab[3], callback = self.parseThes, meta={'num': 3, 'dont_redirect': True})
        yield scrapy.Request("http://www.thesaurus.com/browse/" + vocab[4], callback = self.parseThes, meta={'num': 4, 'dont_redirect': True})


    def parseThes(self, response):
        global inc
        global syns
        temp = set()
        for a in response.selector.xpath('//div[@class="relevancy-list"]/ul/li'):
            selector = './/a/span/text()'
            temp.add(a.xpath(selector).extract_first())
        syns[response.meta['num']] = temp

        inc += 1
        if inc == 5:
            answer = self.driver.find_element_by_xpath('//a[@class="answer-item" and @rel="' + self.decideAndClick() + '"]')
            answer.click() #clicks answer
            self.driver.quit()


    def decideAndClick(self):
        global syns
        choice = [0,1,2,3] #matches up to the rel attribute

        choice[0] = len(set(syns[0].intersection(syns[1])))
        choice[1] = len(set(syns[0].intersection(syns[2])))
        choice[2] = len(set(syns[0].intersection(syns[3])))
        choice[3] = len(set(syns[0].intersection(syns[4])))

        return str(choice.index(max(choice)))

        
