import os
import time
import tweepy

CONSUMER_KEY = os.environ.get('TWITTER_API_KEY')  # replace TWITTER_API_KEY with you api key
CONSUMER_SECRET = os.environ.get('TWITTER_API_SECRET')  # replace TWITTER_API_SECRET with you api key
ACCESS_KEY = os.environ.get('TWITTER_ACCESS_TOKEN_KEY')  # replace TWITTER_ACCESS_TOKEN_KEY with you api key
ACCESS_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')  # replace TWITTER_ACCESS_TOKEN_SECRET with you api key

# TEST HASHTAGS
hash_tags = ["#darksidedev", "#darksidedev1", "#darksidedev2", "#darksidedev3"]

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, cache=None)


def search_tweets(query):
    tweets = tweepy.Cursor(api.search, q=query).items(500)
    return tweets


target_tweet = search_tweets(hash_tags[0])


def like_tweet(tweets):
    for tweet in tweets:
        try:
            if not api.get_status(tweet.id).favorited:
                print("Liking tweet...")
                # print(f'Tweet {tweet.id} liked : {api.get_status(tweet.id).favorited}')
                tweet.favorite()
                time.sleep(10)
            else:
                # print("Tweet already liked")
                print(f'Tweet {tweet.id} liked : {api.get_status(tweet.id).favorited}')
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


def retweet(tweets):
    for tweet in tweets:
        try:
            # Retweeted tweets will have a 'retweeted_status' attribute, if that attribute doesn't exist it means the tweet has not been retweeted
            if not hasattr(tweet, 'retweeted_status'):
                # Not retweeted
                print(f'Tweet {tweet.id} not retweeted')
                print("Retweeting tweet...")
                tweet.retweet()
                time.sleep(10)
            else:
                # Retweeted
                print(f'Tweet {tweet.id} retweeted')
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


# REPLY TO TWEET WITH THE HASHTAG USED
def reply_tweet(tweets):
    for tweet in tweets:
        try:
            if tweet.in_reply_to_status_id is None:
                # This is a main tweet not a reply => we can leave a reply
                print("Replying main tweet...")
                print(tweet.in_reply_to_status_id)
                api.update_status(f'#{tweet.entities["hashtags"][0]["text"]}', in_reply_to_status_id=tweet.id)
                time.sleep(10)
            else:
                # This is a reply to some tweet => so we only like and retweet
                print("tweet is a reply...\nliking and retweeting...")
                like_tweet(tweets)
                retweet(tweets)
        except tweepy.TweepError as e:
            print(e.reason)
        except StopIteration:
            break


retweet(target_tweet)
