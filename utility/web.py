from bs4 import BeautifulSoup

def Soup(html, method="html.parser"):
	return BeautifulSoup(html, method)