import re
import random
from nltk.tokenize import word_tokenize

pronouns = {
	"you": "i",
	"me": "you",
	"your": "my",
	"my" : "your",
	"are": "am",
	"am": "are",
	"i" : "you"
}

possible_responses = {
	r'[Hh](ello|i).*' : ['Hey there!', 'Hello', 'Hi', 'Howdy'],
	r'\b[Ww]hat is your name?\b' : ['My name is Eliza', 'I am Eliza', 'Eliza'],
	r'I am feeling (.*)' : ["Why are you feeling {0}", "Tell me more!", "What made you feel {0}"],
	r'I am (.*)' :["Why are you {0}", "How long for you been {0} for", "What caused you to be {0}"],
	r'(.*)[Hh]appy(.*)' : ["Why are you happy?", "What made you happy?", "Oh, do you have an exciting news?"],
	r'(.*)[Ss]ad(.*)' : ["Why are you sad?", "What made you sad?", "Did something happened that caused you to be sad?"],
	r'(.*)[Ss]ick(.*)' : ["Are you getting enough sleep?", "Bowl of soup is the best home remedy!", "Call the doctor if it gets worse"],
	r'(.*)[Ss]tresse?d?(.*)' : ["What is causing you stress?", "Deep breathing relieves stress", "It will be over soon. Just breathe :)"],
	r'(.*)([Pp]upp(y|ies))': ["The fur buddies are the best buddies", "Ah! So precious!"],
	r'(.*)([Dd]ogs?)': ["The fur buddies are the best buddies", "Ah! So precious!"],
	r'(.*)([Pp]ets?)': ["It's always good to have pets"],
	r'(.*)([Cc]ats?)': ["The fur buddies are the best buddies", "Ah! So precious!"],
	r'(.*)([Kk]ittens?)': ["The fur buddies are the best buddies", "Ah! So precious!"],
	r'(.*)You are (.*)': ["Why do you think I am {0}?", "Why are you asking if I am {0}?", "Do you think I am {0}?"],
	r'(.*)you(.*)': ["We should be talking about you, not me :)", "Let's focus on talking about you!", "Maybe we should talk about your feelings"],
	r'(.*)' : ["Go on!","Tell me more"]
}
def greeting(name):
	pattern = r'\b[Mm]y name is (.+)\b'
	pattern_2 = r'([A-z].+)'

	x = re.match(pattern,name)
	y = re.match(pattern_2,name)

	if x or y:
		if x:
			return str(x[1])
		if y:
			return str(y[1])
	else:
		return "Incorrect"

def generate_response(user_response):

	for pattern, reponse in possible_responses.items():
		match = re.match(pattern, user_response)
		if match:
			bot_response = random.choice(reponse)
			
			s = ""
			for x in match.groups():
				s = s + " " + x

			#print(s)

			reponse_message = bot_response.format(*[evaluate_pronoun(s)])
			return reponse_message


def evaluate_pronoun(sentence):

	sentence = sentence.lower()
	tokens = word_tokenize(sentence)

	for i, token in enumerate(tokens):
		if token in pronouns:
			print(f"tokens[i] {tokens[i]} before")
			tokens[i] = pronouns[token]
			print(f"tokens[i] {tokens[i]} after")
	print(' '.join(tokens))
	return ' '.join(tokens)

def main():

	correct_name = False
	while not correct_name:
		name = input("Hi, My name is Eliza. What is your name?\n>>")
		greeting_name = greeting(name)
		if greeting_name == "Incorrect":
			correct_name = False
			print("Lets try that again!")
		else:
			correct_name = True
	message = input(f"Hello {greeting_name}, How are you feeling today?\n>>")
	
	while message != 'quit':
		response_question = generate_response(str(message))
		message = input(f"{response_question}\n>>")

main()
