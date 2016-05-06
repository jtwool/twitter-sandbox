""" Downloads and stores 100 tweets on pre-determined topics.
"""
import sys
import TweetDB
from configsreader import getconfigs
from TwitterAPI import TwitterAPI
from TweetClasses import Tweet

CONFIGS = getconfigs(sys.argv[1])

api = TwitterAPI(CONFIGS['consumerkey'],       
                 CONFIGS['consumersecret'],
                 CONFIGS['accesstokenkey'],
                 CONFIGS['accesstokensecret'])

def search(query,feed='search/tweets',api=api, n=100):
    return [Tweet(t) for t in api.request(feed, {'q':query,
                                                 'count': n})]

terms = ('hillary','trump')       

tweets = []
for term in terms:
    tweets += search(term)

db = TweetDB.sqlconnect("./tweets.db")

for tweet in tweets:
    TweetDB.add(tweet,db)

db.commit()
db.close()