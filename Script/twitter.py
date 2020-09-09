# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 02:08:35 2020

@author: DELL
"""

# References
#   1. https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
#   2. http://docs.tweepy.org/en/latest/
#   3. https://developer.twitter.com/en/dashboard
#   4. https://stackoverflow.com/questions/11331982/how-to-remove-any-url-within-a-string-in-python
#   5. https://stackoverflow.com/questions/39782418/remove-punctuations-in-pandas
#   6. https://stackoverflow.com/questions/20078816/replace-non-ascii-characters-with-a-single-space
#   7. https://stackoverflow.com/questions/466345/converting-string-into-datetime

import tweepy as twi
import re
import string
import pandas
import json
from datetime import datetime



consumer_key='IOd6Vb3OGxJxzwKWYUOMDOhUU'
consumer_secret='OQIKScW84qmvwj2v7iravA6iXaWMia7BWPjECe85ohvhV1GxGc'
access_token='1903789182-EkZXfEdZXu9pcp80BiqCcSZ0OHNUxOL76ZZv5ZQ'
access_token_secret='7cPLdq5nVVmGaux4fxkzloBXIn92Y0mxZfumMFVICiB1T'


emj_pat = re.compile("["
        u"\U0001F600-\U0001F64F"  
        u"\U0001F300-\U0001F5FF"  
        u"\U0001F680-\U0001F6FF" 
        u"\U0001F1E0-\U0001F1FF"  
                           "]+", flags=re.UNICODE)

    

auth=twi.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api=twi.API(auth,wait_on_rate_limit=True)

keywords='Canada OR University OR Dalhousie University OR Halifax OR Canada Education'
results=[]
result1=[]

tweets=twi.Cursor(api.search,
                  q=keywords,
                  lang="en",
                  tweet_mode="extended",
                  truncated=False).items(3500)


for tweet in tweets:
    results.append(tweet)
    

for twt in results:
    
    if "retweeted_status" in twt._json:
        re_text=twt.retweeted_status.full_text.lower()
        rmv_url_rt=re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\-|\=|\&|\%)*\b', '',re_text) 
        rmv_punct_rt="".join([ch for ch in rmv_url_rt if ch not in string.punctuation])
        rmv_punct_rt=rmv_punct_rt.replace("\r","")
        rmv_punct_rt=rmv_punct_rt.replace("\n","")
        rmvd_u_rt="".join(i for i in rmv_punct_rt if ord(i)<128)
        cleaned_rt=emojipattern.sub(r'',rmvd_u_rt)  
        twt.retweeted_status.full_text=cleaned_rt
        tweet_date_time=twt.retweeted_status.created_at.strftime("%H:%M:%S.%f - %b %d %Y")
        result1.append({"Tweet":"RT " + twt.retweeted_status.full_text,"Location":twt.user.location,"Created at":tweet_date_time})
    else:
        text=twt.full_text.lower()
        rmv_url=re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\-|\=|\&|\%)*\b', '',text)
        rmv_punct="".join([char for char in rmv_url if char not in string.punctuation])
        rmv_punct=rmv_punct.replace("\r","")
        rmv_punct=rmv_punct.replace("\n","")
        rmvd_u="".join(i for i in rmv_punct if ord(i)<128)
        cleaned=emj_pat.sub(r'',rmvd_u)
        twt.full_text=cleaned
        tweet_date_time=twt.created_at.strftime("%H:%M:%S.%f - %b %d %Y")
        result1.append({"Tweet": twt.full_text,"Location":twt.user.location,"Created at":tweet_date_time})
        



with open('tweets.json','w') as tweets_final:
    json.dump(result1,tweets_final)




