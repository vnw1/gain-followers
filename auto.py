import pprint
from time import sleep
from InstagramAPI import InstagramAPI
import pandas as pd


users_list = []
following_users = []
follower_users = []

class InstaBot:

    def __init__(self):
        self.api = InstagramAPI("your_username", "your_password")

    def get_likes_list(self,username):
        api = self.api
        api.login()
        api.searchUsername(username) #Gets most recent post from user
        result = api.LastJson
        username_id = result['user']['pk']
        user_posts = api.getUserFeed(username_id)
        result = api.LastJson
        media_id = result['items'][0]['id']

        api.getMediaLikers(media_id)
        users = api.LastJson['users']
        for user in users:
            users_list.append({'pk':user['pk'], 'username':user['username']})
        bot.follow_users(users_list)


    def follow_users(self,users_list):
        api = self.api
        api.login()
        api.getSelfUsersFollowing()
        result = api.LastJson
        for user in result['users']:
            following_users.append(user['pk'])
        for user in users_list:
            if not user['pk'] in following_users:
                print('Following @' + user['username'])
                api.follow(user['pk'])
                # set this really long to avoid from suspension
                sleep(20)
            else:
                print('Already following @' + user['username'])
                sleep(10)

    def unfollow_users(self):
        api = self.api
        api.login()
        api.getSelfUserFollowers()
        result = api.LastJson
        for user in result['users']:
            follower_users.append({'pk':user['pk'], 'username':user['username']})

        api.getSelfUsersFollowing()
        result = api.LastJson
        for user in result['users']:
            following_users.append({'pk':user['pk'],'username':user['username']})
        for user in following_users:
            if not user['pk'] in follower_users:
                print('Unfollowing @' + user['username'])
                api.unfollow(user['pk'])
                # set this really long to avoid from suspension
                sleep(20) 


bot =  InstaBot()
# To follow users run the function below
# change the username ('instagram') to your target username
bot.get_likes_list('instagram')

# To unfollow users uncomment and run the function below
# bot.unfollow_users()