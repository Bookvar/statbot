
# pip install facebook_business

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

my_app_id = '268102335015822'
my_app_secret = 'ff9adedcf4335291e3c3545f6d3ab1b1'
my_access_token = '268102335015822|XEyPdjBbdHUfnbFcMKhm26HP1mw'
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
my_account = AdAccount('act_{100000510497873}')
campaigns = my_account.get_campaigns()
print(campaigns)

print("Всё") 
exit()




'''
How do I access Facebook API using Python?
Here are the steps for it.
Go to link developers.facebook.com, create an account there.
Go to link developers.facebook.com/tools/explorer.
Go to “My apps” drop down in the top right corner and select “add a new app”. ...
Again get back to the same link developers.facebook.com/tools/explorer. ...
Then, select “Get Token”.
Подобнее, https://towardsdatascience.com/how-to-use-facebook-graph-api-and-extract-data-using-python-1839e19d6999
'''



# pip install -e git+https://github.com/mobolic/facebook-sdk.git#egg=facebook-sdk

'''
https://coderoad.ru/3058723/%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D0%BE-%D0%BF%D0%BE%D0%BB%D1%83%D1%87%D0%B8%D1%82%D1%8C-%D0%BC%D0%B0%D1%80%D0%BA%D0%B5%D1%80-%D0%B4%D0%BE%D1%81%D1%82%D1%83%D0%BF%D0%B0-%D0%B4%D0%BB%D1%8F-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F-Facebook-Graph-API
'''
#!/usr/bin/python
# coding: utf-8

import facebook
import requests

FACEBOOK_APP_ID     = '268102335015822'
FACEBOOK_APP_SECRET = 'ff9adedcf4335291e3c3545f6d3ab1b1'
FACEBOOK_PROFILE_ID = '100000510497873'


app_id = '268102335015822'
app_secret = 'ff9adedcf4335291e3c3545f6d3ab1b1'

graph = facebook.GraphAPI()

# exactly what you're after ;-)
access_token = graph.get_app_access_token(app_id, app_secret) 

graph = facebook.GraphAPI(access_token)
user = "vbnrtdbx"
profile = graph.get_object(user)
posts = graph.get_connections(profile["id"], "posts")


while True:
    try:
        # Perform some action on each post in the collection we receive from
        # Facebook.
        [some_action(post=post) for post in posts["data"]]
        # Attempt to make a request to the next page of data, if it exists.
        posts = requests.get(posts["paging"]["next"]).json()
    except KeyError:
        # When there are no more pages (['paging']['next']), break from the
        # loop and end the script.
        break
# fb_response = graph.put_wall_post('Hello from Python', profile_id = FACEBOOK_PROFILE_ID)






# Try to post something on the wall.
# try:
#     fb_response = facebook_graph.put_wall_post('Hello from Python', \
#                                                profile_id = FACEBOOK_PROFILE_ID)
#     print (fb_response)
# except facebook.GraphAPIError as e:
#     print ('Something went wrong:', e.type, e.message)

print("Всё") 
exit()


# application_id 268102335015822
# application_secret_key ff9adedcf4335291e3c3545f6d3ab1b1

# access_token  268102335015822|XEyPdjBbdHUfnbFcMKhm26HP1mw
# session_secret_key  

# pip install --upgrade python-facebook-api

import pyfacebook


api = pyfacebook.Api(app_id='268102335015822',   # use the second method.
                    app_secret='ff9adedcf4335291e3c3545f6d3ab1b1',
                    long_term_token='268102335015822|XEyPdjBbdHUfnbFcMKhm26HP1mw')

# api = pyfacebook.Api(app_id='268102335015822',   # use the second method.
#                     app_secret='ff9adedcf4335291e3c3545f6d3ab1b1',
#                     short_token='')


# api = pyfacebook.Api(long_term_token='268102335015822|XEyPdjBbdHUfnbFcMKhm26HP1mw')  # your long term access token



tok=pyfacebook.AuthAccessToken.token_type


result = api.get_token_info(return_json=True)
print(result) 

result = api.get_app_token(return_json=True)
print(result) 

result = api.auth_session
print(result) 

# result = api.get_pages_info('vbrtdbx')


print("Всё") 

# result1 = api.get_posts(ids='vbnrtdbx', return_json=True)
# print(result1) 

result2 = api.get_page_info(page_id='3058518357591033')  # you can make return_json True to see more fields

print(result2) 
print("Всё") 
'''
{'data': {'app_id': 'xxx',
'type': 'USER',
'application': 'xxx',
'data_access_expires_at': 1555231532,
'expires_at': 1553244944,
'is_valid': True,
'issued_at': 1548060944,
'scopes': ['public_profile'],
'user_id': 'xxx'}}
'''

import facebook 
token = 'your token' 
graph = facebook.GraphAPI(token) 
profile = graph.get_object("me") 
friends = graph.get_connections("me", "friends") 
# friend_list = [friend['name'] for friend in friends['data']] 
# print friend_list





import time
import ast
from datetime import datetime, timedelta, date
import requests
from data import config
# pip install gspread
import gspread
# pip install facebook ? 

from facebook import Facebook

api_key = 'Your App API Key'
secret  = 'Your App Secret Key'

session_key = 'your infinite Session key of user'

fb = Facebook(api_key, secret)
fb.session_key = session_key

# now use the fb object for playing around







# получаем доступ к таблице гугл
spreadsheetId = "1DSDFv5uXJkTcDOyuG2Yx_IW_zw4DfTgp9u5dpJzzLZ4"
gc = gspread.service_account(filename='sputnik-analitics-python.json')
sheet = gc.open_by_key(spreadsheetId)

