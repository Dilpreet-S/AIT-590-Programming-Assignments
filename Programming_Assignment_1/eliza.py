import re
import random
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

global last_response
pronouns = {
	"you": "me",
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
	r'[Ii] am feeling (.*)' : ["Why are you feeling {0}", "Tell me more!", "What made you feel {0}"],
	r'[Ii] am (.*)' :["Why are you {0}", "How long for you been {0} for", "What caused you to be {0}"],
	r'[Ii] had an?(.*)' :["Tell me more about the {0}", "How did you have {0}"],
	r'[Ii] have (.*)' : ["Why do you have {0}", "How did you get {0}", "Who/what gave you {0}"],
	r'[Ii] would (.*)' : ["Why would you {0}"],
	r'[Ii]t is (.*)' : ["Why is it {0}", "Is it really {0}?"],
	r'(.*)[Ll]et us (.*)' : ["Why do you want to {0}", "What is making you want to {0}?"],
	r'(.*)[Hh]omework(.*)': ["What class are you taking?", "Are your classes hard?", "Which university/school do you attend?"],
	r'(.*)[Hh]appy(.*)' : ["Why are you happy?", "What made you happy?", "Oh, do you have an exciting news?"],
	r'(.*)[Gg]ood(.*)' : ["Glad to hear", "Always love good feelings", "Always good to be good :)", "Oh yeah! Good!"],
    r'(.*)[Bb]ad(.*)' : ["Why are you feeling bad?", "Did something happened that made you feel like this?"],
	r'(.*)[Ss]ad(.*)' : ["Why are you sad?", "What made you sad?", "Did something happened that caused you to be sad?"],
	r'(.*)[Ss]ick(.*)' : ["Are you getting enough sleep?", "Bowl of soup is the best home remedy!", "Call the doctor if it gets worse"],
	r'(.*)[Ss]tresse?d?(.*)' : ["What is causing you stress?", "Deep breathing relieves stress", "It will be over soon. Just breathe :)"],
	r'(.*)([Pp]upp(y|ies))': ["The fur buddies are the best buddies", "Ah! So precious!"],
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
	r'(.*)[Bb]ecause of (.*)':["Do you want to talk more about that"],
    r'(.*)[Aa]lways (.*)':["Can you think of a specific example?"],
    r'(.*)[Ff]avorite(.*)' : ["speaking of favorites... I'd like to learn more about you"],
    r'(.*)[Ss]uffering(.*)' : ["How can I help you?", "Do you need any help?"],
    r'(.*)[Yy]es(.*)': ["Thats positive!", " You seem confident about it"],
    r'(.*)[Hh]ow(.*)': ["What do you think?", "Why do you ask?"],
    r'(.*)[Nn]ot?(.*)': ["Are you sure", " I guess, it needs time", "There should be a reason behind this"],
    r'(.*)[Hh]ome(.*)': ["Its a safe place, right", "Home is warm"],
    r'(.*)[Cc]omplicated(.*)': ["What does that mean","Why do you think that","Tell me more about it"],
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
	r'(.*)[Yy]ou(.*)': ["We should be talking about you, not me :)", "Let's focus on talking about you!", "Maybe we should talk about your feelings"],
	r'(.*)' : ["Go on!","Tell me more"]
}

def greeting():
	correct_name = False
	name = ""
	while not correct_name:
		while name == "":
			greeting_message = "\n***************************************************\n"
			greeting_message += "Hello! Welcome to student psychology services\n"
			greeting_message += "Please feel free to express yourself\n"
			greeting_message += "Please enter 'quit' if you wish to discontinue at any point\n"
			greeting_message += "***************************************************\n"
			print(greeting_message)
			name = input("Hi, My name is Eliza. What is your name?\n>>")
			name = str(name.strip())
			
			quit_pattern = r'[Qq]uit;?'
			quit = re.match(quit_pattern,name)

			if name == "":
				print("Please give me your name! :)")
				continue
			#elif name != 'quit' and name != 'Quit':
			elif not quit:
				greeting_name = greeting_validation(name, check_y=True)
				if greeting_name == "Incorrect":
					correct_name = False
					print("Lets try that again!")
				else:
					correct_name = True
			else:
				#print("Thank you for visiting")
				bye()
				exit()
	message = ""
	while message == "":
		message = input(f"Hello {greeting_name}, How are you feeling today?\n>>")
		if message == "":
			print("You have to tell me how you feel! :)")
	return message

