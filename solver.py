from lib2to3.pgen2.token import NEWLINE
import random
from time import sleep, strptime
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
    
def check_terms():
    if strptime(date, "%Y-%m-%d") > max_date:
        return 0
    if strptime(date, "%Y-%m-%d") < min_date:
        return 0
    if "Jungle" in right_terms or "Top" in right_terms or "Middle" in right_terms or "Bottom" in right_terms or "Support" in right_terms:
        for pos in positions:
            if pos not in right_terms:
                return 0
    if "Human" in right_terms or "Revenant" in right_terms or "Undead" in right_terms or "Yordle" in right_terms or "Dragon" in right_terms or "Magically Altered" in right_terms or "Vastayan" in right_terms or "Spiritualist" in right_terms or "Spirit" in right_terms or "God" in right_terms or "Golem" in right_terms or "Demon" in right_terms or "Iceborn" in right_terms or "Magicborn" in right_terms or "Celestial" in right_terms or "Chemically Altered" in right_terms or "Void-Being" in right_terms or "Aspect" in right_terms or "Cyborg" in right_terms or "Rat" in right_terms or "Darkin" in right_terms or "God-Warrior" in right_terms:
        for species in specieses:
            if species not in right_terms:
                return 0
    if "Female" in right_terms or "Male" in right_terms or "Other" in right_terms:
        if gender not in right_terms:
            return 0
    if "Ranged" in right_terms or "Melee" in right_terms:
        for range in ranges:
            if range not in right_terms:
                return 0
    if "Mana" in right_terms or "Manaless" in right_terms or "Flow" in right_terms or "Energy" in right_terms or "Rage" in right_terms or "Courage" in right_terms:
        if resource not in right_terms:
            return 0
    if "Runeterra" in right_terms or "Bandle City" in right_terms or "Shadow Isles" in right_terms or "Zaun" in right_terms or "Piltover" in right_terms:
        for region in regions:
            if region not in right_terms:
                return 0
    
    # status = 1
    if gender in wrong_terms:
        return 0
    for pos in positions:
        if pos in wrong_terms:
            return 0
    for species in specieses:
        if species in wrong_terms:
            return 0
    if resource in wrong_terms:
        return 0
    for range in ranges:
        if range in wrong_terms:
            return 0
    for region in regions:
        if region in wrong_terms:
            return 0
    # if gender in right_terms:
    #     status = 1
    # for pos in positions:
    #     if pos in right_terms:
    #         status = 1
    # for species in specieses:
    #     if species in right_terms:
    #         status = 1
    # if resource in right_terms:
    #     status = 1
    # for range in ranges:
    #     if range in right_terms:
    #         status = 1
    # return status

    # not in wrong terms
    # or in right terms
    # 
    return 1


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

# huge strings list
wrong_terms = []
right_terms = []

before_dates = []
after_dates = []
max_date = strptime("2050-01-01", "%Y-%m-%d")
min_date = strptime("1000-01-01", "%Y-%m-%d")


first_run = True
# main for loop

specieslist = []


random.shuffle(champs)
for champ in champs:
    score = 0
    name = champ["championName"]
    gender = champ["gender"]
    positions = champ["positions"]
    specieses = champ["species"]
    resource = champ["resource"]
    ranges = champ["range_type"]
    regions = champ["regions"]
    date = champ["release_date"]

    # big ass check against known terms
    if not first_run:
        if not check_terms():
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
                x = x.replace(',', "")
                add_str_if_not_there(x, wrong_terms)
        else:
             add_str_if_not_there(square.text, wrong_terms)

    # handling right terms
    for square in green_squares:
        if "\n" in square.text:
            split_list = square.text.split("\n")
            for x in split_list:
                x = x.replace(',', "")
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

    first_run = False
    print("wrong: ", wrong_terms)
    print("right: ", right_terms, "\n")
# wait 40 seconds
print("you win!")
sleep(30)
driver.close()
exit()