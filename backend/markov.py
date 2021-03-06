import markovify, tweepy, re, time, sys, praw

def generateMarkov(text):
	# Get raw text as string.
	'''
	with open("/path/to/my/corpus.txt") as f:
	    text = f.read()
	'''
	# Build the model.
	text_model = markovify.Text(text)

	# Print five randomly-generated sentences
	for i in range(15):
	    text+= str(text_model.make_sentence())

	# Print three randomly-generated sentences of no more than 140 characters
	#for i in range(3):
	#    print(text_model.make_short_sentence(140))

	return text

def searchTweets(textToSearch):
   auth = tweepy.OAuthHandler('72USdViI5PT9VuadnGTocxwtP', 'RBpgWBnyMvsNSy5VIrpAuw1Z9v9stZXH33q0ygl747CB4BP60H')
   auth.set_access_token('2632797234-Caxa9h9PdbK9dW47njosiegOl0kPuJxSFov5vDl', 'yhcDb9R1iyR56jpeCU6nBhxylZRgaIXfRaOq0gUHqrxDT')
   api = tweepy.API(auth)
   statuses = api.search(q=textToSearch,count=50,locale='en_US')
   data = [s.text.encode('utf8') for s in statuses]
   return data

def writeStory():
	markovText = ""
	text = ""
	topic = sys.argv[1]
	post_limit = 10
	if sys.argv[2] == "twitter":
		# Get topic to search
		tweets = searchTweets(topic)

		# Parse Tweets
		for tweet in tweets:
			if len(tweet.strip()) > 5:
				# Remove social crap from tweets (credit: https://stackoverflow.com/a/8377440)
				stripped = lambda tweet: re.compile('\#').sub('', re.compile('RT @').sub('@', tweet, count=0).strip())
				text += ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",stripped(tweet)).split()) + '. '

		# Generate markov
		markovText = generateMarkov(text).rsplit(' ', 1)[0]
	elif sys.argv[2] == "reddit":
		r = praw.Reddit(user_agent='storytime script: amorgan.me/storytime')	
		r.login('storytime_bot', 'Jnw5v9pgbHW6qXXrNb24EJkGeE8KwZ', disable_warning=True)
		submissions = r.get_subreddit(topic).get_new(limit=10)

		# Get comments
		for x in xrange(0,post_limit):
			submission = next(submissions)
			#comments = praw.helpers.flatten_tree(submission.comments)
			# Parse comments
			print (submission)
			#for comment in submission.comments:
				#markovText+=comment.body
			#	print(comment.body)
	print (markovText)

def main():
	writeStory()

if __name__ == "__main__":
    	main()
