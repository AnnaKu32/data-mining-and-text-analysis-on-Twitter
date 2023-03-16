import tweepy
import verf_keys
import mysql.connector
from datetime import datetime
import functions as fun

cnx = mysql.connector.connect(user='', password='',
                              host='',
                              database='')

cursor = cnx.cursor(buffered=True)

# ---------------   authorization and query   --------------- #
client = tweepy.Client(bearer_token=verf_keys.Bearer_Token)
api = tweepy.API(client)
query = 'Java lang:EN'
#query = 'Java lang:EN -is:retweet -is:quote -is:reply'
start = '2023-03-13T10:00:00Z'
end = '2023-03-13T10:30:00Z'
response = client.search_recent_tweets(query=query, start_time=start, end_time=end, max_results=100,
                                    tweet_fields=['created_at', 'public_metrics', 'lang'],
                                    user_fields=['location'],
                                    expansions=['author_id'])

# ---------------   add data to database    --------------- #
users = {u['id']: u for u in response.includes['users']}
#column = ['author', 'date', 'location', 'retweet', 'likes', 'reply_count', 'tweet']
data = []
all_words = []

for tweet in response.data:

    if users[tweet.author_id]:
        user = users[tweet.author_id]
        tweet_retweet = tweet.public_metrics['retweet_count']
        tweet_reply_count = tweet.public_metrics['reply_count']
        tweet_likes = tweet.public_metrics['like_count']
        user_location = user.location
        tweet_text = fun.cleaning(tweet.text)
        tweet_time = datetime.strftime(tweet.created_at,'%a %b %d %H:%M:%S %z %Y')

        add_tweet_information = (
            "INSERT INTO tweets "
            "(Author, DateofTweet, Location, Retweet, Likes, Reply_count, Tweet) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        )

        data_tweet = (
            user.username, tweet_time, user_location, tweet_retweet, tweet_likes, tweet_reply_count, tweet.text
        )

        cursor.execute(add_tweet_information, data_tweet)
        emp_no = cursor.lastrowid

cnx.commit()
cursor.close()
cnx.close()
