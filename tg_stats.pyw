# Получение статистики использования API по активированным вами тарифам
# https://api.tgstat.ru/usage/stat?token=c22f439d88f5cf122e9b8d281e578574
# Пример запроса от 01-04-2021 - на тарифе S вернёт последние 10 дней
# https://api.tgstat.ru/channels/views?token=c22f439d88f5cf122e9b8d281e578574&channelId=@sputniklive&startDate=1617224400&group=day

import time
import ast
from datetime import datetime, timedelta, date
import requests
from data import config
# pip install gspread
import gspread

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
COUNTRIES = ['BN','AB','AM','AZ','BL','GE','KZ','KG','ML','OS','TJ','UZ','SBZ','UA']
TG_CHANNEL_IDS = config.TG_CHANNEL_IDS
TG_CHANNEL_COL = config.TG_CHANNEL_COL
access_token = config.TG_ACCESS_TOKEN
interval = "day"

# функция для преобразования имени колонки в номер


def shits_column_name_to_number(column_name):
    column_name = column_name.upper()
    sum = 0
    for i in column_name:
        sum = sum * 26
        sum = sum + (ord(i) - ord('A'))
    return sum+1

# функция запроса к api tgstat


def get_views(channel_id, date_curr):
    date_from = date_curr
    date_to = date_from+timedelta(days=1)
    timestamp_from = int(time.mktime(date_from.timetuple()))
    timestamp_to = int(time.mktime(date_to.timetuple())-1)
    r = requests.get("https://api.tgstat.ru/channels/views",
                     params={
                         "token": access_token,
                         "channelId": channel_id,
                         "startDate": timestamp_from,
                         "endDate": timestamp_to,
                         "group": interval
                     }
                     )
    response = r.json()
    # print(date_curr,' ',timestamp_from,' ',timestamp_to,' ' , response)
    views = ((response.get('response', None))[0]).get('views_count', None)
    # views = ((response.get('response', None))[0]).get(
    #  'visitors', None).get('views', None)
    # print(views)
    return views


def main():
    # цикл по странам
    for country in COUNTRIES:
        print(country)
        # выбираем лист страны
        worksheet = sheet.worksheet(country)
        # берём список групп VK страны
        eTG_CHANNEL_IDS = ast.literal_eval(TG_CHANNEL_IDS)
        CHANNEL_IDS = eTG_CHANNEL_IDS.get(country, None)
        for channel_id in CHANNEL_IDS:
            eTG_CHANNEL_COL = ast.literal_eval(TG_CHANNEL_COL)
            CHANNEL_COL = eTG_CHANNEL_COL.get(country, None)
            # берем индекс группы
            idx = CHANNEL_IDS.index(channel_id)
            column_name = CHANNEL_COL[idx]
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
                views_curr = get_views(channel_id, date_curr)
                print(day, ' ',  views_curr)
                num_filled_cells += 1
                row_num = num_filled_cells + 3
                worksheet.update_cell(row_num, 1, str(date_curr))
                worksheet.update_cell(row_num, column_num, views_curr)
                time.sleep(3)


main()
