#!/usr/bin/env python
# encoding: utf-8

# usage: python 2nd_degree_networks.py username tweetcount
# e.g. python 2nd_degree_networks.py barackobama 50
# defaults to 50 tweets, maximum 200

import tweepy #https://github.com/tweepy/tweepy
import sys

# Twitter API credentials, get your own at apps.twitter.com
# (yes I know I should import a config file or use environment variables)
access_key = ""
access_secret = ""
consumer_key = ""
consumer_secret = ""

# This function takes a user's Twitter handle and how many recent tweets to fetch (up to 200).
# It then extracts mentioned users from each tweet, *excluding* retweeted users - this is a 
# deliberate decision as I feel retweets aren't a strong signal of conversation.
def get_user_connections(screen_name,tweet_count):    
    # Can probably move these out of the function
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    # make initial request for most recent tweets (200 is the maximum allowed count):
    try:
    	user_tweets = api.user_timeline(screen_name = screen_name,count=tweet_count)
    except:
    	user_tweets = None
    user_mentions = []
    
    for tweet in user_tweets:
        user_mentions_count = len(tweet.entities['user_mentions'])
        # exclude retweets:
        if not hasattr(tweet,'retweeted_status'):
            # if there are user mentions, add them to user_mentions:
            if user_mentions_count > 0:
                for i in range (0,user_mentions_count):
                    user_mentions.append(tweet.entities['user_mentions'][i]['screen_name'])
    user_mentions_set = list(set(user_mentions))
    return user_mentions, user_mentions_set

# who's the centre of the network? We'll get their first-degree mentions then examine each one in turn.
screen_name = str(sys.argv[1])
# number of tweets to fetch from each user (defaults to 50)
try:
	sys.argv[2]
except:
	tweet_count = 50
else:
	tweet_count = int(sys.argv[2])
print "Getting",tweet_count,"tweets for",screen_name

user_mentions, user_mentions_set = get_user_connections(screen_name,tweet_count)
print "All mentions: ", user_mentions

print "Unique mentions: ", user_mentions_set

# dictionary holding the list of everyone mentioned by each first-degree connection:
mentions_manifest = {}

# for each first-degree connection, get their first-degree connections;
# this gives us the network centre's second-degree connections
for user in user_mentions_set:
	try:
		temp_mentions, temp_mentions_set = get_user_connections(user,tweet_count)
		# add the user to the manifest
		mentions_manifest[user] = []
		# add their connections to the manifest; if they spoke to someone multiple times we capture that 
		# so we can do edge weighting in the resulting graph. If you don't want edge weighting you can use
		# temp_mentions_set instead.
		for temp_user in temp_mentions:
			mentions_manifest[user].append(temp_user)
		print "Finished", user, "with", len(temp_mentions), "connections"
	except:
		print "Could not fetch", user        
#print "Manifest: ", mentions_manifest

# the following output is in Gephi's semicolon-delimited format
outfile = screen_name+".csv"
print "Saving data in",outfile
outfile = open(outfile,"wb")

# print the network center's first-degree connections
for user in user_mentions:
	# print screen_name+";"+user # uncomment to print in terminal
	outfile.write(screen_name+";"+user+"\n")

# print the manifest connections
for user in mentions_manifest:
    for user2 in mentions_manifest[user]:
		outfile.write(user+";"+user2+"\n")
		# print user+";"+user2 # uncomment to print in terminal
        

outfile.close()
