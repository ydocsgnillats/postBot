import praw
import prawcore
import time
import sys
import re
import json
import post

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

	title = "Nibiru - Septagan(2020)"
	url = "https://www.youtube.com/watch?v=yT1QbKEXeSQ"

	def post(self): 

		global errors

		for sub in subreddits:
			try:
				title = "Nibiru - Septagan [experimental]"
				url = "https://www.youtube.com/watch?v=yT1QbKEXeSQ"
				#try posting on subreddits listed
				# try:
				subreddit = reddit.subreddit(sub)
				subreddit.submit(title, url = url)
				print("Posted to r/" + sub)
				print("Done.")
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
		#global subreddits
		for arg in argv:
			#if Bot.sub_exists(arg):
			subreddits.append(arg)
			print("Added: r/" + arg + " to subreddit array.")
			#else:
			#	print("The subreddit " + arg + " does not exist.")

	def clearSubreddits(self):
		global subreddits
		subreddits = []
		print("Subreddit list cleared.")

def main():
    
	b = Bot()
	b.clearSubreddits()
	b.popSubreddits("music", "atlantamusic","edmproduction","futurebeatproducers","indiemusicfeedback","lofihiphop","roastmytrack","promoteyourmusic","shareyourmusic","thisisourmusic","experimentalmusic","dub")
	b.post()
    
main()
