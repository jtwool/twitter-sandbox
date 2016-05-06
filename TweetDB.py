import sqlite3 as sql

def setupDB(path):
    """ Sets up the tweets.db file in SQlite3
    """
    db = sql.connect(path)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE tweets (text text, twid text, created text,
                                           createdfull text, hashtags text,
                                           mentions text, urls text,
                                           original text)""")
    db.commit()
    db.close()

def sqlconnect(path, cursor = False):
    """Connects to a sqlite database"""
    db = sql.connect(path)
    if cursor == True:
        return db, db.cursor()
    return db
    
def add(tweet, db):
    """Adds a tweet to the database setup by setupDB"""
    db.cursor().execute("INSERT INTO tweets VALUES (?,?,?,?,?,?,?,?)",
                   (str(tweet.text), str(tweet.twid), str(tweet.created),         
                    str(tweet.created_full),str(tweet.hashtags),
                    str(tweet.mentions), str(tweet.urls),
                    str(tweet.original)))
    db.commit()