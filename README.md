# twitter-chat-networks
Some tools for creating network graphs from Twitter interactions

##2nd_degree_networks.py: 

Find everyone a user has mentioned in their recent tweets, then everyone mentioned by those users. Good for mapping conversational networks. Outputs a CSV which can be imported into Gephi for visualisation. Requires [Tweepy](https://github.com/tweepy/tweepy) and  Twitter application keys. Usage:

    python 2nd_degree_networks.py username tweetcount
    eg
    python 2nd_degree_networks.py barackobama 200
