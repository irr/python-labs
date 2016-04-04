import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")

facebookUsername = os.getenv("FBUSER")
facebookPassword = os.getenv("FBPASS")

emailFieldID = "email"
passFieldID = "pass"
loginButtonXpath = "//input[@value='Log In']"
facebookLogo = "/html/body/div/div[1]/div/div/div/div[1]/div/h1/a"

emailFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(emailFieldID))
passFieldElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_id(passFieldID))
loginButtonElement = WebDriverWait(driver, 10).until(lambda driver: driver.find_element_by_xpath(loginButtonXpath))

emailFieldElement.clear()
emailFieldElement.send_keys(facebookUsername)
passFieldElement.clear()
passFieldElement.send_keys(facebookPassword)
loginButtonElement.click()

WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath(facebookLogo))

print(dir(driver))
