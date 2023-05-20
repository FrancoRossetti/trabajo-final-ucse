import tweepy
import time
import pandas as pd
import re
import sys
from datetime import datetime
from twitter_keys import consumer_key, consumer_secret, access_token_secret, access_token


def quit():
    """Program was not initialized correctly"""
    print("example: python template.py -o something_here -b")
    sys.exit(1)


def custom_error(message):
    """Some other custom error"""
    print("There is a problem: %s" % message)
    sys.exit(2)

# Setup access to API


def connect_to_twitter_OAuth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # add proxy='172.30.1.251:6969' if needed
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


if __name__ == "__main__":
    # Connect to twitter API
    api = connect_to_twitter_OAuth()
    # tweet content
    tweets = []
    # likes from tweet
    likes = []
    # datetime created of tweet
    timecreated = []
    # IDs of tweets
    tweet_id = []
    # add queries to search
    queries = []
    teams = ['Argentina vs Francia']
    players = ['Messi', 'Mbappe', 'Dibu Martinez']
    general_hashtags = ['#Mundial2022', '#Qatar2022', '#CopaMundialFIFA']
    queries = teams + general_hashtags + players
    rtfilter = " -filter:retweets lang:es"
    queries = [s + rtfilter for s in queries]
    for i in [1, 2, 3, 4]:
        print('Iteration number: %d' % i)
        for query in queries:
            print('Tweet api search query: ', query)
            for tweet in tweepy.Cursor(api.search_tweets,
                                       q=query).items(1250):
                text = tweet.text.replace('\n', ' ')
                clean_tweet = re.sub("@[A-Za-z0-9]+", "", text)
                clean_tweet = re.sub(r"http\S+", "", clean_tweet)
                tweets.append(clean_tweet.lower())
                tweet_id.append(tweet.id_str)
                likes.append(tweet.favorite_count)
                timecreated.append(tweet.created_at)
        df = pd.DataFrame(
            {'tweet_id': tweet_id, 'tweets': tweets, 'likes': likes, 'time': timecreated},)
        now = datetime.now()
        df.to_csv('D:\\FACU\\TF_CSVs\\'+'WorldCupTweets_' + str(now)[:16].replace(':', '_') + '.csv',
                  index=True,
                  encoding='utf-8-sig',
                  sep=';'
                  )
        print('Csv created at: %s' % 'D:\\FACU\\TF_CSVs\\' +
              'WorldCupTweets_' + str(now)[:16].replace(':', '_') + '.csv')
        time.sleep(900)
