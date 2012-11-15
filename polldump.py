import sys
import time
import scrapersettings as settings
from twython import Twython
from pymongo import Connection
from datetime import datetime
import dateutil.parser as parser

query_subjects = ["Romney", "Obama", "#election"]


print 'Connecting to the database...',
if settings.uses_remote:
    db = Connection(settings.remote_loc, slave_okay=True)
else:
    db = Connection()

storage = db['electiontweets']

if settings.uses_auth and not storage.authenticate(settings.mongousr, settings.mongopwd):
    print 'Failed to authenticate. Quitting.'
    sys.exit()
else:
    print 'Done.'


if settings.uses_outh:
    try:
        print 'Authenticating with Twitter...',
        twitter = Twython(settings.twitter_token, settings.twitter_secret, settings.oauth_token, settings.oauth_token_secret)
    except:
        print 'Failed. Quitting.'
        sys.exit()
    print 'Success.'


print 'Starting.'
done = False
while not done:
    print 'Polling...',
    numnew = 0
    try:
        for query in query_subjects:
            search_results = twitter.search(q=query, rpp="100", result_type="current", page=str(1))
            for tweet in search_results["results"]:
                d = {}
                d['tweet_id'] = tweet['id_str']
                d['from_user'] = tweet['from_user'].encode('utf-8')
                d['from_user_id'] = tweet['from_user_id_str']
                d['created_at'] = parser.parse(tweet['created_at'])
                d['text'] = tweet['text'].encode('utf-8')
                geo = tweet['geo']
                d['geopos'] = geo['coordinates'] if geo != None else "null"
                d['scraped_at'] = datetime.now()
                storage['tweets'].insert(d)
    except KeyboardInterrupt:
        print 'Quitting.',
        done = True
    except:
        print 'Crashed for some reason. :(',
    time.sleep(30)
