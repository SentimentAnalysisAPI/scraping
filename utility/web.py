from bs4 import BeautifulSoup

def Soup(html, method="html.parser"):
	return BeautifulSoup(html, method)

def Click(driver, xpath):
	elements = driver.find_elements_by_xpath(xpath)
	elements[0].click()
	return elements