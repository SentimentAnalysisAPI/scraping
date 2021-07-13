if __name__ == '__main__':
    ### adding FinancialSentiment directory to path
    import sys
    import os
    path = os.path.abspath(__file__)
    name = "FinancialSentiment"
    index = path.rfind(name) + len(name)
    path = path[:index]
    sys.path.append(path)

from utility.display import PrintJson
from utility.file import Path, ReadSoup, WriteJson, WriteSoup
from utility.web import Click, Soup

from selenium import webdriver
import time
import datetime

def Main():
    Load()

def Load():
    driver = webdriver.Chrome(Path("download", "chromedriver", "chromedriver"))
    driver.get("https://finance.yahoo.com/")

    xpath = "//button[@type='submit' and @name='agree' and @value='agree']"
    button = driver.find_elements_by_xpath(xpath)[0]
    button.click()

    soup = Soup(driver.page_source)
    posts = soup.findAll("li", {"class": "js-stream-content Pos(r)"})
    print(len(posts))

    previous = 0
    while len(posts) < 150 or not previous == len(posts):
        previous = len(posts)
        driver.execute_script("window.scrollTo(0, 100000);")
        soup = Soup(driver.page_source)
        posts = soup.findAll("li", {"class": "js-stream-content Pos(r)"})
        print(len(posts))

    while True:
        pass
    # data = [DataJson(post) for post in posts]
    # WriteJson("businessinsider.json", data)

def DataJson(post):
    try:
        return {
            "title": post.find("a", {"class": "tout-title-link"}).text.strip(),
            "timestamp": Timestamp(post.find("span", {"class": "tout-timestamp headline-regular js-date-format js-rendered"}).text.strip()),
            "category": post.find("a", {"class": "tout-tag-link headline-bold"}).text.strip(),
            "text": post.find("div", {"class": "tout-copy river body-regular"}).text.strip()
        }
    except: return {}

### timeText format like "1 minute ago" or "10 hours ago"
def Timestamp(timeText):
    timestamp = time.time()
    num, kind = timeText.split()[:2]
    num = int(num)
    if kind in ["second", "seconds"]:
        multiple = 1
    elif kind in ["minute", "minutes"]:
        multiple = 60
    elif kind in ["hour", "hours"]:
        multiple = 3600
    elif kind in ["day", "days"]:
        multiple = 3600 * 24
    else:
        # "Jul 9, 2021, 8:03 PM"
        delta = 1
    return int(timestamp + num * multiple)

if __name__ == '__main__':
    Main()