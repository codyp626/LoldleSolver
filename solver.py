from time import sleep, strptime
from turtle import right
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import WebDriverException

import json


def add_str_if_not_there(str, list):
    if str not in list:
       list.append(str)
       return True
    else:
        return False
    


with open('champinfo.json') as f:
    champs = json.load(f)


#web driver setup
from selenium.webdriver.common.by import By
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.get("http://www.loldle.net")

#click the 'classic mode' button
button = driver.find_element(By.CLASS_NAME, "button-img")
button.click()
sleep(1)

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException,WebDriverException)

box_offset = 9 #offset to find correct boxes

# huge strings list
wrong_terms = []
right_terms = []

before_dates = []
after_dates = []
Flag = False
max_date = strptime("2050-01-01", "%Y-%m-%d")
min_date = strptime("1000-01-01", "%Y-%m-%d")


first_run = True
# main for loop
for champ in champs:
    score = 0
    name = champ["championName"]
    gender = champ["gender"]
    positions = champ["positions"]
    specieses = champ["species"]
    resources = champ["resource"]
    ranges = champ["range_type"]
    regions = champ["regions"]
    date = champ["release_date"]

# big ass check against known terms
    if not first_run:
        if strptime(date, "%Y-%m-%d") > max_date:
            continue
        if strptime(date, "%Y-%m-%d") < min_date:
            continue
        if gender not in right_terms:
            continue
        for pos in positions:
            if pos in wrong_terms:
                flag = True
                break
        for species in specieses:
            if species in wrong_terms:
                flag = True
                break
        for resource in resources:
            if resource in wrong_terms:
                flag = True
                break
        for range in ranges:
            if range in wrong_terms:
                flag = True
                break
        for region in regions:
            if region in wrong_terms:
                flag = True
                break
        if flag:
            flag = False
            continue


# typing champ name
    try:
        textbox = driver.find_element(By.XPATH, "//input[@placeholder=\"Type champion name ...\"]")
    except ignored_exceptions as Exception:
        continue
    try:
        textbox.send_keys(name)
        textbox.send_keys(Keys.RETURN)
    except ignored_exceptions as Exception:
        continue

    sleep(4) # wait for squares to be revealed

    #find and categorize all squares
    red_squares = driver.find_elements(By.CLASS_NAME, 'square-bad')
    green_squares = driver.find_elements(By.CLASS_NAME, 'square-good')
    partial_squares = driver.find_elements(By.CLASS_NAME, 'square-partial')
    inferior_squares = driver.find_elements(By.CLASS_NAME, 'square-inferior')
    superior_squares = driver.find_elements(By.CLASS_NAME, 'superior-inferior') #guessing here for now

# handling wrong terms
    for square in red_squares:
        if "\n" in square.text:
            split_list = square.text.split("\n")
            for x in split_list:
                add_str_if_not_there(x, wrong_terms)           
        else:
             add_str_if_not_there(square.text, wrong_terms)

# handling right terms
    for square in green_squares:
        if "\n" in square.text:
            split_list = square.text.split("\n")
            for x in split_list:
                add_str_if_not_there(x, right_terms)
        else :
            add_str_if_not_there(square.text, right_terms)

# handling too recent of dates
    for square in inferior_squares:
        date = champ["release_date"]
        date = strptime(date, "%Y-%m-%d")
        if date < max_date:
            max_date = date

# handling too old of dates
    for square in superior_squares:
        date = champ["release_date"]
        date = strptime(date, "%Y-%m-%d")
        if date > min_date:
            min_date = date

    
    # box_position = boxes[box_offset+1].text
    # print("right terms: ", right_terms)
    # print("wrong terms: ", wrong_terms)

    # except ignored_exceptions as Exception:
        # print("caught box exception")
    box_offset += 8
    first_run = False

# wait 40 seconds
print("you win!")
sleep(10)
driver.close()
exit()