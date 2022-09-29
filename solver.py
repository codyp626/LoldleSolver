from time import sleep
from time import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.get("http://www.loldle.net/classic")

button = driver.find_element(By.CLASS_NAME, "button-img")
button.click()
sleep(1)

file = open('champs.txt')
champs = file.read().split(',')

ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)

for name in champs:
    try:
        textbox = driver.find_element(By.XPATH, "//input[@placeholder=\"Type champion name ...\"]")
    except NoSuchElementException as Exception:
        print("you win")
    
    try:
        textbox.send_keys(name)
        textbox.send_keys(Keys.RETURN)
    except StaleElementReferenceException as Exception:
        print("you win")
    except ElementNotInteractableException as Exception:
        print("you win")


sleep(10)
driver.close()