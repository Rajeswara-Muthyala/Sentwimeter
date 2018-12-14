#!/usr/bin/python
from twython import Twython  
import json
import pprint
import re
from textblob import TextBlob
from googletrans import Translator
import sys

def clean_tweet(tweet): 
    ''' 
    Utility function to clean tweet text by removing links, special characters 
    using simple regex statements. 
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

def get_tweet_sentiment(tweet): 
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text 
    analysis = TextBlob(clean_tweet(tweet)) 
    # set sentiment 
    if analysis.sentiment.polarity > 0: 
        return 'positive'
    elif analysis.sentiment.polarity == 0: 
        return 'neutral'
    else: 
        return 'negative'

def opinion_mining(search_results):
    #Dictionary 
    opinion_dict = {"positive":(), \
                    "negative":(), \
                    "neutral":()}
                    
    num_tweets = len(search_results['statuses'])
    positive = 0
    negative = 0
    neutral = 0
    for tweet in search_results['statuses']:
        #print("Created at ", tweet['created_at'], tweet['text'])
        sentimeter = get_tweet_sentiment(tweet['text'])
        if sentimeter == "positive":
            opinion_dict["positive"] += tuple([tweet['text']])
            positive+=1
        elif sentimeter == "negative":
            opinion_dict["negative"] += tuple([tweet['text']])
            negative+=1    
        else:
            opinion_dict["neutral"] += tuple([tweet['text']])
            neutral+=1

    positive_percetage = (float(positive) / num_tweets) * 100
    negative_percetage = (float(negative) / num_tweets) * 100
    neutral_percetage = (float(neutral) / num_tweets) * 100

    print "keyword ", keyword, "is trending in twitter as below:"
    print "Positive :) ", positive_percetage
    print "Negative :( ", negative_percetage
    print "neutral  :| ", neutral_percetage

    print "\n Assessed on ", num_tweets, " tweets"

    return opinion_dict

####main####

if len(sys.argv) != 4:
    print "Use Sentwi <tweet-keyword> <tweet-count> <since_date(YYYY-MM-DD)>"
    exit(0)

keyword = sys.argv[1]
tweet_count = sys.argv[2]
date = sys.argv[3]

APP_KEY = 'gQhZuweqmNC9gMAolBfHEny4f'
APP_SECRET = 'PBgFD6dX7vqfSfJByRg7uWd9bB4333t3e0VPnHkJOisWb8hkXi'

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

single_tweet = twitter.search(q=keyword, count=1, result_type='recent', until=date)
if len(single_tweet['statuses']) != 1:
    print "More thatn a single tweet for fetching since_id, exiting...", len(single_tweet['statuses'])
    exit(0)

print "since_id is ...", single_tweet['statuses'][0]['id'], "created at", single_tweet['statuses'][0]['created_at']
since = single_tweet['statuses'][0]['id']

pp = pprint.PrettyPrinter(indent=1)
search_results = twitter.search(q=keyword, count=tweet_count, result_type='recent', since_id=since)
'''
te_search_results = twitter.search(q=keyword, count=tweet_count, result_type='mixed', since_id=since, lang="te")

trans = Translator()
for result in te_search_results['statuses']:
    print result['text']
    trans.translate(result['text'])
'''
opin_dict = opinion_mining(search_results)
print type(opin_dict)

print "Print 1)Positive 2)Negative 3)Netral 4)Exit \n "
option = input("Enter option(1/2/3/4)")

opted_tuple = ()
if option == 1:
    opted_tuple = opin_dict['positive']
elif option == 2:
    opted_tuple = opin_dict['negative']
elif option == 3:
    opted_tuple = opin_dict['neutral']
elif option == 4:
    print "Exiting.."
    exit(0)
else:
    print "Undefined option, existing..."
    exit(0)

for tweet in opted_tuple:
    print " ***Start*** \n", tweet, "\n***End***"
