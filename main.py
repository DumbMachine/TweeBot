# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 21:26:44 2019

@author: ratin
"""
import seaborn as sns
import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import requests
import json 
KEY= "G5XlhCqsGp7pxVgAjGTFu04yYvnD8esq"


consumer_key =  '2XZ8WwA60fjcn30nUwMcZGNoZ'
consumer_secret = 'dlWKue8WH17vPRJO3bUJb9w4I1KJHQaD6MV7W0eTJFmeKQ6Gcm'
access_token = '753985003328012288-tPRbv9Za68YBLdelJEznkud2vJSkxQj'
access_token_secret = 'mEXfWUrHdwKLDLlqObzWsI9AHB6pdpnM1xNFH0IV8Pmju'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweets = []
for page in tweepy.Cursor(api.search , q="#trump" , count = 100,languages=["en"],tweet_mode='extended').pages(100):
    for tweet in page:
        hashtags_=[]
        urls=[]
        for hashtag in tweet.entities["hashtags"]:
            hashtags_.append(hashtag["text"])
#        for media in tweet.entities["media"]:
#            urls.append(media["expanded_url"])
        geo_url = "https://www.mapquestapi.com/geocoding/v1/address?key=KEY&inFormat=kvp&outFormat=json&location=LOCATION&thumbMaps=false".replace("KEY", KEY).replace("LOCATION",tweet.user.location)
        try:
            r = requests.get(url = geo_url)
            location =json.loads(r.content.decode('utf-8'))["results"][0]["locations"][0]["adminArea1"]
        except:
            location = ""
        twe = {"text": tweet.full_text,
               "cleaned_text": " ".join([word for word in tweet.full_text.split() if word not in stopwords.words('english')]).replace("#","").replace("*",""),
               "location": location.lower(),
               "username": tweet.user.screen_name,
               "retweets": tweet.retweet_count,
               "favcount": tweet.user.favourites_count,
               "hastags": hashtags_,
               "sentiment": TextBlob(" ".join([word for word in tweet.full_text.split() if word not in stopwords.words('english')])).sentiment.polarity,
               "subjectivity": TextBlob(" ".join([word for word in tweet.full_text.split() if word not in stopwords.words('english')])).sentiment.subjectivity,
                }
        tweets.append(twe)


locations = []
pos_x = []
pos_y = []
neg_x = []
neg_y=  []
for tweet in tweets:
    if tweet["sentiment"]>0:
        pos_x.append(tweet["sentiment"])
        pos_y.append(tweet["subjectivity"])
        
for tweet in tweets:
    if tweet["sentiment"]<0:
        neg_x.append(tweet["sentiment"])
        neg_y.append(tweet["subjectivity"])
        
for tweet in tweets:
    if tweet["location"]:
        locations.append(tweet["location"])
        
        
from collections import Counter
myDict=Counter(locations)
myDict= dict(myDict)


from pygal.maps.world import World
wm = World()
wm.force_uri_protocol = 'http'

wm.title="Tweets from the world"
wm.add('North America',myDict)

wm.render_to_file('map.svg')

#worldmap_chart = pygal.maps.world.World()
#worldmap_chart.title = 'Countries by Tweets'
#worldmap_chart.add('us1', [1])
#worldmap_chart.add('sg', [1,1,2,1,1])
#worldmap_chart.add('th', [1])
#a = worldmap_chart.render()
#print(len(a))
#file=open("graf.html","w")
#file.write(str(a))
#file.close()
#worldmap_chart.render_to_file('world.svg')
#        
x= [tweet["sentiment"] for tweet in tweets]
y = [tweet["subjectivity"] for tweet in tweets]

#########################################Plots################################


#------------------------------LinePlot
fig, ax = plt.subplots(facecolor='#000000')
plt.plot(pos_x, color='#FF8C00')
plt.plot(neg_x)
plt.rcParams['axes.facecolor'] = "#000000"
plt.rcParams['lines.linewidth'] = 2
plt.rcParams["figure.figsize"] = [11,4]
ax.tick_params(axis='x', colors='#4666FF')
ax.tick_params(axis='y', colors='yellow')
ax.set_xlabel("Number of Tweets",color = 'white')
ax.set_ylabel("Polarity of the tweet",color = 'white')

# Be sure to specify facecolor or it won't look right in Illustrator
#fig.savefig("output.pdf", facecolor=fig.get_facecolor(), transparent=True)
#-----------------------------ScatterPlot
##POSTIVE AND NEGATIVE DIFFERENT COLORS PLX
fig, ax = plt.subplots(facecolor='#000000')
plt.scatter(pos_y,pos_x, color='#9966ff')
plt.scatter(neg_y,neg_x)
#plt.scatter(x,y)
plt.rcParams['axes.facecolor'] = "#000000"
plt.rcParams['lines.linewidth'] = 2
plt.rcParams["figure.figsize"] = [11,4]
ax.tick_params(axis='x', colors='red')
ax.tick_params(axis='y', colors='red')
ax.set_xlabel("Number of Tweets",color = 'white')
ax.set_ylabel("Polarity of the tweet",color = 'white')

#----------------------------HeatPlot
sns.heatmap([x,y])
#----------------------------asdasdPlot

fig, ax = plt.subplots(facecolor='#000000')
plt.plot(pos_x, color='#FF8C00')
plt.rcParams['axes.facecolor'] = "#000000"
plt.rcParams['lines.linewidth'] = 2
plt.rcParams["figure.figsize"] = [22,4]
plt.xticks([i*100 for i in range(30)])
ax.tick_params(axis='x', colors='#4666FF')
ax.tick_params(axis='y', colors='yellow')
ax.set_xlabel("Number of Tweets",color = 'white')
ax.set_ylabel("Polarity of the tweet",color = 'white')


from pygal.maps.world import World

wm = World()
wm.force_uri_protocol = 'http'
wm.title="Tweets from the world"
wm.add('Tweets',myDict)

wm.render_to_file('map.svg')
