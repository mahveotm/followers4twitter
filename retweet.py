import os
import tweepy, time

# this script enables you to retweet your timeline feeds. Several error including attempts to retweet already retweeted tweets are taken into account
#new update include saving your consumer keys and other secret tokens to env before running. 
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET =os.environ.get('CONSUMER_SECRET')
ACCESS_KEY =os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

FILE_NAME = 'last_seen_id.txt'
#You need to create an empty text file and name last_seen_id.txt
#This script will read the tweet id and keep updating it when done to avoid repeating a tweet

def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def retweet():
    print('retrieving and attempting to retweet...')

    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    home = api.home_timeline(
                        last_seen_id,)
    for status in reversed(home):
        print(str(status.id)+status.text)
        last_seen_id = status.id
        store_last_seen_id(last_seen_id, FILE_NAME)
    if 'follow' in status.text.lower():
        	print('found tweets')
        	api.retweet(status.id)

while True:
	try:
		retweet()
		time.sleep(120)
	except tweepy.RateLimitError:
		print("You have reached the twitter rate limit, kindly wait for sometime -don't worry my timer has started already and I'd restart automatically")
		time.sleep(60*60*3)
	except tweepy.TweepError:
		print('you have retweeted this before, please wait while I pass')
		time.sleep(30)
