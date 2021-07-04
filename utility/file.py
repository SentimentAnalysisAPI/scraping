import json

def WriteJson(path, jsonObject):
	with open(path, "w") as f:
		f.write(json.dumps(jsonObject, indent=4))