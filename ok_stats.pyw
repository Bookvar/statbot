
# application_id 512000898698
# application_key CLIHLCKGDIHBABABA
# application_secret_key 0FE3705B47B45ADB5BDE14D3

# access_token  tkn1gm9zHPSu4dSQL6pWK97RvjLb8nZJIQ1fs3v5XXLc7Cak2ma4pzy8LgGTdePHPkEPj
# session_secret_key  18c93ad1bdc3683cf7c74b72e677ac38

import time
import ast
from datetime import datetime, timedelta, date
import requests
from data import config
# pip install gspread
import gspread
# pip install ok_api
from ok_api import OkApi

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


# COUNTRIES = ['BN','AB','AM','AZ','BL','GE','KZ','KG','LV','LT','ML','OS','TJ','UZ','SBZ','UA','SRU' ]
COUNTRIES = ['BL']
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
    print(r.json())
    response = r.json()
    # print(date_curr,' ',timestamp_from,' ',timestamp_to,' ' , response)
    views = ((response.get('renderings', None))[0]).get('value', None)
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
            num_filled_cells = len(column_values_list) - 3
            # дата, с которой продолжим заполнять
            date_start = date_begin + timedelta(days=num_filled_cells)
            date_list = [date_start + timedelta(days=x)
                         for x in range(numdays-num_filled_cells)]
            #  цикл по дням
            for day in date_list:
                date_curr = day
                # запрос views на определенную дату
                views_curr = get_views(group_id, date_curr)
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