# первая дата, с которой всё заносим 01.04.2021
date_begin = date(2021, 4, 1)
#  последняя дата, на которую должны занести данные, это вчера
date_end = (datetime.today().replace(hour=0, minute=0,
            second=0, microsecond=0) - timedelta(days=1)).date()
# таким образом мы знаем сколько записей должно быть в таблице, как разницу дат в днях
numdays = (date_end - date_begin).days + 1

# 
COUNTRIES = ['BN','AB','AM','AZ','BL','GE','ML','OS','LV','LT','TJ','UZ','KZ','KG','SBZ','UA','SRU' ]
# COUNTRIES = ['BL','ML','UA']
# gid='53622940434687'
OK_GROUP_IDS = config.OK_GROUP_IDS
OK_GROUP_COL = config.OK_GROUP_COL
access_token = config.OK_ACCESS_TOKEN
application_key=config.OK_APPLICATION_KEY
application_secret_key=config.OK_APPLICATION_SECRET_KEY

# interval = "day"

# функция для преобразования имени колонки в номер
def shits_column_name_to_number(column_name):
    column_name = column_name.upper()
    sum = 0
    for i in column_name:
        sum = sum * 26
        sum = sum + (ord(i) - ord('A'))
    return sum+1

# функция запроса к api ok
def get_views(group_id, date_curr):

    date_from = date_curr
    date_to = date_from+timedelta(days=1)
    timestamp_from = int(time.mktime(date_from.timetuple())*1000)
    timestamp_to = int(time.mktime(date_to.timetuple())*1000)

    ok = OkApi(access_token=access_token,
            application_key=application_key,
            application_secret_key=application_secret_key)

    r = ok.group.getStatTrends(
        gid=group_id, start_time=timestamp_from, end_time=timestamp_to, fields='RENDERINGS')
    # print(r.json())
    response = r.json()
    # print(date_curr,' ',timestamp_from,' ',timestamp_to,' ' , response)
    try: 
        views = ((response.get('renderings', None))[0]).get('value', None)
    except Exception as ex:
        views = ""
    return views


def main():
    """
    """
    # цикл по странам
    for country in COUNTRIES:
        print(country)
        # выбираем лист страны
        worksheet = sheet.worksheet(country)
        # берём список групп VK страны
        eOK_GROUP_IDS = ast.literal_eval(OK_GROUP_IDS)
        GROUP_IDS = eOK_GROUP_IDS.get(country, None)
        if GROUP_IDS == None:
            continue
        for group_id in GROUP_IDS:
            eOK_GROUP_COL = ast.literal_eval(OK_GROUP_COL)
            GROUP_COL = eOK_GROUP_COL.get(country, None)
            # берем индекс группы
            idx = GROUP_IDS.index(group_id)
            column_name = GROUP_COL[idx]
            column_num = shits_column_name_to_number(column_name)
            # берём все значения в  колонке канала
            column_values_list = worksheet.col_values(column_num)
            # всего заполненнх значений
            num_filled_cells = max(0, len(column_values_list) - 3)
            # дата, с которой продолжим заполнять
            date_start = date_begin + timedelta(days=num_filled_cells)
            date_list = [date_start + timedelta(days=x)
                         for x in range(numdays-num_filled_cells)]
            #  цикл по дням
            for day in date_list:
                date_curr = day
                # запрос views на определенную дату
                views_curr = get_views(group_id, date_curr)
                if (views_curr != ""):
                    print(day, ' ',  views_curr)
                    num_filled_cells += 1
                    row_num = num_filled_cells + 3
                    worksheet.update_cell(row_num, 1, str(date_curr))
                    worksheet.update_cell(row_num, column_num, views_curr)
                    time.sleep(3)


    '''
    # api.ok.ru/fb.do
    # ?application_key=CLIHLCKGDIHBABABA
    # &fields=RENDERINGS
    # &format=json
    # &gid=53622940434687
    # &method=group.getStatTrends
    # &start_time=1617224400
    # &sig=7921092a9be22624c15597b1b44a661d
    # &access_token=tkn1s5Zr9dD9CdvfnATQNWEIw89poz6cnWX4ZLoAAc6iLGAFq8dhcuuGr3ECTf5hvXO5W

    # ok4 = OkApi(access_token='tkn1cAiaWbmBWVB3tZhqtXMStM4KcJSDcJ69fbXjIxVoLxw8AdoYTRnhv7CAok20Z5nW4',
    #             application_key='CLIHLCKGDIHBABABA',
    #             application_secret_key='0FE3705B47B45ADB5BDE14D3')



            

    response4 = ok4.group.getStatTrends(
        gid='53622940434687', start_time=timestamp_from, end_time=timestamp_to, fields='RENDERINGS')


    print(response4.json())

    response5 = ok4.group.getStatTrends(
        gid='53545326018734', start_time=timestamp_from, end_time=timestamp_to, fields='RENDERINGS')


    print(response5.json())

    '''
    '''
    COMMENTS
    COMPLAINTS
    CONTENT_OPENS
    ENGAGEMENT
    FEEDBACK
    HIDES_FROM_FEED
    LEFT_MEMBERS
    LIKES
    LINK_CLICKS
    MEMBERS_COUNT
    MEMBERS_DIFF
    MUSIC_PLAYS
    NEGATIVES
    NEW_MEMBERS
    NEW_MEMBERS_TARGET
    PAGE_VISITS
    PHOTO_OPENS
    REACH
    REACH_EARNED
    REACH_MOB
    REACH_MOBWEB
    REACH_OWN
    REACH_WEB
    RENDERINGS
    RESHARES
    TOPIC_OPENS
    VIDEO_PLAYS
    VOTES'
    '''


if __name__ == '__main__':
    main()
