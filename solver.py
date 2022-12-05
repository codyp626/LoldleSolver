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
import sys
import time


global_gender_list = ["Male", "Female", "Other"]
global_positions_list = ["Jungle", "Top", "Middle", "Bottom", "Support"]
global_species_list = ["Minotaur", "Unknown", "Brackern", "Cat", "Troll", "Human", "Revenant", "Undead", "Yordle", "Dragon", "Magically Altered", "Vastayan", "Spiritualist", "Spirit", "God", "Golem", "Demon", "Iceborn", "Magicborn", "Celestial", "Chemically Altered", "Void-Being", "Aspect", "Cyborg", "Rat", "Darkin", "God-Warrior"]
global_resource_list = ["Fury", "Ferocity", "Shield", "Heat", "Grit", "Bloodthirst", "Mana", "Manaless", "Flow", "Energy", "Rage", "Courage", "Health costs"]
global_range_list = ["Ranged", "Melee"]
global_region_list = ["Void", "Icathia", "Ixtal", "Demacia", "Camavor", "Rhaast", "Bilgewater", "Ionia", "Targon", "Noxus", "Runeterra", "Bandle City", "Blessed Isles", "Shadow Isles", "Zaun", "Piltover", "Freljord", "Shurima"]
global_years_list = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

global_right_terms = [None]

list_list = [global_gender_list, global_positions_list, global_species_list, global_resource_list, global_range_list, global_region_list]
class champ:
    def __init__(self, name, gender, positions, species_list, resource, range, regions, year):
        self.name = name
        self.gender = gender
        self.positions = positions
        self.species_list = species_list
        self.resource = resource
        self.range = range
        self.regions = regions
        self.year = year

default_correct_champ = champ(None, global_gender_list, global_positions_list, global_species_list, global_resource_list, global_range_list, global_region_list, global_years_list)

def add_str_if_not_there(str, list):
    if str not in list:
       list.append(str)
       return True
    else:
        return False




def specify_terms(item, term_type, single):
    # this cleans up wrong term boxes
    if term_type == "wrong":
        for list in list_list:
            if item in list:
                list.remove(item)
    if term_type == "right" and single == True:
        for list in list_list:
            if item in list:
                list.clear()
                list.append(item)
    return



# function returns 1 if champ matches, 0 otherwise
def check_champ_against_terms(champ, max_date, min_date):
    if not champ["gender"] in global_gender_list:
        return 0
    for pos in champ["positions"]:
        if not pos in global_positions_list:
            return 0
    for species in champ["species"]:
        if not species in global_species_list:
            return 0
    if not champ["resource"] in global_resource_list:
        return 0
    for range in champ["range_type"]:
        if not range in global_range_list:
            return 0
    for region in champ["regions"]:
        if not region in global_region_list:
            return 0
    if int(champ["release_date"]) > max_date:
        return 0
    if int(champ["release_date"]) < min_date:
        return 0
    return 1

start = time.time()
def main():
    guesses = 0
    max_date = 3000
    min_date = 0
    f = open('champinfo.json')
    champs = json.load(f)
    #web driver setup
    from selenium.webdriver.common.by import By
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
    driver.set_window_size(1920, 1080)
    driver.get("http://www.loldle.net")

    #click the 'classic mode' button
    button = driver.find_element(By.CLASS_NAME, "button-img")
    button.click()
    sleep(1)

    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,ElementNotInteractableException,WebDriverException)
    first_run = True
    # main for loop

    # for champ in champs:
    #     # for species in champ["resource"]:
    #     if not champ["resource"] in global_resource_list:
    #         print("Missing:", champ["resource"])
    # return

    inferior = 0
    superior = 0
    random.shuffle(champs)
    for champ in champs:
        name = champ["championName"]
        date = int(champ["release_date"])
        # print("trying", name)
        # check against known terms
        if not first_run:
            if not check_champ_against_terms(champ, max_date, min_date):
                continue
        # print("champ passed")
        # typing champ name
        try:
            textbox = driver.find_element(By.XPATH, "//input[@placeholder=\"Type champion name ...\"]")
        except ignored_exceptions as Exception:
            continue
        try:
            textbox.send_keys(name)
            textbox.send_keys(Keys.RETURN)
            guesses += 1
        except ignored_exceptions as Exception:
            continue

        sleep(4) # wait for squares to be revealed

        #find and categorize all squares
        red_squares = driver.find_elements(By.CLASS_NAME, 'square-bad')
        green_squares = driver.find_elements(By.CLASS_NAME, 'square-good')
        partial_squares = driver.find_elements(By.CLASS_NAME, 'square-partial')
        inferior_squares = driver.find_elements(By.CLASS_NAME, 'square-inferior')
        superior_squares = driver.find_elements(By.CLASS_NAME, 'square-superior') #guessing here for now

        # handling wrong terms
        for square in red_squares:
            if "\n" in square.text:
                split_list = square.text.split("\n")
                for x in split_list:
                    x = x.replace(',', "")
                    specify_terms(x, "wrong", False)
                    
                    
            else:
                specify_terms(square.text, "wrong", False)

        # handling right terms
        for square in green_squares:
            if "\n" in square.text:
                split_list = square.text.split("\n")
                for x in split_list:
                    x = x.replace(',', "")
                    specify_terms(x, "right", False)
            else :
                specify_terms(square.text, "right", True)

        # handling too recent of dates
        if len(superior_squares) > superior:
            if date > min_date:
                min_date = date
                # print("min date", min_date)
            superior += 1

        # handling too old of dates
        if len(inferior_squares) > inferior:
            if date < max_date:
                max_date = date
                # print("max date", max_date)
            inferior += 1

        # # handling partial terms
        # for square in partial_squares:
        #     if not " " in square.text and not "\n" in square.text and not "," in square.text:
        #         add_str_if_not_there(square.text, right_terms)


        first_run = False
    print("Won in\t",guesses,"\tguesses")
    driver.close()
    # end = start - time.time()

    f.close()

    return

if __name__ == '__main__':
    sys.exit(main())  