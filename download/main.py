if __name__ == '__main__':
    ### adding FinancialSentiment directory to path
    import sys
    import os
    path = os.path.abspath(__file__)
    name = "FinancialSentiment"
    index = path.rfind(name) + len(name)
    path = path[:index]
    sys.path.append(path)

from download.business_insider import BusinessInsider
from download.reddit import Reddit
from download.yahoo_finance import YahooFinance
from utility.file import MakeFolder, Path, WriteJson

import time

def DownloadManager():
    data = {}

    name = "Business Insider"
    print(f"Downloading", name, "posts")
    data["businessInsider"] = BusinessInsider()
    print("Downloaded", len(data["businessInsider"]), "posts")

    ### Reddit not working as expected and slow
    # print("Downloading posts from 'Reddit'")
    # data["reddit"] = Reddit()

    name = "Yahoo Finance"
    print(f"Downloading", name, "posts")
    data["yahooFinance"] = YahooFinance()
    print("Downloaded", len(data["yahooFinance"]), "posts")

    MakeFolder(Path("data"))
    WriteJson(Path("data", f"{int(time.time())}.json" ), data)

if __name__ == '__main__':
    DownloadManager()