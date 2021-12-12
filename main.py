
import nltk
import random
import string
import sys
import nltk

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from classes_dict import *

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def lem_tokens(tokens):

	lemmer = nltk.stem.WordNetLemmatizer()

	return [lemmer.lemmatize(token) for token in tokens]

def lem_normalize(text):
	return lem_tokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


def my_response(my_dict, user_input, sent_tokens):

	robo_response = ''

	#sent_tokens.append(user_response)
	sent_tokens['user'] = user_input

	sent_tokens_ = []

	for value in sent_tokens:
		sent_tokens_.append(sent_tokens[value])

	# tfidf_vec = TfidfVectorizer(tokenizer = lem_normalize, stop_words='english')
	tfidf_vec = TfidfVectorizer(tokenizer = lem_normalize)

	tfidf = tfidf_vec.fit_transform(sent_tokens_)
	vals = cosine_similarity(tfidf[-1], tfidf)
	idx = vals.argsort()[0][-2]
	flat = vals.flatten()
	flat.sort()
	req_tfidf = flat[-2]
	# print req_tfidf

	error_threshold = 0.1
	if(req_tfidf < error_threshold):
		robo_response = ["[No Suggestion]"]
		return robo_response

	else:
		for value in sent_tokens:
			match_pattern = sent_tokens_[idx]
			pattern = sent_tokens[value]
			if match_pattern == pattern:
					match_class = value

		# print match_class
		robo_response = my_dict[match_class]['response']
		return robo_response

def post_dict(some_dict):

	sent_tokens = {}

	for value in some_dict:
		words = some_dict[value]["pattern"]
		words = ' '.join(words)
		sent_tokens[value] = words
		word_tokens = nltk.word_tokenize(words)

	return sent_tokens, word_tokens

sent_tokens, word_tokens = post_dict(classes_dict)

print("* Hello! Type in a message and I will suggest some replies! If you'd like to exit please type quit!")

flag = True

while flag:

	user_input = input('>>> ').lower()

	if(user_input != "quit"):

		response = my_response(classes_dict, user_input, sent_tokens)

		for i in range(0, len(response)):
			print('* ' + response[i])

		  # sent_tokens.remove(user_input)
		del sent_tokens['user']

	else:

		flag = False
