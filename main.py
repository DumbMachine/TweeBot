import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
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
for page in tweepy.Cursor(api.user_timeline , id ="tommyxtopher" , count = 200).pages(100):
    for tweet in page:
        q1 = [word for word in tweet.text.split() if word not in stopwords.words('english')]
        sum=0
        for word in q1:
                sum+= TextBlob(word).sentiment.polarity
        x.append(sum/len(q1))



plt.plot(x,color="#9966ff")
plt.ylim(-1,1,0.005)
plt.rcParams['axes.facecolor'] = "#000000"
plt.rcParams['lines.linewidth'] = 1
plt.show()
sum=0
for nos in x:
        sum+=nos
print(sum/len(x))

plt.scatter([i for i  in range(len(x))],x)
plt.show()


