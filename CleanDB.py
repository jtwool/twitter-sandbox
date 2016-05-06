""" Cleans the ./tweets.db file by removing duplicate tweets.
Duplicate tweets are determined by rowid, not by content.
"""
import datetime, TweetDB

db = TweetDB.sqlconnect("./tweets.db")

db.cursor().execute("""
    DELETE
    FROM tweets
    WHERE   rowid NOT IN
            (
            SELECT  MIN(rowid)
            FROM    tweets
            GROUP BY twid
            ) 
    """)

now = datetime.datetime.now()

todaystweets = db.cursor().execute("""
    SELECT count(rowid)
    FROM tweets
    WHERE created
        LIKE '{}'
    """.format(now.strftime("%b %d %Y"))).fetchone()[0]

print("Run on {}. {} tweets added today.".\
       format(now.strftime("%c"),todaystweets))

db.commit()
db.close()