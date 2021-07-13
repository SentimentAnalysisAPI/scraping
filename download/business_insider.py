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
    Load(50)

def Load(num):
    driver = webdriver.Chrome(Path("download", "chromedriver", "chromedriver"))
    driver.get("https://www.businessinsider.com/latest#")

    driver.switch_to.frame(driver.find_element_by_id("sp_message_iframe_364840"))
    xpath = "/html/body/div/div[2]/div[6]/div[2]/button"
    button = driver.find_elements_by_xpath(xpath)[0]
    button.click()

    driver.switch_to.default_content()
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    xpath = "//a[text()='View more']"
    button = driver.find_elements_by_xpath(xpath)[0]
    button.click()

    soup = Soup(driver.page_source)
    posts = soup.findAll("section", {"class": "river-item featured-post"})
    print(len(posts))

    while len(posts) < num:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        soup = Soup(driver.page_source)
        posts = soup.findAll("section", {"class": "river-item featured-post"})
        print(len(posts))

    data = [DataJson(post) for post in posts]
    WriteJson("businessinsider.json", data)

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
