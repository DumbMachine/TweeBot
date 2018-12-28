import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
consumer_key =  '2XZ8WwA60fjcn30nUwMcZGNoZ'
consumer_secret = 'dlWKue8WH17vPRJO3bUJb9w4I1KJHQaD6MV7W0eTJFmeKQ6Gcm'
access_token = '753985003328012288-tPRbv9Za68YBLdelJEznkud2vJSkxQj'
access_token_secret = 'mEXfWUrHdwKLDLlqObzWsI9AHB6pdpnM1xNFH0IV8Pmju'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



#To get a hashtag , maxes at around 15000ish
for page in tweepy.Cursor(api.search , q = "batman" , count = 10).pages(1):
    for tweet in page:
        print(tweet.place)

#To get a USERS tweets
x=[]
y=[]
for page in tweepy.Cursor(api.user_timeline , id ="Trump" , count = 200).pages(5):
    for tweet in page:
        x.append(TextBlob(tweet.text).sentiment.polarity)
        y.append(TextBlob(tweet.text).sentiment.subjectivity)

plt.plot(x,color="#9966ff")
plt.rcParams['axes.facecolor'] = "#000000"
plt.rcParams['lines.linewidth'] = 5
plt.show()