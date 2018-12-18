#!/usr/bin/python
import sys
from twitterclient import TwitterClient
import argparse
####main####

parser = argparse.ArgumentParser()

### Start of arguments ###
parser.add_argument("keyword", help = "keyword to search for")
parser.add_argument("since_date", help = "The date from which tweets should be analyzed")
parser.add_argument("-count", "--tweet_count", type=int, help = "Number of tweets to consider - *Warning* This may trigger multiple search requests. Each twitter search requests has a limitation 100 tweets. Default will be best effort", default=1000)
parser.add_argument("-st", "--search_type", help = "recent(default)/popular/mixed", default="recent")
parser.add_argument("-lang", "--language", help = "language tweets", default="en")
### End of arguments ###

args = parser.parse_args()

tClient = TwitterClient()
if args.tweet_count <= 100:
    search_results = tClient.search_until(k=args.keyword, tc=args.tweet_count, st=args.search_type, ud=args.since_date, lan = args.language)
    opin_dict = tClient.opinion_mining(search_results['statuses'])
    '''
    te_search_results = twitter.search(q=keyword, count=tweet_count, result_type='mixed', since_id=since, lang="te")

    trans = Translator()
    for result in te_search_results['statuses']:
        print result['text']
        trans.translate(result['text'])
    '''
else:
    multi_search_results = tClient.multi_search_until(k=args.keyword, ud=args.since_date, lan = args.language)
    opin_dict = tClient.opinion_mining_multi(multi_search_results)


while True:
    print "Print 1)Positive 2)Negative 3)Netral 4)Exit \n "
    option = input("Enter option(1/2/3/4)")

    opted_dict = {}
    if option == 1:
        opted_dict = opin_dict['positive']
    elif option == 2:
        opted_dict = opin_dict['negative']
    elif option == 3:
        opted_dict = opin_dict['neutral']
    elif option == 4:
        print "Exiting.."
        exit(0)
    else:
        print "Undefined option, existing..."
        exit(0)

    for key in opted_dict:
        print " ***" + opted_dict[key]['id_str'] + "***" + opted_dict[key]['created_at'] + "*** \n", opted_dict[key]['full_text'], "\n***End***"
