import time
import datetime
import requests
from data import config
# pip install gspread
import gspread

# получаем доступ к таблице гугл
spreadsheetId = "1DSDFv5uXJkTcDOyuG2Yx_IW_zw4DfTgp9u5dpJzzLZ4"
gc = gspread.service_account(filename='sputnik-analitics-python.json')
sheet = gc.open_by_key(spreadsheetId)

# первая дата, с которой всё заносим 01.04.2021
date_begin = datetime.date(2021, 4, 1)
#  последняя дата, на которую должны занести данные, это вчера
date_end = (datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1))
print(yesterday_date)


COUNTRIES = ['BL']
VK_GROUP_IDS = config.VK_GROUP_IDS

app_id = config.VK_APP_ID
interval = "day"

key = "f0dfe844f0dfe844f0dfe8448cf0a87729ff0dff0dfe84490706c387d29110877481f2a"
access_token = "72b487c44d2891a38ece84b942a72d60db7c15e04c4a7056c6a7ce7c9aaa8fa5e6ef37176d3e665b31465"
date_from = datetime.date(2021, 5, 26)
date_to = date_from+datetime.timedelta(days=1)
print(date_from)
print(date_to)

timestamp_from = int(time.mktime(date_from.timetuple()))
timestamp_to = int(time.mktime(date_to.timetuple())-1)
print(timestamp_from, timestamp_to)


def main():
    # цикл по странам
    for country in COUNTRIES:
        # берём список групп VK страны
        GROUP_IDS = eval(VK_GROUP_IDS.get(country, None))
        for group_id in GROUP_IDS:
            r = requests.get("https://api.vk.com/method/stats.get",
                             params={
                                 "group_id": group_id,
                                 "app_id": app_id,
                                 "timestamp_from": timestamp_from,
                                 "timestamp_to": timestamp_to,
                                 "interval": interval,
                                 "access_token": access_token,
                                 "extended": 1,
                                 "v": "5.86"
                             }
                             )
            response = r.json()
            views = ((response.get('response', None))[0]).get(
                'visitors', None).get('views', None)
            # print(response)
            print(views)


main()
