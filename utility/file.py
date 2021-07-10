import json
import os

def ReadJson(path):
	with open(path, "r") as f:
		return json.loads(f.read())

def ReadSoup(path):
	from utility.web import Soup
	with open(path, "r") as f:
		return Soup(f.read())

def WriteJson(path, jsonObject):
	with open(path, "w") as f:
		f.write(json.dumps(jsonObject, indent=4))

def WriteSoup(path, soup):
	with open(path, "w") as f:
	    f.write(soup.prettify())

def MakeFolder(path):
	if not os.path.exists(path): os.mkdir(path)