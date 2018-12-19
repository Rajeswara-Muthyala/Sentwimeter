#!/usr/bin/python
import sys
from twitterclient import TwitterClient
import argparse
from collections import OrderedDict
import pprint


### Start of arguments ###
parser = argparse.ArgumentParser()
parser.add_argument("Movie", help = "keyword to search for")
parser.add_argument("since_date", help = "The date from which tweets should be analyzed")
parser.add_argument("-v", "--verbose", help = "Print traces for debugging", type=bool, default=False)
### End of arguments ###

####main####
args = parser.parse_args()
tClient = TwitterClient()

ReviewRules = [('VeryGood' , 90),
               ('Good'     , 80),
               ('Watchable', 70),
               ('Average'  , 60),
               ('Bad'      , 30),
               ('VeryBad'  ,  0)]

multi_search_results = tClient.multi_search_until(k=args.Movie, ud=args.since_date, verbose=args.verbose)
total_tweets, opinion_dictionary = tClient.review_mining_multi(multi_search_results, ReviewRules)

'''
opinion dictionary is a dictionary of dictionaries has the following structure

{Sentiment : {tweet_id: tweet_text}}

ex: {'VeryGood' : { 1 : "Must Watch",
                    2 : "Top Notch" } } 

'''
result_summary_dictionary = OrderedDict({int: [str,(float, int)]})
'''
{SentimentSNo:[Sentiment, 
                (approved percetage(percentage of tweets who approved this rating), 
                 tweets in rating(number of tweets in rating)
                )
              ]
}

ex: { 1 : ['VeryGood' , (30% , 45)],
      2 : { 'Good'    , (20% , 30)},
    }

'''
for i, rule in enumerate(ReviewRules):
    rating = rule[0]
    rating_wise_dictionary = opinion_dictionary[rating]
    tweets_per_rating = len(rating_wise_dictionary)
    approved_percent_per_rating = (float(tweets_per_rating)/total_tweets) * 100
    result_summary_dictionary[i] = [rating, (approved_percent_per_rating, tweets_per_rating)]


while True:
    print "Result Summary:-"
    '''
    for key,value in result_summary_dictionary.items():
        print key, ")", value[0], \
        " Approved Percetage ",value[1][0], \
        "Tweets in Category", value[1][1]  
    '''
    for key,value in result_summary_dictionary.items():
        print key, ")", value[0], \
        "    ***   ", value[1][0],"%", \
        "    ***   ", value[1][1],"tweets"

    print "To print tweets Rating wise, Enter 0 to 5, or 6(to quit)"
    option = input()
    if option < 6:
        disp_dict = opinion_dictionary[ReviewRules[option][0]]
        for tweet_id in disp_dict:
            print "\n****"+str(tweet_id)+"*****"
            print disp_dict[tweet_id]['full_text']
            print "\n*****************"
    else:
        break
