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
from bs4 import BeautifulSoup

#for geocoding r.json()["results"][0]["address_components"][3]["short_name"]
#url = 'https://maps.googleapis.com/maps/api/geocode/json?address=Burbank+CA&key=AIzaSyAFzN_oHN633l3pAOwJbbV8GwwdnPfvrDM'

consumer_key =  '2XZ8WwA60fjcn30nUwMcZGNoZ'
consumer_secret = 'dlWKue8WH17vPRJO3bUJb9w4I1KJHQaD6MV7W0eTJFmeKQ6Gcm'
access_token = '753985003328012288-tPRbv9Za68YBLdelJEznkud2vJSkxQj'
access_token_secret = 'mEXfWUrHdwKLDLlqObzWsI9AHB6pdpnM1xNFH0IV8Pmju'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


tweets = []
for page in tweepy.Cursor(api.search , q="#batman" , count = 200,languages=["en"],tweet_mode='extended').pages(1):
    for tweet in page:
        hashtags_=[]
        urls=[]
        for hashtag in tweet.entities["hashtags"]:
            hashtags_.append(hashtag["text"])
#        for media in tweet.entities["media"]:
#            urls.append(media["expanded_url"])
        
        twe = {"text": tweet.full_text,
               "cleaned_text": " ".join([word for word in tweet.full_text.split() if word not in stopwords.words('english')]).replace("#","").replace("*",""),
               "location": tweet.user.location,
               "username": tweet.user.screen_name,
               "retweets": tweet.retweet_count,
               "favcount": tweet.user.favourites_count,
               "hastags": hashtags_,
               "sentiment": TextBlob(" ".join([word for word in tweet.full_text.split() if word not in stopwords.words('english')])).sentiment.polarity,
               "subjectivity": TextBlob(" ".join([word for word in tweet.full_text.split() if word not in stopwords.words('english')])).sentiment.subjectivity,
                }
        tweets.append(twe)
        
for tweet in tweets:
    if tweet["location"]:
        print(tweet["location"])
        
        
        
x= [tweet["sentiment"] for tweet in tweets]
y = [tweet["subjectivity"] for tweet in tweets]

#plots
#------------------------------LinePlot
fig, ax = plt.subplots(facecolor='#000000')
plt.plot(x)
plt.rcParams['axes.facecolor'] = "#000000"
plt.rcParams['lines.linewidth'] = 2
ax.tick_params(axis='x', colors='red')
ax.tick_params(axis='y', colors='red')
ax.set_xlabel("Number of Tweets",color = 'white')
ax.set_ylabel("Polarity of the tweet",color = 'white')


# Be sure to specify facecolor or it won't look right in Illustrator
fig.savefig("output.pdf", facecolor=fig.get_facecolor(), transparent=True)
#-----------------------------ScatterPlot
fig, ax = plt.subplots(facecolor='#000000')
plt.scatter(x,y)
plt.rcParams['axes.facecolor'] = "#000000"
plt.rcParams['lines.linewidth'] = 2
ax.tick_params(axis='x', colors='red')
ax.tick_params(axis='y', colors='red')
ax.set_xlabel("Number of Tweets",color = 'white')
ax.set_ylabel("Polarity of the tweet",color = 'white')


def geocoder_api(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=Burbank+CA&key=AIzaSyAFzN_oHN633l3pAOwJbbV8GwwdnPfvrDM'.format("+".join(address).replace(",",""))
    print(url)
    r = requests.get(url)
    country = r.json()["results"][0]["address_components"][3]["short_name"]
    return country 

def geocoder(address):
    selector1= "#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-hero-header.white-foreground > div.section-hero-header-description > div:nth-child(1) > h1".replace("nth-child","nth-of-type")
    selector = "#pane > div > div.widget-pane-content.scrollable-y > div > div > div.section-hero-header.white-foreground > div.section-hero-header-description > h2:nth-child(3) > span".replace("nth-child","nth-of-type")
    url = "https://www.google.com/maps/place/"+ address
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    res = requests.get(url,headers = headers,verify=True)
    soup = BeautifulSoup(res.text,'lxml')
    print(soup.select(selector),soup.select(selector1),url)
    return soup
