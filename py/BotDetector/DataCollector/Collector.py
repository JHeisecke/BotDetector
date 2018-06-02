'''
Created on 15 may. 2018

@author: Santirrium
'''

import csv
import time
import re
import codecs
from io import StringIO
from argparse import ArgumentParser
import tweepy
from tweepy import OAuthHandler

from py.BotDetector.others import utils
from py.BotDetector.DataCollector.DBmanager import DBmanager
from py.BotDetector.DataCollector.TwUsers import TwUser

#Credenciales de twitter 
consumer_key = '4qFYcgtelubwkBlJaYlPYlEpa'
consumer_secret = 'HRSUwg5QFi0rnizqNYwIgSy4CE47pVjab8PjchIppzB60jVC9U'
access_token = '65257006-tO6cC5TVGSPmpzI3a9LO1oUEmFbKtAdY2gs9wLFnO'
access_secret = 'E6VuPitApOi6yqYm2XgmZlBKa2BkMl7OpnkksOuNYwyUq'
          
#twitter connection api
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)


def get_friends_descriptions(api, file_path, twitter_account, max_users):
    """
    Return the bios of the people that a user follows

    api -- the tweetpy API object
    twitter_account -- the Twitter handle of the user
    max_users -- the maximum amount of users to return
    """

    user_ids = []

    try:
        for page in tweepy.Cursor(api.followers_ids, id=twitter_account, count=5000).pages():
            user_ids.extend(page)

    except tweepy.RateLimitError:
        print ("RateLimitError...waiting 1000 seconds to continue")
        time.sleep(1000)
        for page in tweepy.Cursor(api.followers_ids, id=twitter_account, count=5000).pages():
            user_ids.extend(page)

    following = []

    for start in range(0, min(max_users, len(user_ids)), 100):
        end = start + 100

        try:
            following.extend(api.lookup_users(user_ids[start:end]))

        except tweepy.RateLimitError:
            print ("RateLimitError...waiting 1000 seconds to continue")
            time.sleep(1000)
            following.extend(api.lookup_users(user_ids[start:end]))
    
    csv.register_dialect('myDialect', delimiter='\t', )
    with open(file_path, 'w', newline='' ) as file:

        
        
        camposCabecera = ['name', 
                          'screen_name', 
                          'location', 
                          'url', 
                          'protected', 
                          'followers_count', 
                          'friends_count', 
                          'listed_count', 
                          'favourites_count', 
                          'statuses_count', 
                          'created_at', 
                          'utc_offset', 
                          'profile_background_color', 
                          'profile_background_image_url',
                          'profile_background_image_url_https',
                          'profile_background_tile',
                          'profile_banner_url',
                          'profile_image_url',
                          'profile_image_url_https',
                          'profile_link_color',
                          'profile_sidebar_border_color',
                          'profile_sidebar_fill_color',
                          'profile_text_color',
                          'profile_use_background_image',
                          'default_profile',
                          'default_profile_image',
                          'withheld_in_countries',
                          'withheld_scope',
                          'description']
        writer = csv.DictWriter(file, fieldnames=camposCabecera, dialect='myDialect', extrasaction='ignore')
        writer.writeheader()
        
        #Conexion a la BD BotDetecto
        dbm = DBmanager('TwUsers')
        for user in following:
            try:
                writer.writerow({'name' : utils.clear(user.name),  
                                 'screen_name': utils.clear(user.screen_name), 
                                 'location' : user.location, 
                                 'url' : user.url, 
                                 'protected' : user.protected, 
                                 'followers_count' : user.followers_count, 
                                 'friends_count' : user.friends_count, 
                                 'listed_count' : user.listed_count, 
                                 'favourites_count' : user.favourites_count, 
                                 'statuses_count' : user.statuses_count, 
                                 'created_at' : user.created_at, 
                                 'utc_offset' : user.utc_offset, 
                                 'profile_background_color' : user.profile_background_color, 
                                 'profile_background_image_url' : user.profile_background_image_url,
                                 'profile_background_image_url_https' : user.profile_background_image_url_https,
                                 'profile_background_tile' : user.profile_background_tile,
                                 'profile_banner_url' : utils.getattribute(user, 'profile_banner_url'),
                                 'profile_image_url' : user.profile_image_url,
                                 'profile_image_url_https' : user.profile_image_url_https,
                                 'profile_link_color' : user.profile_link_color,
                                 'profile_sidebar_border_color' : user.profile_sidebar_border_color,
                                 'profile_sidebar_fill_color' : user.profile_sidebar_fill_color,
                                 'profile_text_color' : user.profile_text_color,
                                 'profile_use_background_image' : user.profile_use_background_image,
                                 'default_profile' : user.default_profile,
                                 'default_profile_image' : user.default_profile_image,
                                 'withheld_in_countries' : utils.getattribute(user, 'withheld_in_countries'),
                                 'withheld_scope' : utils.getattribute(user, 'withheld_scope'),
                                 'description': utils.clear(user.description)
                                })
            except UnicodeEncodeError:
                print("No se pudo guardar: " + user.screen_name)
            
            #print("Usuario:" + user.screen_name + user.description)
            twuser = ''
            twuser = TwUser(utils.clear(user.name),  
                            utils.clear(user.screen_name), 
                            user.location, 
                            user.url, 
                            user.protected, 
                            user.followers_count, 
                            user.friends_count, 
                            user.listed_count, 
                            user.favourites_count, 
                            user.statuses_count, 
                            user.created_at, 
                            user.utc_offset, 
                            user.profile_background_color, 
                            user.profile_background_image_url,
                            user.profile_background_image_url_https,
                            user.profile_background_tile,
                            utils.getattribute(user, 'profile_banner_url'),
                            user.profile_image_url,
                            user.profile_image_url_https,
                            user.profile_link_color,
                            user.profile_sidebar_border_color,
                            user.profile_sidebar_fill_color,
                            user.profile_text_color,
                            user.profile_use_background_image,
                            user.default_profile,
                            user.default_profile_image,
                            utils.getattribute(user, 'withheld_in_countries'),
                            utils.getattribute(user, 'withheld_scope'),
                            utils.clear(user.description)
                            )
            dbm.save_record(twuser.ToDbJson())

if __name__ == "__main__":

    FILE_PATH = "dataSet.csv"
    TWITTER_ACCOUNT = "santirrium"
    MAX_USERS = 2000

    print ("Colectando datos...")
    get_friends_descriptions(api, FILE_PATH, TWITTER_ACCOUNT, max_users=MAX_USERS)
    
    print("Fin..")