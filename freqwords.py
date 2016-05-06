"""Gets recent tweets from a database and returns formatted output showing the most commonly used terms,
along with the percentage of occurance for each term used.

Has a verbose option which will provide examples from the DB of how each term was used.

Terms are represented as lemmas, so that knight, knighted, knights are all considered one term.
"""
import sys
from TweetDB import sqlconnect
from TweetClasses import Tweet
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter

class Candidate(object):
    """Holds information about the term to be searched for and the context its used in.
    """
    def __init__(self,name):
        self.name = name
        self.word_counts = Counter()
        self.by_lemma = {}
        self.lemmatizer = WordNetLemmatizer()
        
    def count_tweet(self, tweet, stoplist):
        """Adds a tweet to the context for the term.
        """
        for word in word_tokenize(tweet.text):
            lemma = self.lemmatizer.lemmatize(word.lower())
            if lemma in stoplist or len(lemma)<3:
                continue
            else:
                self.word_counts[lemma] += 1
                self.by_lemma[lemma] = self.by_lemma.get(lemma,[]) + [tweet.text]   
    
    def get_total_words(self):
        self.total_words = sum(self.word_counts.values())
        return self.total_words
    
    def get_most_common_words(self,n=20):
        self.most_common_words = self.word_counts.most_common(20)
        return self.most_common_words
    
def load_stoplist(path):
    """Loads a generic stoplist and adds a few custom terms
    """
    stoplist = open(path).read().split('\n')
    stoplist = stoplist + ['donald','trump','hillary',
                           'clinton','i','rt',
                           'http','...',"n't","'re",'amp',
                           'hillaryclinton','realdonaldtrump',]
    return stoplist

def db_to_tweets(dbcursor,n=5000):
    """Pulls some tweets from the database"""
    return [Tweet(eval(t[0])) for t in dbcursor.execute("""
                                                SELECT original
                                                FROM tweets
                                                ORDER BY rowid DESC
                                                LIMIT {}
                                                """.format(n)).fetchall()]

def rp(part,whole):
    """Turns two ints into a 3 decimal fraction"""
    fraction = part / float(whole)
    return round(fraction * 100,3)

def most_common_words(tweets, stoplist, candidates = [], examples = False):
    
    for tweet in tweets:
        for candidate in candidates:
            if tweet.text.lower().find(candidate.name.lower()) != -1:
                candidate.count_tweet(tweet, stoplist)
  
    for candidate in candidates:
        candidate.get_total_words()
        candidate.get_most_common_words()
        if candidate.name == candidates[-1].name:
            term = '\n'
        else:
            term = ''
        print("{:<30}".format(candidate.name), end=term)
    
    for i in range(20):
        for candidate in candidates:
            word, count = candidate.most_common_words[i]
            if candidate.name == candidates[-1].name:
                term = '\n'
            else:
                term = ''
            print("{:<20}{:>5}%{:<4}".format(word,
                                             rp(count,candidate.total_words),
                                             ""), end=term)
            
      
    if examples == True:    
        for candidate in candidates:
            for lemma,count in candidate.most_common_words:
                print("\n\n**{}:{}".format(candidate.name,lemma))
                i = 0
                for i,tweet in enumerate(candidate.by_lemma[lemma]):
                    if i >= 5: break
                    else: print(tweet)
              
db,cur = sqlconnect('tweets.db', cursor=True)
stoplist = load_stoplist('stoplist.txt')
tweets = db_to_tweets(cur)
Hillary = Candidate("Hillary")
Trump = Candidate("Trump")
if "v" in sys.argv[1:]:
    verbose = True
else: verbose = False
most_common_words(tweets, stoplist, 
                  candidates=[Hillary, Trump],
                  examples=verbose)