def greeting_validation(name, check_y):
	#pattern = r'\b[Mm]y name is (.+)\b'

	name_count = name.split()

	if (len(name_count) > 1):
		pattern = r'\b[Mm]y name is\b ([A-z].+)'
		x = re.match(pattern,name)
		if x:
			return str(x[1])
		else:
			return "Incorrect"
	else:
		if check_y:
			#print("At y")
			pattern_2 = r'\b([A-z]+)\b'
			y = re.match(pattern_2,name)
			if y:
				return str(y[1])
			else:
				return "Incorrect"

def replace_punctuation(user_response):

	had_pattern = r'[Ii]\'d an?'
	user_response = str(user_response)
	user_response = re.sub(r'[Ii]\'m', "I am", user_response)
	if re.match(had_pattern,user_response):
		user_response = re.sub(r'[Ii]\'d', "I had", user_response)
	else:
		user_response = re.sub(r'[Ii]\'d', r"I would", user_response)
	user_response = re.sub(r'[Ii]\'ve', "I have", user_response)
	user_response = re.sub(r"[Ii]t\'s", "It is", user_response)
	user_response = re.sub(r'[Ll]et\'s', "Let us", user_response)
	print(user_response)

	return user_response

def generate_response(user_response,last_response):

	valid_status = check_validity(user_response)
	user_response = replace_punctuation(user_response)
	#print(f"valid_status {valid_status}")
	if valid_status == "valid":

		for pattern, reponse in possible_responses.items():
			match = re.match(pattern, user_response)
			if match:
				bot_response = random.choice(reponse)
				
				s = ""
				for x in match.groups():
					s = s + " " + x

				reponse_message = bot_response.format(*[evaluate_pronoun(s)])
				return reponse_message
	else:
		#print("at else")
		reponse_message = valid_status #+ "\n" + last_response
		return reponse_message


def evaluate_pronoun(sentence):

	sentence = sentence.lower()
	tokens = word_tokenize(sentence)

	for i, token in enumerate(tokens):
		if token in pronouns:
			tokens[i] = pronouns[token]
	
	return ' '.join(tokens)

def check_validity(message):
	valid_message = "valid"
	message_1 = message.strip()
	greeting_check = greeting_validation(message, check_y=False)
	#print(f"greeting_check {greeting_check}")
	if greeting_check != None and greeting_check != "Incorrect":
		#print("at greeting_check")
		valid_message = f"Hello {message}, How are you feeling today?"
		return valid_message
	return valid_message

def bye():

	possible_bye_messages = ["It was pleasure talking to you.", "Bye have a nice day.", "See you soon, take care."]
	bye_message = random.choice(possible_bye_messages)
	print(bye_message)

def main():

	greeting_message = greeting()
	#last_response = message
	last_response = greeting_message
	message = greeting_message
	matching_resonse = False
	last_question = None
	quit_pattern = r'[Qq]uit;?'
	quit = re.match(quit_pattern,message)
	#while message != 'quit':
	while not quit:
		#response_question = generate_response(str(message),last_response)
		if message == "":
			#print(f"Message {message}")
			#response_question = generate_response(str(last_response),last_response=None)
			print("You have to tell me something! :)")
			message = input(f"{response_question}\n>>")
			continue
		else:
			#message = input(f"{response_question}\n>>")
			#if last_question is None:
			if matching_resonse:
				response_question = last_question
				#response_question = generate_response(str(message),last_response)
				#message = input(f"{response_question}\n>>")
			else:
				response_question = generate_response(str(message),last_response)
				#response_question = last_question
				#last_question = None
			message = input(f"{response_question}\n>>")
			if last_response == message :
				print("You can't repeat yourself! :)\nPlease response to the response below....")
				#print(f"last_response: {last_response}")
				last_question = response_question
				matching_resonse = True
			else:
				matching_resonse = False
			#message = input(f"{response_question}\n>>")
			#response_question = generate_response(str(message),last_response)
			#message = input(f"{response_question}\n>>")

			#continue
			last_response = message
		quit = re.match(quit_pattern,message)
	bye()

main()
