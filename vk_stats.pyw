import time
import ast
# import datetime
from datetime import datetime, timedelta, date
import requests
from data import config
# import os, time, sys
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
# print(date_begin, ' - ', date_end, ' = ',number_dates)


COUNTRIES = ['BL']
VK_GROUP_IDS = config.VK_GROUP_IDS
VK_GROUP_COL = config.VK_GROUP_COL
access_token = config.VK_ACCESS_TOKEN

app_id = config.VK_APP_ID
interval = "day"

# access_token = "28748b0ec022928947321d16eabcca18dce38b6f720cb1381b257c125d030127fe028061072cd20c8d950"

# преобразуем имя колонки в номер


def shits_column_name_to_number(column_name):
    column_name = column_name.upper()
    sum = 0
    for i in column_name:
        sum = sum * 26
        sum = sum + (ord(i) - ord('A'))
    return sum+1


def get_views(group_id, date_curr):
    # date_from = date(2021, 5, 26)
    date_from = date_curr
    date_to = date_from+timedelta(days=1)
    # print(date_from)
    # print(date_to)
    timestamp_from = int(time.mktime(date_from.timetuple()))
    timestamp_to = int(time.mktime(date_to.timetuple())-1)
    # print(timestamp_from, timestamp_to)
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
    # print(views)
    return views


def main():
    # цикл по странам
    for country in COUNTRIES:
        # выбираем лист страны
        worksheet = sheet.worksheet(country)
        # берём список групп VK страны
        eVK_GROUP_IDS = ast.literal_eval(VK_GROUP_IDS)
        GROUP_IDS = eVK_GROUP_IDS.get(country, None)
        for group_id in GROUP_IDS:
            eVK_GROUP_COL = ast.literal_eval(VK_GROUP_COL)
            GROUP_COL = eVK_GROUP_COL.get(country, None)
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
            date_list = [date_start + timedelta(days=x) for x in range(numdays-num_filled_cells)]
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
                # print("{0} - {1}".format(day, views_curr)


main()
