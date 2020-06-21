import os
import time
import tweepy

CONSUMER_KEY = os.environ.get('TWITTER_API_KEY')  # replace TWITTER_API_KEY with you api key
CONSUMER_SECRET = os.environ.get('TWITTER_API_SECRET')  # replace TWITTER_API_SECRET with you api key
ACCESS_KEY = os.environ.get('TWITTER_ACCESS_TOKEN_KEY')  # replace TWITTER_ACCESS_TOKEN_KEY with you api key
ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')  # replace TWITTER_ACCESS_TOKEN_SECRET with you api key

#TEST HASHTAGS
hash_tags = ["#darksidedev", "#darksidedev1", "#darksidedev2", "#darksidedev3"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def search_tweets(query):
    tweets = tweepy.Cursor(api.search, q=query).items(500)
    return tweets


target_tweet = search_tweets(hash_tags[0])


def like_tweet(tweets):
    for tweet in tweets:
        print(tweet)
        try:
            print("Liking tweet...")
            tweet.favorite()
            time.sleep(10)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


def retweet(tweets):
    for tweet in tweets:
        print(tweet)
        try:
            print("Retweeting tweet...")
            tweet.retweet()
            time.sleep(10)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


#REPLY TO TWEET WITH THE HASHTAG USED
def reply_tweet(tweets):
    for tweet in tweets:
        try:
            print("Replying tweet...")
            api.update_status(f'#{tweet.entities["hashtags"][0]["text"]}', in_reply_to_status_id=tweet.id)
            time.sleep(10)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


like_tweet(target_tweet)
retweet(target_tweet)
reply_tweet(target_tweet)




