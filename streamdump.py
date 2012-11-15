from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Go to http://dev.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = ''
consumer_secret = ''

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = ''
access_token_secret = ''

filters = ['Obama', 'Romney', '#debate', 'debate', 'president']


class TwitterStreamListener(StreamListener):
    def __init__(self, filename):
        self.myfile = open(filename, "a")

    def on_data(self, data):
        self.myfile.write(data)
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':
    listener = TwitterStreamListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, listener)
    stream.filter(track=filters)
