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
from pygal.style import Style
KEY= "G5XlhCqsGp7pxVgAjGTFu04yYvnD8esq"


consumer_key =  '2XZ8WwA60fjcn30nUwMcZGNoZ'
consumer_secret = 'dlWKue8WH17vPRJO3bUJb9w4I1KJHQaD6MV7W0eTJFmeKQ6Gcm'
access_token = '753985003328012288-tPRbv9Za68YBLdelJEznkud2vJSkxQj'
access_token_secret = 'mEXfWUrHdwKLDLlqObzWsI9AHB6pdpnM1xNFH0IV8Pmju'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

tweets = []
for page in tweepy.Cursor(api.search , q="#english" , count = 20,languages=["en"],tweet_mode='extended').pages(1):
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

#########################################Plots################################3
#------------------------------LinePlot
fig, ax = plt.subplots(facecolor='#000000')
plt.plot(x, color='#9966ff')
plt.rcParams['axes.facecolor'] = "#000000"
plt.rcParams['lines.linewidth'] = 2
ax.tick_params(axis='x', colors='red')
ax.tick_params(axis='y', colors='red')
ax.set_xlabel("Number of Tweets",color = 'white')
ax.set_ylabel("Polarity of the tweet",color = 'white')


# Be sure to specify facecolor or it won't look right in Illustrator
#fig.savefig("output.pdf", facecolor=fig.get_facecolor(), transparent=True)
#-----------------------------ScatterPlot
fig, ax = plt.subplots(facecolor='#000000')
plt.scatter(x,y, color='#9966ff')
plt.rcParams['axes.facecolor'] = "#000000"
plt.rcParams['lines.linewidth'] = 2
ax.tick_params(axis='x', colors='red')
ax.tick_params(axis='y', colors='red')
ax.set_xlabel("Number of Tweets",color = 'white')
ax.set_ylabel("Polarity of the tweet",color = 'white')

#----------------------------HeatPlot
sns.heatmap([x,y])  

#     return soup


from pygal.maps.world import World

wm = World()
wm.force_uri_protocol = 'http'

wm.title="Tweets from the world"
wm.add('North America',{'mx': 3, 'es': 1, 'us': 5, 'gb': 1, 'ca': 1, 'ly': 1, 'sa': 1, 'th': 1, 'my': 1, 'tw': 1})

wm.render_to_file('map.svg')
