import nltk

# nltk.download()


def Main(text):
	words = SentenceWords(text)
	words = FilterSentenceWords(words)
	words = StemSentenceWords(words)
	print(words)

def Words(text):
	return nltk.tokenize.word_tokenize(text)

def Sentences(text):
	return nltk.tokenize.sent_tokenize(text)

def SentenceWords(text):
	return [Words(sentence) for sentence in Sentences(text)]

def StopWords(language="english"):
	return nltk.corpus.stopwords.words(language)

def FilterWords(words, stopWords=StopWords()):
	return list(filter(lambda word: word not in stopWords, words))

def FilterSentenceWords(sentenceWords, stopWords=StopWords()):
	return [FilterWords(words, stopWords) for words in sentenceWords]

def Stemmer():
	return nltk.stem.PorterStemmer()

def Stem(word, stemmer=Stemmer()):
	return stemmer.stem(word)

def StemWords(words, stemmer=Stemmer()):
	return [Stem(word, stemmer) for word in words]

def StemSentenceWords(sentenceWords, stemmer=Stemmer()):
	return [StemWords(words, stemmer) for words in sentenceWords]

def PosTagWord(word):
	return nltk.pos_tag([word])

def PosTagWords(words):
	return [PosTagWord(word) for word in words]

if __name__ == '__main__':
	text = "These are short, famous texts in English from classic sources like the Bible or Shakespeare. Some texts have word definitions and explanations to help you. Some of these texts are written in an old style of English. Try to understand them, because the English that we speak today is based on what our great, great, great, great grandparents spoke before! Of course, not all these texts were originally written in English. The Bible, for example, is a translation. But they are all well known in English today, and many of them express beautiful thoughts."
	Main(text)
