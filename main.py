# -*- coding: utf-8 -*-
"""
Created on Wed Jan  2 21:26:44 2019

@author: ratin
"""

import tweepy
from textblob import TextBlob
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import requests

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
        print(tweet["location"],tweet["sentiment"],tweet["subjectivity"])
        
        
        
x= [tweet["sentiment"] for tweet in tweets]


def geocoder(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address=Burbank+CA&key=AIzaSyAFzN_oHN633l3pAOwJbbV8GwwdnPfvrDM'.format("+".join(address).replace(",",""))
    r = requests.get(url)
    country = r.json()["results"][0]["address_components"][3]["short_name"]
    return country
