import praw
import config
import time


def bot_login():
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "Testing new bot")
	print "logged in!!!!"
	return r

def check_comment(comment):
	already_read_comments.append(comment.id)
	commentTextLower = comment.body.lower()
	if "years old" in commentTextLower:
		keywordIndex = commentTextLower.find("years")
		suspectedAge = commentTextLower[keywordIndex-3: keywordIndex-1]
		try:
			suspectedAgeInt = int(suspectedAge)
			#print commentTextLower
			ages.append(suspectedAgeInt)
		except ValueError:
			return commentTextLower
	elif "i'm " in commentTextLower or "im " in commentTextLower:
		if "i'm" in commentTextLower:
			temp = 4
			keywordIndex = commentTextLower.find("i'm")
		elif "im" in commentTextLower:
			temp = 3
			keywordIndex = commentTextLower.find("im")

		suspectedAge = commentTextLower[keywordIndex + temp: keywordIndex + temp + 2]
		try:
			suspectedAgeInt = int(suspectedAge)
			#print commentTextLower
			ages.append(suspectedAgeInt)
		except ValueError:
			return commentTextLower

def run_bot(r):
	for comment in r.subreddit(config.subreddit).comments(limit=100):
		if comment.id not in already_read_comments:
			check_comment(comment)


already_read_comments = []
ages = []
file = open("comments.txt")
for line in file:
	already_read_comments.append(line.strip('\n'))
file.close()
r = bot_login()
while True:
	run_bot(r)
	print ages