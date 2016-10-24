import pyttsx

def say(text):
	"""synthesizes the given text to speech"""	
	engine = pyttsx.init()
	engine.setProperty('rate', 100)
	engine.say(text)
	engine.runAndWait()

say("good morning")
