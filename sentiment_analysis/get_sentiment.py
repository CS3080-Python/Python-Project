# Regex Capabilities
import re

# Command-Line Arguments
import sys

# Provides access to Twitter API
import tweepy

# Textblob provides robust text processing capabilities
from textblob import TextBlob
from tweepy import OAuthHandler

# Import POST 
sys.path.append('C:\CS3080\Python-Project\dataflow')  
from post_data import post_tweet


class Object_DB(object):
    '''
    This is the final object type that is passed into the database, and is modified depending on what we decide to display to the user.
    '''
    def __init__(self):
        self.topic = ''
        self.sa_type = ''
        self.sa_score = 0


class Tweet_DB(object):
    '''
    Return objects from get_tweets for storage into local database. Ensure that this class
    has all of the attributes that need to be represented in the database.
    '''
    def __init__(self):
        self.topic = ''             # search topic to tweet
        self.text = ''              # tweet text content
        self.sentiment = ''         # pos/neut/neg sentiment
        self.sent_score = ''
        self.user = tweepy.User     # contains poster data - reassigned to username
        self.hashtag_list = []      # list of associated hashtags, if applicable


class TwitterClient(object): 
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        # Access Tokens & Customer Keys
        auth_list = self.get_access_keys()
        consumer_key = auth_list[0]
        consumer_secret = auth_list[1]
        access_token = auth_list[2]
        access_token_secret = auth_list[3]

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
    
    def get_access_keys(self):
        '''
        Get the keys from local machine for Twitter API.
        '''

        # Enter Location of Keys Here
        file_location = r'C:\CS3080\Python-Project\keys.txt'

        auth_list = []
        with open (file_location, 'rt') as keyfile:
            for x in range(4):
                content = keyfile.readline()
                # strip newline char
                content = content[:-1]
                auth_list.insert(x, content)
        
        # return list of keys & tokens
        return auth_list

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
        
        # Store SA Data
        sa_list = []
        
        # Get SA of Tweet
        if analysis.sentiment.polarity > 0:
            sa_list.append('positive')
            sa_list.append(analysis.sentiment.polarity * (1 - analysis.sentiment.subjectivity))
            return sa_list
        elif analysis.sentiment.polarity == 0:
            sa_list.append('neutral')
            sa_list.append(analysis.sentiment.polarity * (1 - analysis.sentiment.subjectivity))
            return sa_list
        else:
            sa_list.append('negative')
            sa_list.append(analysis.sentiment.polarity * (1 - analysis.sentiment.subjectivity))
            return sa_list

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # Fetch Tweets that Match Specified Query
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:

                # Create Database Tweet, Assign Parameters
                parsed_tweet = Tweet_DB()
                parsed_tweet.topic = query
                parsed_tweet.text = tweet.text
                
                # Get Sentiment and Score
                sentiment_list = self.get_tweet_sentiment(tweet.text)
                parsed_tweet.sentiment = sentiment_list[0]
                parsed_tweet.sent_score = sentiment_list[1]

                # Extracting Username from Tweet
                if tweet.user._json['name']:  # if any name present...
                    parsed_tweet.user = tweet.user._json['name']
                else:
                    parsed_tweet.user = 'Unknown'
                
                
                # Extracting Hashtags from Tweet
                if tweet.entities['hashtags']:  # if any values...
                    # print(tweet.hashtag_set['hashtags'])  # print full list
                    for tags in tweet.entities['hashtags']:  # print tags
                        parsed_tweet.hashtag_list.append(tags['text']) # add extracted tags to list
                    
                            
                # Add Parsed Tweet to Tweet List
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # Return Parsed Tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

def SentimentAnalysis(query): 
    # creating object of TwitterClient Class
    api = TwitterClient() 
    
    # create DB Object for storage
    db_obj = Object_DB()
    db_obj.topic = query # assign topic
    
    # calling function to get tweets 
    tweets = api.get_tweets(query, count=100)
    
    # Calculate Cumulative Sentiment
    overall_polarity = 0
    for tweet in tweets:
        overall_polarity += tweet.sent_score
    
    # assign polarity to database object
    db_obj.sa_score = overall_polarity
    # set to 2 decimal places
    db_obj.sa_score = round(db_obj.sa_score, 2);
    
    # calculate sentiment type of database object
    if overall_polarity > 0:
        db_obj.sa_type = 'positive'
    elif overall_polarity < 0:
        db_obj.sa_type = 'negative'
    else:
        db_obj.sa_type = 'neutral'

    # Send to Database
    post_tweet(db_obj)
    
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet.sentiment == 'positive'] # add positive tweets

    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet.sentiment == 'negative'] # add negative tweets

    # percentage of positive tweets
    print("Positive tweets percentage: {0:.2f}%".format(100*len(ptweets)/len(tweets)))
    print("Positive tweets sentiment number:", len(ptweets))

    # percentage of negative tweets 
    print("Negative tweets percentage: {0:.2f}%".format(100*len(ntweets)/len(tweets))) 
    print("Negative tweets sentiment number:", len(ntweets))
    
    # percentage of neutral tweets 
    print("Neutral tweets percentage: {0:.2f}%".format(100*(len(tweets)-(len(ntweets)+len(ptweets)))/len(tweets))) 
    print("Neutral tweets senetiment number:", len(tweets) - (len(ptweets) + len(ntweets)))
    
    return db_obj
    
if __name__ == "__main__": 
    # calling main function
    db_obj = SentimentAnalysis()
