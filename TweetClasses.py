from datetime import datetime

class Tweet(object):
    """ A class designed to hold tweets."""
    def __init__(self, json):
        self.original = json
        self.text = json['text']
        self.twid = json['id']
        self.urls = [u['expanded_url'] for u in json['entities']['urls']]
        self.created = datetime.strptime(json['created_at'],
                                         '%a %b %d  %X %z %Y').strftime("%b %d %Y")
        self.created_full = json['created_at']
        self.hashtags = [ht['text'] for ht in json['entities']['hashtags']]
        self.mentions = [{'name':user['name'],
                          'id':user['id']} for user\
                           in json['entities']['user_mentions']]
        self.misc = {}
  
    def __repr__(self):
        return "{} ({})".format(self.text,self.created)
