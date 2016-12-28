import scrapy
from scrapy import Selector
from scrapy.spidermiddlewares.httperror import HttpError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random
import sys
inc = 0
periodicDict = {'Hydrogen': 'H', 'Helium': 'He', 'Lithium': 'Li', 'Beryllium': 'Be', 'Boron': 'B', 'Carbon': 'C', 'Nitrogen': 'N', 'Oxygen': 'O', 'Fluorine': 'F', 'Neon': 'Ne', 'Sodium': 'Na', 'Magnesium': 'Mg', 'Aluminium': 'Al', 'Silicon': 'Si', 'Phosphorus': 'P', 'Sulfur': 'S', 'Chlorine': 'Cl', 'Argon': 'Ar', 'Potassium': 'K', 'Calcium': 'Ca', 'Scandium': 'Sc', 'Titanium': 'Ti', 'Vanadium': 'V', 'Chromium': 'Cr', 'Manganese': 'Mn', 'Iron': 'Fe', 'Cobalt': 'Co', 'Nickel': 'Ni', 'Copper': 'Cu', 'Zinc': 'Zn', 'Gallium': 'Ga', 'Germanium': 'Ge', 'Arsenic': 'As', 'Selenium': 'Se', 'Bromine': 'Br', 'Krypton': 'Kr', 'Rubidium': 'Rb', 'Strontium': 'Sr', 'Yttrium': 'Y', 'Zirconium': 'Zr', 'Niobium': 'Nb', 'Molybdenum': 'Mo', 'Technetium': 'Tc', 'Ruthenium': 'Ru', 'Rhodium': 'Rh', 'Palladium': 'Pd', 'Silver': 'Ag', 'Cadmium': 'Cd', 'Indium': 'In', 'Tin': 'Sn', 'Antimony': 'Sb', 'Tellurium': 'Te', 'Iodine': 'I', 'Xenon': 'Xe', 'Cesium': 'Cs', 'Barium': 'Ba', 'Lanthanum': 'La', 'Cerium': 'Ce', 'Praseodymium': 'Pr', 'Neodymium': 'Nd', 'Promethium': 'Pm', 'Samarium': 'Sm', 'Europium': 'Eu', 'Gadolinium': 'Gd', 'Terbium': 'Tb', 'Dysprosium': 'Dy', 'Holmium': 'Ho', 'Erbium': 'Er', 'Thulium': 'Tm', 'Ytterbium': 'Yb', 'Lutetium': 'Lu', 'Hafnium': 'Hf', 'Tantalum': 'Ta', 'Tungsten': 'W', 'Rhenium': 'Re', 'Osmium': 'Os', 'Iridium': 'Ir', 'Platinum': 'Pt', 'Gold': 'Au', 'Mercury': 'Hg', 'Thallium': 'Tl', 'Lead': 'Pb', 'Bismuth': 'Bi', 'Polonium': 'Po', 'Astatine': 'At', 'Radon': 'Rn', 'Francium': 'Fr', 'Radium': 'Ra', 'Actinium': 'Ac', 'Thorium': 'Th', 'Protactinium': 'Pa', 'Uranium': 'U', 'Neptunium': 'Np', 'Plutonium': 'Pu', 'Americium': 'Am', 'Curium': 'Cm', 'Berkelium': 'Bk', 'Californium': 'Cf', 'Einsteinium': 'Es', 'Fermium': 'Fm', 'Mendelevium': 'Md', 'Nobelium': 'No', 'Lawrencium': 'Lr', 'Rutherfordium': 'Rf', 'Dubnium': 'Db', 'Seaborgium': 'Sg', 'Bohrium': 'Bh', 'Hassium': 'Hs', 'Meitnerium': 'Mt', 'Darmstadtium': 'Ds', 'Roentgenium': 'Rg', 'Ununbium': 'Uub', 'Ununtrium': 'Uut', 'Ununquadium': 'Uuq', 'Ununpentium': 'Uup', 'Ununhexium': 'Uuh', 'Ununseptium': 'Uus', 'Ununoctium': 'Uuo'}

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
        pw.send_keys('quentintruong')
        pw.submit()

        self.driver.get('http://freerice.com/#/chemical-symbols-full-list/1')
        yield scrapy.Request('http://freerice.com/#/chemical-symbols-full-list/1', callback = self.parseRice)


    def parseRice(self, response):
        global periodicDict, inc

        riceSRC = self.driver.page_source
        option = [0,1,2,3,4]

        option[0] = Selector(text=riceSRC).xpath('//div[@id="question-title"]/a/b/text()').extract_first()
        option[1] = Selector(text=riceSRC).xpath('//a[@class="answer-item" and @rel="0"]/text()').extract_first()
        option[2] = Selector(text=riceSRC).xpath('//a[@class="answer-item" and @rel="1"]/text()').extract_first()
        option[3] = Selector(text=riceSRC).xpath('//a[@class="answer-item" and @rel="2"]/text()').extract_first()
        option[4] = Selector(text=riceSRC).xpath('//a[@class="answer-item" and @rel="3"]/text()').extract_first()

        if None in option:
            self.driver.quit()
            sys.exit()

        try:
            mySym = periodicDict[option[0]]
        except KeyError:
            self.driver.quit()
            sys.exit()

        answer = ""

        if mySym == option[1]:
            answer = self.driver.find_element_by_xpath('//a[@class="answer-item" and @rel="0"]')
        elif mySym == option[2]:
            answer = self.driver.find_element_by_xpath('//a[@class="answer-item" and @rel="1"]')
        elif mySym == option[3]:
            answer = self.driver.find_element_by_xpath('//a[@class="answer-item" and @rel="2"]')
        else:
            answer = self.driver.find_element_by_xpath('//a[@class="answer-item" and @rel="3"]')

        answer.click()
        time.sleep(random.randrange(1, 3)) #delay because website ban
        inc += 1
        if inc == 19: #stop beyond 19 because website ban
            self.driver.quit()
            sys.exit()

        self.driver.get('http://freerice.com/restart')

        yield scrapy.Request('http://freerice.com/restart', callback = self.parseRice, dont_filter = True)

        
