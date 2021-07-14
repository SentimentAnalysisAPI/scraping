from utility.file import Path

from bs4 import BeautifulSoup
from selenium import webdriver

def Soup(html, method="html.parser"):
    return BeautifulSoup(html, method)

def Click(driver, xpath):
    elements = driver.find_elements_by_xpath(xpath)
    elements[0].click()
    return elements

def ChromeDriver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(Path("download", "chromedriver", "chromedriver"), options=options)
    return driver