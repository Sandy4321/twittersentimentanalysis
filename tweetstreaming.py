# -*- coding: utf-8 -*-
"""
Created on Mon May 18 16:54:49 2015

@author: Deepna
"""

import tweepy
import sys
import pymongo

consumer_key="IJgRrksytlDQa86234CZGZdSd"
consumer_secret="BFgX7oxgHtkInj5p8uzprSGLUuPah4gwXmrhYk5tY02zGNPhgl"

access_token="318537895-ixn2XK83HoVAdT5g7Q4sNNJ4AFOMm2RLTY2cxC4L"
access_token_secret="jAeDFEnzCMZJwG12zQSXTpAtOrI5HyFJauzLAWwt36Ckj"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        super(tweepy.StreamListener, self).__init__()

        self.db = pymongo.MongoClient('localhost', 27017).rockets

    def on_status(self, status):
        status.text=str(unicode(status.text).encode("utf-8"))
        print status.text , "\n"

        data ={}
        data['text'] = status.text
        data['created_at'] = status.created_at
        data['geo'] = status.geo
        data['source'] = status.source

        self.db.rockets.insert(data)


    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
sapi.filter(track=['rockets']) 
