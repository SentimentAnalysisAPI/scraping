import json
import os
import sys

def PrintJson(jsonObject):
	print(json.dumps(jsonObject, indent=4))

class Mute:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def bar(total):
    import alive_progress
    return alive_progress.alive_bar(total, manual=False, bar="classic", spinner="classic")