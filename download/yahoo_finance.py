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
from utility.file import Path, ReadJson, ReadSoup, WriteJson, WriteSoup
from utility.web import Click, Soup

from selenium import webdriver
import time
import datetime

def YahooFinance():
    posts = Load()
    return posts

def Load():
    driver = webdriver.Chrome(Path("download", "chromedriver", "chromedriver"))
    driver.get("https://finance.yahoo.com/")

    xpath = "//button[@type='submit' and @name='agree' and @value='agree']"
    button = driver.find_elements_by_xpath(xpath)[0]
    button.click()

    # soup = Soup(driver.page_source)
    # posts = soup.findAll("li", {"class": "js-stream-content Pos(r)"})
    # print(len(posts))

    posts = []

    previous = 0
    while len(posts) < 150 or not previous == len(posts):
        previous = len(posts)
        driver.execute_script("window.scrollTo(0, 100000);")
        soup = Soup(driver.page_source)
        posts = soup.findAll("li", {"class": "js-stream-content Pos(r)"})
        print(len(posts))

    soup = Soup(driver.page_source)
    # WriteSoup("full.html", soup)

    # if not os.path.exists("test"): os.mkdir("test")
    # for i, post in enumerate(posts): WriteSoup(Path("download", "test", f"{str(i).zfill(3)}.html"), post)

    posts = [DataJson(post) for post in posts]
    posts = list(filter(None, posts))
    # WriteJson("posts.json", posts)
    return posts

def DataJson(post):
    try:
        if len(post.findAll("a", {"target": "_blank"})) > 0: return {}
        return {
            "title": post.find("h3").text.strip(),
            "timestamp": Timestamp(post.find("div", {"class": "C(#959595) Fz(11px) D(ib) Mb(6px)"}).contents[2].text.strip()),
            "category": post.find("div", {"data-test-locator": "catlabel"}).text.strip(),
            "text": post.find("p").text.strip()
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
    posts = YahooFinance()
    PrintJson(posts)