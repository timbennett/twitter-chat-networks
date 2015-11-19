# twitter-chat-networks
Some tools for creating network graphs from Twitter interactions

##2nd_degree_networks.py: 

Find everyone a user has mentioned in their recent tweets, then everyone mentioned by those users (e.g. two degrees of separation from the original user). Good for mapping conversational networks. Outputs a CSV which can be imported into [Gephi](http://gephi.github.io/) for visualisation. Requires [Tweepy](https://github.com/tweepy/tweepy) and  Twitter application keys. Usage:

    python 2nd_degree_networks.py username tweetcount
    eg
    python 2nd_degree_networks.py barackobama 200

Sample image (after visualisation in Gephi):

![@dannolan](http://i.imgur.com/Dt1A0bb.png)
