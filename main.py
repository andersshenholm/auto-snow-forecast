from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import json
from util import Mountain, number_value, mountain_list, home_mountain_list
from config import * #includes user-specific variables home_mountains and units

#needs:
#commit on thursday

'''
summary: gives total snow forecast for a given mountain and number of days into the future
args:
    - mountain: Mountain
    - days: int
other inputs:
    - inches: boolean config variable indicating snow forecasted as in. vs cm.
returns: none
notes: assumes valid input of a Mountain matching a US resort and an integer number of days 1-7
'''
def snow_total(mountain, days):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    print(str(days) + " day forecast for " + mountain.name + "...")
    driver.get(f"https://www.snow-forecast.com/resorts/{mountain.url}/6day/mid")
    snow_boxes = driver.find_elements(By.XPATH, "//div[@class='snow-amount']")
    snow_total = 0 
    for i, item in enumerate(snow_boxes):
        if i > days * 3:
            break
        snow_total += number_value(item.get_attribute('data-value'))
    driver.quit()

    if inches == True:
        snow_total *= 0.39
        print (str(round(snow_total, 1)) + " inches")
    else:
        print (str(round(snow_total, 1)) + " centimeters")
    return 

'''
summary: Matches user input to mountain in mountain_list
args: 
    - s1: user input to be matched with a moutain
other inputs: 
    - mountain_list: global list of US mountains (type Mountain)
returns:
    - selected_mountain: Mountain matched to user input 
notes: Mountain selection compares alphanumeric input characters to alphanumeric mountain name (case insensitive). 
The strings match when the input string (alnum) exists anywhere in the mountain url-> i.e. 'ove.la' matches 'Loveland'
At the moment, the regex doesn't account for '_' in input
'''
def find_mountain_from_input(s1):
    candidate_mountains = []
    selected_mountain = None
    dense_input = re.sub(r'\W+', '', s1, flags=re.A).lower()
    for item in mountain_list:
        if dense_input in item.dense_url:
            candidate_mountains.append(item)

    if len(candidate_mountains) < 1:
        print("No matching mountains found")
    elif len(candidate_mountains) == 1:
        selected_mountain = candidate_mountains[0]
    else:
        s2 = "Indicate with a number which mountain you wanted.\n"
        for i in range (0, len(candidate_mountains)):
            s2 += str(i+1) + ". " + candidate_mountains[i].name + ": " + candidate_mountains[i].location + "\n"
        while True:
            choice = input(s2)  
            try:
                choice = int(choice)
                selected_mountain = candidate_mountains[int(choice)-1]
                return selected_mountain
            except:
                print("Input out of range or could not be interpreted, please try again")
        
    return selected_mountain
'''
summary: Parses user input for a valid number of forecast days
args: 
    - s1: user input to be parsed
other inputs: none
returns:
    - days: number of forecast days parsed from input
'''
def find_days_from_input(s1):
    days = 0
    try:
        days = int(s1)
    except:
        print("Please enter an integer number of days")
        return 0
    if days >= 7 or days <= 0:
        print("Please enter a day range from 1 to 7")
        return 0
    return days

'''
summary: checks forecasts for user-selected home mountains
args: none
other inputs:
    - home_mountain_list: list of user's home mountains gathered from home_mountains.txt
    - home_mountain_forecast_days: number of forecast days 1-7, set in config
returns: none
notes: assumes correctly formatted and up to date mountain data in home_mountains_list (from home_mountains.txt).
assumes home_mountain_forecast_days is an integer 1-7
'''
def home_mountain_forecast():
    for i in home_mountain_list:
        snow_total(i, home_mountain_forecast_days)  
    return
'''
summary: CURRENTLY UNUSED - prompts user for a mountain and number of days then finds that forecast
args: none
other inputs: 
    - user-selected mountain
    - user-selected number of forecast days
returns: none
notes: prompt-based forecast system that was used in the begining of development
'''
def select_mountain():
    selection = ""
    days = 0
    while (selection == None):
        selection = find_mountain_from_input(input("Which mountain do you want a snow forecast for?\n"))
    while (days == 0):  
        days = find_days_from_input(input("How many days in the future do you want forecast for (limit 7)"))
    snow_total(selection, days)
    return

'''
summary: simple command line prompt loop that allows user to get home mountain or specifc mountain forecasts
args: none
other inputs: 
    - user commands help, h/home, as f/forecast as well as other unusable input
returns: none
notes: for f/forecast, the shell checks for validity of days input before parsing mountain input so that user doesn't go through mountain selection
to then realize their days input is invalid. This is probably less intuitive if user has both inputs wrong, but keeping this as simple soln for now.
At the moment, the shell can only handle mountains as unbroken strings (i.e. 'winterpark' matches correctly but 'winter park' doesn't)     
'''

def shell():
    while(True):
        args = input('> ').split()
        if args[0] == 'help':
            print('Current supported commands:\nh, home - snow forecast for home mountains\nf, forecast [mountain] [days] - snow forecast for specified mountain for chosen number of days (1-7)\n')
        elif args[0] == 'h' or args[0] == 'home':
            home_mountain_forecast()
        elif len(args) > 2 and (args[0] == 'f' or args[0] == 'forecast'):
            days = find_days_from_input(args[2])
            if days == 0:
                pass
            else: 
                mountain = find_mountain_from_input(args[1])    
                if mountain == None:
                    pass
                else:
                    snow_total(mountain, days)
        else:
            print('Couldn\'t interpret input. Use "help" command for more information.')


def main():
    shell()

if __name__ == "__main__":
    main()