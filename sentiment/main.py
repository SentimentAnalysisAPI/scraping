if __name__ == '__main__':
    ### adding FinancialSentiment directory to path
    import sys
    import os
    path = os.path.abspath(__file__)
    name = "FinancialSentiment"
    index = path.rfind(name) + len(name)
    path = path[:index]
    sys.path.append(path)

from utility.display import bar, PrintJson
from utility.file import Path, ReadJson, WriteJson

import concurrent.futures
import itertools

def main():
	data = ReadJson(Path("data", "1629311471.json"))["yahooFinance"]
	with bar(len(data)) as b:
		with concurrent.futures.ThreadPoolExecutor() as executor:
			future = executor.map(thread, data, itertools.repeat(b))
			WriteJson("yahoo_finance_text.json", list(future))

def thread(item, b):
	result = {
		"text": item["text"],
		"sentiment": {
			"vader": round(sentiment_nltk_vader(item["text"]), 3),
			"textblob": round(sentiment_textblob_polarity(item["text"]), 3),
			"flair": round(sentiment_flair(item["text"]), 3)
		}
	}
	b()
	return result

def sentiment_vader(text):
	from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
	analyzer = SentimentIntensityAnalyzer()
	return analyzer.polarity_scores(text)["compound"]

def sentiment_nltk(text):
	from nltk.sentiment import SentimentAnalyzer

def sentiment_nltk_vader(text):
	from nltk.sentiment.vader import SentimentIntensityAnalyzer
	analyzer = SentimentIntensityAnalyzer()
	return analyzer.polarity_scores(text)["compound"]

def sentiment_textblob_polarity(text):
	from textblob import TextBlob
	statement = TextBlob(text)
	return statement.sentiment.polarity

# def sentiment_textblob_classify(text):
# 	from textblob import TextBlob
# 	statement = TextBlob(text)
# 	return statement.classify()

def sentiment_flair(text):
	from flair.models import TextClassifier
	from flair.data import Sentence
	classifier = TextClassifier.load("en-sentiment")
	sentence = Sentence(text)
	classifier.predict(sentence)
	score = sentence.labels[0].to_dict()["confidence"]
	return score if sentence.labels[0].to_dict()["value"] == "POSITIVE" else -score

# def sentiment_spacy(text):
#	import spacy
# 	### python -m spacy download en
# 	nlp = spacy.load("en_core_web_sm")
# 	doc = nlp("Apple is looking at buying U.K. startup for $1 billion")
# 	for token in doc:
# 	    print(token.text)

if __name__ == '__main__':
	main()