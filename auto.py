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
        self.api.USER_AGENT = 'Instagram 10.34.0 Android (18/4.3; 320dpi; 720x1280; Huawei; P30; armani; qcom; en_US)'

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

    def get_my_profile_details(self):
        api = self.api
        api.login() 
        api.getSelfUsernameInfo()
        result = api.LastJson
        username = result['user']['username']
        full_name = result['user']['full_name']
        profile_pic_url = result['user']['profile_pic_url']
        followers = result['user']['follower_count']
        following = result['user']['following_count']
        media_count = result['user']['media_count']
        df_profile = pd.DataFrame(
            {'username':username,
            'full name': full_name,
            'profile picture URL':profile_pic_url,
            'followers':followers,
            'following':following,
            'media count': media_count,
            }, index=[0])
        df_profile.to_csv('profile.csv', sep='\t', encoding='utf-8')

    def get_my_feed(self):
        api = self.api
        image_urls = []
        api.login()
        api.getSelfUserFeed()
        result = api.LastJson
        # formatted_json_str = pprint.pformat(result)
        # print(formatted_json_str)
        if 'items' in result.keys():
            for item in result['items'][0:5]:
                if 'image_versions2' in item.keys():
                    image_url = item['image_versions2']['candidates'][1]['url']
                    image_urls.append(image_url)

        df_feed = pd.DataFrame({
                    'image URL':image_urls
                })
        df_feed.to_csv('feed.csv', sep='\t', encoding='utf-8')


bot =  InstaBot()
# To follow users run the function below
# change the username ('instagram') to your target username
bot.get_likes_list('instagram')

# To unfollow users uncomment and run the function below
# bot.unfollow_users()