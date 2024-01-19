# supporting functions and mountain list variables for snow-forecast scraping tool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import json


class Mountain:
    def __init__(self, url, name, dense_url, location):
        self.url = url
        self.name = name
        self.dense_url = dense_url
        self.location = location
    def __str__(self):
        return f"url: {self.url}\nName: {self.name}\nDense url: {self.dense_url}\nLocation: {self.location}\n"

mountain_list = []  #all US ski mountains as list of Mountain
with open('mountains.txt','r') as file:
    data = json.load(file) 
    for i in data: 
        j = json.loads(json.dumps(i)) #need dumps to convert from python strings (single quote) to json quotes (double quote)
        mountain = Mountain(**j)
        mountain_list.append(mountain)

home_mountain_list = [] #user-specific US ski mountains as list of Mountain
with open('home_mountains.txt','r') as file:
    data = json.load(file) 
    for i in data: 
        j = json.loads(json.dumps(i))
        mountain = Mountain(**j)
        home_mountain_list.append(mountain)
    
'''
summary: represents mountain object as a dict.
args: 
    - mountain: a mountain object
returns:
    - mountain.__dict__: the mountain object represented as a dictionary
notes: for json encoding of mountains in mountains.txt
'''
def mountain_encoder(mountain):
    return mountain.__dict__

'''
summary: gives number value (if any) from text
args: 
    - n: a value that may be a number
returns:
    - the parsed number value or 0 if not a number
'''
def number_value(n):
    try:
        return float(n)
    except:
        return 0
    
'''
summary: compiles US ski mountain data from snow-forecast.com and deposits it in mountains.txt
args: none
other inputs:
    - mountain location: from location dropdown
    - mountain name: from resort dropdown
    - mountain url: from dropdown 'value' attribute
returns: none
other outputs:
    - mountains.txt
notes: currently using unreliable 1 second sleeps rather than more nuanced selenium waits. on the todo list
'''
def scrape_mountains():
    mountain_list = []
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.snow-forecast.com")
    us_mountain_navs = driver.find_elements(By.XPATH, "//select[@id='feature']/option[contains(text(),'USA - ')]")
    for i in us_mountain_navs:
        i.click()
        location = i.text
        time.sleep(1)
        state_mountain_navs = driver.find_elements(By.XPATH, "//select[@id='resort']/option[not(contains(text(),'Choose resort'))]")
        for j in state_mountain_navs:
            url = j.get_attribute('value')
            name = j.text
            dense_url = re.sub(r'\W+', '', url, flags = re.A).lower()
            mountain = Mountain(url, name, dense_url, location)
            mountain_list.append(mountain)
            print(mountain)
    with open('mountains.txt','w') as file:
        json.dump(mountain_list, file, default=mountain_encoder)