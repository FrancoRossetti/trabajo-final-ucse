"""
This module contains the code for processing World Cup tweets.
"""

import time
import re
from datetime import datetime
import pandas as pd
from twitter_keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_SECRET, ACCESS_TOKEN
import tweepy

# Setup access to API


def connect_to_twitter_oauth():
    """
    Function to connect to Twitter api.
    """
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # add proxy='172.30.1.251:6969' if needed
    twitter_api = tweepy.API(auth, wait_on_rate_limit=True)
    return twitter_api


if __name__ == "__main__":
    # Connect to twitter API
    api = connect_to_twitter_oauth()
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
    RT_FILTER = " -filter:retweets lang:es"
    queries = [s + RT_FILTER for s in queries]
    for i in [1, 2, 3, 4]:
        print(f'Iteration number: {i}')
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
        df.to_csv(f"D:\\FACU\\TF_CSVs\\WorldCupTweets_{str(now)[:16].replace(':', '_')}.csv",
                  index=True,
                  encoding='utf-8-sig',
                  sep=';'
                  )
        print('Csv created at: %s' % 'D:\\FACU\\TF_CSVs\\' +
              'WorldCupTweets_' + str(now)[:16].replace(':', '_') + '.csv')
        time.sleep(900)
