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

    print("Downloading posts from 'Business Insider'")
    data["businessInsider"] = BusinessInsider()

    ### Reddit not working as expected and slow
    # print("Downloading posts from 'Reddit'")
    # data["reddit"] = Reddit()

    print("Downloading posts from 'Yahoo Finance'")
    data["yahooFinance"] = YahooFinance()

    MakeFolder(Path("data"))
    WriteJson(Path("data", f"{int(time.time())}.json" ), data)

if __name__ == '__main__':
    DownloadManager()