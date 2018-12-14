#!/usr/bin/python
import sys
from twitterclient import TwitterClient
####main####

if len(sys.argv) != 4:
    print "Use Sentwimeter <tweet-keyword> <tweet-count> <since_date(YYYY-MM-DD)>"
    exit(0)

keyword = sys.argv[1]
count = sys.argv[2]
date = sys.argv[3]

tClient = TwitterClient()
search_results = tClient.search_until(k=keyword, tc=count, st="latest", ud=date)


'''
te_search_results = twitter.search(q=keyword, count=tweet_count, result_type='mixed', since_id=since, lang="te")

trans = Translator()
for result in te_search_results['statuses']:
    print result['text']
    trans.translate(result['text'])
'''
opin_dict = tClient.opinion_mining(search_results)
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
