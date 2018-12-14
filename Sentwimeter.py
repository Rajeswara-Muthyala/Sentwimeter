#!/usr/bin/python
import sys
from twitterclient import TwitterClient
import argparse
####main####

parser = argparse.ArgumentParser()
parser.add_argument("keyword", help = "keyword to search for")
parser.add_argument("count", help = "Number of tweets to consider(limit of 100)")
parser.add_argument("since_date", help = "The date from which tweets should be analyzed")
parser.add_argument("-st", "--search_type", help = "recent(default)/popular/mixed", default="recent")
parser.add_argument("-lang", "--language", help = "language tweets", default="en")
args = parser.parse_args()

tClient = TwitterClient()
search_results = tClient.search_until(k=args.keyword, tc=args.count, st=args.search_type, ud=args.since_date, lan = args.language)

'''
te_search_results = twitter.search(q=keyword, count=tweet_count, result_type='mixed', since_id=since, lang="te")

trans = Translator()
for result in te_search_results['statuses']:
    print result['text']
    trans.translate(result['text'])
'''

opin_dict = tClient.opinion_mining(search_results)

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
