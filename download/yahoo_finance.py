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
from utility.file import WriteJson
from utility.web import Soup

import json
import re
import requests

def DataJson():
	### https://youtu.be/fw4gK-leExw
	response = requests.get("https://finance.yahoo.com/")
	soup = Soup(response.text)
	pattern = re.compile(r"\s--\sData\s--\s")
	data = soup.find("script", text=pattern).contents[0].strip()
	data = json.loads(data[data.find("context") - 2:-11])
	return data

if __name__ == '__main__':
	data = DataJson()
	# PrintJson(data)
	# WriteJson("yahoo_finance_data.json", data)