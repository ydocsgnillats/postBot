import praw
import prawcore
import time
import sys
import re
import json
import post

from app import hello

from prawcore import NotFound

subreddits = []

def login():
    try:
        reddit = praw.Reddit('bot1',user_agent='Spread-Bot V1.0')
        return reddit    
    except prawcore.exceptions.OAuthException:
        print("Wrong username or password")

pos = 0
errors = 0
reddit = login()

class Bot:

	title = "1"
	link = "2"

	def getLink(self):
		return Bot.link

	def setLink(self, l):
		Bot.link = "\""+l+"\""
		print("Link set to: " + Bot.link)

	def getTitle(self):
		return Bot.title

	def setTitle(self, t):
		Bot.title = "\""+t+"\""
		print("Title set to: " + Bot.title)

	def post(self): 

		global errors

		for sub in subreddits:
			try:
				#try posting on subreddits listed
				subreddit = reddit.subreddit(sub)
				subreddit.submit(Bot.title, url = Bot.link)
				print("Posted to r/" + sub)
			except KeyboardInterrupt:
				print('\n')
				sys.exit(0)
			except praw.exceptions.APIException as e:
				if (e.error_type == "RATELIMIT"):
					delay = re.search("(%d) minutes", e.message)
					if delay:
						delay_seconds = float(int(delay.group(1)) * 60)
						time.sleep(delay_seconds)
						self.post(sub)
					else: 
						delay = re.search("(%d) seconds", e.message)
						delay_seconds = float(delay.group(1))
						time.sleep(delay_seconds)
						self.post(sub)
			except: 
				errors = errors+1
				if(errors >10):
					print("Program Crashed")

	def sub_exists(self, sub):
		exists = True
		try:
			reddit.subreddits.search_by_name(sub, exact=True)  
		except NotFound:
			exists = False
		return exists

	def popSubreddits(self,*argv):
		dne = False
		dneString = "\nSubreddit(s) not found: "
		for arg in argv:
			if (Bot.sub_exists(arg,arg)):
				subreddits.append(arg)
				print("Added: r/" + arg + " to subreddit array.")
			else:
				dne = True 
				dneString+="\n 	" + arg
		if (dne == True):
			print(dneString + "\n")
		
	def clearSubreddits(self):
		global subreddits
		subreddits = []
		print("Subreddit list cleared.")

def main():
    
	b = Bot()
	b.clearSubreddits()
	b.popSubreddits("music", "roastmytrack", "atlantamusic", "promoteyourmusic", "experimentalmusic", "shareyourmusic", "vaporwave")
	b.setTitle("Test")
	b.setLink("www.youtube.com")
	b.post()
	
main()
