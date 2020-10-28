# Regex Capabilities
import re 

# Command-Line Arguments
import sys

# Provides access to Twitter API
import tweepy 
from tweepy import OAuthHandler 

# Textblob provides robust text processing capabilities
from textblob import TextBlob 

class TwitterClient(object): 
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		# Access Tokens & Customer Keys
		consumer_key = '3e3RCRzto4oZcUZNkNsNfqtCb'
		consumer_secret = 'NFwqPxYeRvjrdBSkKlc0NVYlr6kKTQuCRPtM6DyDRkBp1xtftm'
		access_token = '1320550279159468033-TV2TUbDeLocc8U1VPTNahrJgVCZvzX'
		access_token_secret = '0FiY0BmzKFazRJRxpTtc54ftiCevn1as3V0E94C0iic2c'

		# Access API
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# Use Textblob to Conduct Sentiment Analysis
		analysis = TextBlob(self.clean_tweet(tweet)) 
		
        # Get SA of Tweet
		if analysis.sentiment.polarity > 0: 
			return 'positive'
		elif analysis.sentiment.polarity == 0: 
			return 'neutral'
		else: 
			return 'negative'

	def get_tweets(self, query, count = 10): 
		''' 
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			# Fetch Tweets that Match Specified Query
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} 

				# Retrieving Text
				parsed_tweet['text'] = tweet.text 
				# Set Sentiment 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once 
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e)) 

def main(): 
	# creating object of TwitterClient Class 
    api = TwitterClient() 
    
    # get query from CLI
    if len(sys.argv) >= 2:
        query = sys.argv[1]
    else:
        query = 'python'
        
    # calling function to get tweets 
    tweets = api.get_tweets(query, count = 200) 

    # picking positive tweets from tweets 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 

    # percentage of positive tweets 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))

    # picking negative tweets from tweets 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 

    # percentage of negative tweets 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 

    # percentage of neutral tweets 
    print("Neutral tweets percentage: {} %".format(100*(len(tweets) -(len( ntweets )+len( ptweets)))/len(tweets))) 

    # printing first 5 positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        print(tweet['text']) 

    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text']) 

if __name__ == "__main__": 
	# calling main function 
	main() 
