import re
import random
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize

pronouns = {
	"you": "i",
	"me": "you",
	"your": "my",
	"my" : "your",
	"are": "am",
	"am": "are",
	"i" : "you",
       "mine":"yours",
	"myself":"yourself",
	"yours":"mine",
	"yourself": "myself"
 
}


possible_responses = {
	r'[Hh](ello|i).*' : ['Hey there!', 'Hello', 'Hi', 'Howdy'],
	r'\b[Ww]hat is your name?\b' : ['My name is Eliza', 'I am Eliza', 'Eliza'],
	r'I am feeling (.*)' : ["Why are you feeling {0}", "Tell me more!", "What made you feel {0}"],
	r'I am (.*)' :["Why are you {0}", "How long for you been {0} for", "What caused you to be {0}"],
	r'(.*)([Hh]appy|[Gg]ood)(.*)' : ["Why are you happy?", "What made you happy?", "Oh, do you have an exciting news?", "Glad to hear that you are in this mood"],
        r'(.*)[Bb]ad(.*)' : ["Why are you feeling bad?", "Did something happened that made you feel like this?"],
	r'(.*)[Ss]ad(.*)' : ["Why are you sad?", "What made you sad?", "Did something happened that caused you to be sad?"],
	r'(.*)[Ss]ick(.*)' : ["Are you getting enough sleep?", "Bowl of soup is the best home remedy!", "Call the doctor if it gets worse"],
	r'(.*)[Ss]tresse?d?(.*)' : ["What is causing you stress?", "Deep breathing relieves stress", "It will be over soon. Just breathe :)"],
        r'(.*)([Ll]onely|[Aa]lone)(.*)': ["Why do you feel Lonely", "What makes you think you are alone "],
        r'(.*)([Ll]oved?)(.*)': ["Why do you feel this way", "What makes you think like this "],
        r'(.*)[Ss]orry (.*)':[" No apology is needed.","Why do you feel to say sorry?"],
        r'(.*)[Aa]lone (.*)':[" Why do you think you are alone?.","You can share with me"],
        r'(.*)[Ff]amily(.*)': ["Tell me more about your family.","Why does it makes you feel this way?"],
        r'(.*)[Ff]ather(.*)': ["How is your relationship with your father?","Tell me more about your relation"],
        r'(.*)[Mm]o(ther|m)(.*)': ["How is your relationship with your mom?","Tell me more about your relation"],
        r'(.*)[Ss]isters?(.*)': ["How is your relationship with your sister?","Tell me more about your relation"],
        r'(.*)[Bb]rothers?(.*)': ["How is your relationship with your brother?","Tell me more about your relation"],
        r'(.*)[Ff]rinds?(.*)': ["How is your relationship with your friends?","Tell me about them"],
        r'(.*)[Yy]es(.*)': ["Thats positive!", " You seem confident about it"],
        r'(.*)[Nn]ot?(.*)': [" I understand", " I guess, it needs time", "There should be a reason behind this"],
        r'(.*)[Hh]ome(.*)': ["Its a safe place, right", "Home is warm"],
        r'(.*)[Cc]omplicated(.*)': ["What does that mean","Why do you think that","Tell me more about it"],
        r'(.*)([Pp]upp(y|ies))': ["The fur buddies are the best buddies", "Ah! So precious!"],
	r'(.*)([Dd]ogs?)': ["The fur buddies are the best buddies", "Ah! So precious!"],
	r'(.*)([Pp]ets?)': ["It's always good to have pets"],
	r'(.*)([Cc]ats?)': ["The fur buddies are the best buddies", "Ah! So precious!"],
	r'(.*)([Kk]ittens?)': ["The fur buddies are the best buddies", "Ah! So precious!"],
	r'(.*)[Yy]ou are (.*)': ["Why do you think I am {0}?", "Why are you asking if I am {0}?", "Do you think I am {0}?"],
	r'(.*)[Yy]ou(.*)': ["We should be talking about you, not me :)", "Let's focus on talking about you!"],
	r'(.*)' : ["Go on!","Tell me more", "let's change the topic", "I can't help, if you don't tell me", " Don't be shy,your secret is safe with me","Take your time, I am there for you"]
		
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
			tokens[i] = pronouns[token]
	
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
