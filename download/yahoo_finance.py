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
from utility.file import ReadJson, WriteJson
from utility.web import Soup


import json
import re
import requests
from datetime import datetime
import pytz

def DataJson():
    ### https://youtu.be/fw4gK-leExw
    response = requests.get("https://finance.yahoo.com/")
    soup = Soup(response.text)
    pattern = re.compile(r"\s--\sData\s--\s")
    data = soup.find("script", text=pattern).contents[0].strip()
    start = data.find("context") - 2
    end = -11
    data = json.loads(data[start:end])
    return data
"""
def DataJson_2():
    ### https://youtu.be/fw4gK-leExw
    response = requests.get("https://finance.yahoo.com/")
    soup = Soup(response.text)
    pattern = re.compile(r"Data\s--\s")
    data_2 = soup.find("script", text=pattern).contents[0].strip()
    start = data_2.find("context") - 2
    end = -11
    data_2 = json.loads(data_2[start:end])
    return data_2
"""
data = DataJson()

#data_2 = DataJson_2()

Yahoo_data = []
root_to_data = data["context"]["dispatcher"]["stores"]["StreamStore"]["streams"]["mega.c"]["data"]["stream_items"]

def DataYahoo():
    for entry in root_to_data:

        infos = {
        #    "summary": entry["summary"],
        #    "pubtime": entry["pubtime"],
        #    "categoryLabel": entry["categoryLabel"],
            "title": entry["title"],
        #    "stockTickers": entry["finance"]["stockTickers"]

            }

        Yahoo_data.append(infos)


    return Yahoo_data

if __name__ == '__main__':
    infos = DataYahoo()
    PrintJson(Yahoo_data)
    WriteJson("yahoo_finance_data.json", data)
    #("yahoo_finance_data_2.json", data_2)
