#!/usr/bin/python
from twython import Twython  
import json
import pprint
import re
from textblob import TextBlob
from googletrans import Translator
import sys

class TwitterClient():
    'Twitter client to access twitter'
    def __init__(self):
        APP_KEY = 'gQhZuweqmNC9gMAolBfHEny4f'
        APP_SECRET = 'PBgFD6dX7vqfSfJByRg7uWd9bB4333t3e0VPnHkJOisWb8hkXi'

        twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
        ACCESS_TOKEN = twitter.obtain_access_token()

        self.twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)


    def __clean_tweet(self, tweet): 
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
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.__clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

    def search_until(self, k, tc, st, ud, lan = 'en'):
        single_tweet = self.twitter.search(q=k, count=1, result_type="recent", until=ud)
        if len(single_tweet['statuses']) != 1:
            print "More than a single tweet for fetching since_id, exiting...", len(single_tweet['statuses'])
            exit(0)

        print "since_id is ...", single_tweet['statuses'][0]['id'], "created at", single_tweet['statuses'][0]['created_at']
        since = single_tweet['statuses'][0]['id']

        search_results = self.twitter.search(q=k, count=tc, result_type=st, since_id=since, lang = lan, tweet_mode='extended')
        return search_results

    def multi_search_until(self, k, ud, lan = 'en'):
        single_tweet = self.twitter.search(q=k, count=1, result_type="recent", until=ud)
        if len(single_tweet['statuses']) != 1:
            print "More than a single tweet for fetching since_id, exiting...", len(single_tweet['statuses'])
            exit(0)

        print "since_id is ...", single_tweet['statuses'][0]['id'], "created at", single_tweet['statuses'][0]['created_at']
        since = single_tweet['statuses'][0]['id']

        results = []
        result = self.twitter.search(q=k, count=100, result_type="recent", lang = lan, tweet_mode='extended')
        results.append(result)
        iter = 0
        
        while iter <= 10:
            # Get max_id of results
            print result['search_metadata']
            try:
                next_max_id = result['search_metadata']['next_results'].split('max_id=')[1].split('&')[0]
            except:
                print "No more next pages"
                break

            if next_max_id <= since:
                break

            # Use max_id in next request 
            result = self.twitter.search(q=k, count=100, max_id=next_max_id, lang = lan, tweet_mode='extended')
            results.append(result)
            iter += 1

        print "Am i here"
        return results

    def opinion_mining_multi(self, multi_search_results):
        num_tweets = 0
        positive = 0
        negative = 0
        neutral = 0

        opinion_dict = {"positive":{}, \
                        "negative":{}, \
                        "neutral":{}}

        for i in multi_search_results:
                            
            num_tweets += len(i['statuses'])
            for tweet in i['statuses']:
                #print("Created at ", tweet['created_at'], tweet['text'])
                sentimeter = self.get_tweet_sentiment(tweet['full_text'])
                if sentimeter == "positive":
                    opinion_dict["positive"][tweet['id']] = tweet
                    positive+=1
                elif sentimeter == "negative":
                    opinion_dict["negative"][tweet['id']] = tweet
                    negative+=1    
                else:
                    opinion_dict["neutral"][tweet['id']] = tweet
                    neutral+=1

        positive_percetage = (float(positive) / num_tweets) * 100
        negative_percetage = (float(negative) / num_tweets) * 100
        neutral_percetage = (float(neutral) / num_tweets) * 100

        #print "keyword ", keyword, "is trending in twitter as below:"
        print "Positive :) ", positive_percetage
        print "Negative :( ", negative_percetage
        print "neutral  :| ", neutral_percetage

        print "\n Assessed on ", num_tweets, " tweets"

        return opinion_dict

    def opinion_mining(self, search_results):
        #Dictionary 
        opinion_dict = {"positive":{}, \
                        "negative":{}, \
                        "neutral":{}}
                        
        num_tweets = len(search_results)
        positive = 0
        negative = 0
        neutral = 0
        for tweet in search_results:
            #print("Created at ", tweet['created_at'], tweet['text'])
            sentimeter = self.get_tweet_sentiment(tweet['full_text'])
            if sentimeter == "positive":
                opinion_dict["positive"][tweet['id']] = tweet
                positive+=1
            elif sentimeter == "negative":
                opinion_dict["negative"][tweet['id']] = tweet
                negative+=1    
            else:
                opinion_dict["neutral"][tweet['id']] = tweet
                neutral+=1

        positive_percetage = (float(positive) / num_tweets) * 100
        negative_percetage = (float(negative) / num_tweets) * 100
        neutral_percetage = (float(neutral) / num_tweets) * 100

        #print "keyword ", keyword, "is trending in twitter as below:"
        print "Positive :) ", positive_percetage
        print "Negative :( ", negative_percetage
        print "neutral  :| ", neutral_percetage

        print "\n Assessed on ", num_tweets, " tweets"

        return opinion_dict
