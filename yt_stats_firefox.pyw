'''
Переписал сниппет под firefox.
Драйвер берём https://github.com/mozilla/geckodriver/releases
Последий релиз был 0.29.1
'''

import os
import time
import sys
from datetime import datetime, timedelta, date
import ast
from selenium import webdriver  # pip install selenium
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
import pyautogui  # pip install pyautogui
# Подключаем библиотеки для работы с таблицами
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

#  Вычисляем дату вчерашнего дня
yesterday = (datetime.today().replace(hour=0, minute=0,
             second=0, microsecond=0) - timedelta(days=1))

COUNTRIES = ['AB', 'AM', 'AZ', 'GE', 'LV', 'LT', 'KZ', 'KG']
YOUTUBE_CHANNELS = config.YOUTUBE_CHANNELS
COLUMNS_CHANNELS = config.COLUMNS_CHANNELS
TITLES_YT_CHANNELS = config.TITLES_YT_CHANNELS


#  Для перевода месяцев на русском в номер месяца
RU_MONTH_VALUES = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апр.': 4,
    'апреля': 4,
    'мая': 5,
    'июн.': 6,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 10,
    'декабря': 12,
}

# преобразуем имя колонки в номер


def shits_column_name_to_number(column_name):
    column_name = column_name.upper()
    sum = 0
    for i in column_name:
        sum = sum * 26
        sum = sum + (ord(i) - ord('A'))
    return sum+1


def int_value_from_ru_month(date_str):
    for k, v in RU_MONTH_VALUES.items():
        date_str = date_str.replace(k, str(v))
    return date_str


def main():

    #  Подготавливаем граббер Firefox

    binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
    profile = FirefoxProfile(
        "C:\\Users\\mitkevich\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\t2200nfq.statbot")
    driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary,
                               executable_path="C:\\bot\\statbot\\BrowserDrivers\\geckodriver.exe")
    #    , log_path='geckodriver.log'

    # цикл по странам
    for country in COUNTRIES:
        # выбираем лист страны
        print(country)
        worksheet = sheet.worksheet(country)
        # Переключаем на нужный аккаунт
        country_url = 'https://studio.youtube.com/channel/'
        driver.maximize_window()
        driver.get(country_url)
        time.sleep(3)
        # ищем кнопку аватара
        elem_id = driver.find_element_by_id("avatar-btn")  #
        elem_id.click()
        time.sleep(1)
        # elem_id = driver.find_element_by_xpath('//div[@id="label" and @class="style-scope ytd-compact-link-renderer"]')
        elem_id = driver.find_element_by_link_text("Сменить аккаунт")
        elem_id.click()
        time.sleep(3)

        # берём список каналов Youtube страны
        eYOUTUBE_CHANNELS = ast.literal_eval(YOUTUBE_CHANNELS)
        GROUP_CHANNELS = eYOUTUBE_CHANNELS.get(country, None)

        for channel in GROUP_CHANNELS:
            eCOLUMNS_CHANNELS = ast.literal_eval(COLUMNS_CHANNELS)
            COL_CHANNELS = eCOLUMNS_CHANNELS.get(country, None)
            eTITLES_YT_CHANNELS = ast.literal_eval(TITLES_YT_CHANNELS)
            titles_yt_channels = eTITLES_YT_CHANNELS.get(country, None)

            # берем индекс группы
            idx = GROUP_CHANNELS.index(channel)

            title_channel = titles_yt_channels[idx]

            elem_ids = driver.find_elements_by_id("channel-title")  #
            time.sleep(2)
            # elem_ids = driver.find_element_by_xpath(
            # '//div[@id="contents" and @class="style-scope ytd-account-item-section-renderer"]')
            # time.sleep(2)
            
            i = 0
            for elem_id in elem_ids:
                if (elem_id.text == title_channel):
                    # print(elem_id.text)
                    # elem_id.click()
                    break
                i += 1
            if (i == len(elem_ids)):
                print(u'{} не найден с списке аккаунтов '.format(title_channel))
                break
            elem_ids[i].click()
            time.sleep(3)
            
            # ''' Алтернатива начало'''
            # select = Select(elem_ids)
            # select.select_by_visible_text('title_channel')
            # time.sleep(3)
            # ''' Алтернатива конец'''

            column_name = COL_CHANNELS[idx]
            column_num = shits_column_name_to_number(column_name)
            # берём все значения в  колонке канала
            column_values_list = worksheet.col_values(column_num)
            # всего заполненнх значений
            num_filled_cells = len(column_values_list) - 3
            '''
            # последние два дня перезаполняем, для этого
            if (num_filled_cells > 2):
                num_filled_cells -= 2
            '''
            # дата, с которой продолжим заполнять
            date_start = date_begin + timedelta(days=num_filled_cells)
            date_list = [date_start + timedelta(days=x)
                         for x in range(numdays-num_filled_cells)]
            #  цикл по дням
            for day in date_list:

                date_curr = datetime.combine(day, datetime.min.time())

                # запрос views на определенную дату

                # Если дата в таблице ранее чем вчера, используем метод выборки конкретного дня,
                # иначе (то есть за вчера)  используем метод последнего дня последней недели.

                if (date_curr == yesterday):
                    #  итак просто берём данные последней доступной недели
                    country_url = 'https://studio.youtube.com/channel/' + \
                        channel + '/analytics/tab-reach_viewers/period-week'
                else:
                    #  вычисляем границы даты для запроса
                    epoch = datetime.utcfromtimestamp(0)
                    ds = date_curr + timedelta(hours=7)
                    de = date_curr + timedelta(days=1) + timedelta(hours=7)
                    date_start = int((ds - epoch).total_seconds()) * 1000
                    date_end = int((de - epoch).total_seconds()) * 1000

                    country_url = 'https://studio.youtube.com/channel/' + channel + \
                        '/analytics/tab-reach_viewers/period-' + \
                        str(date_start)+','+str(date_end)

                driver.get(country_url)
                # ищем табулятор показов
                time.sleep(5)
                elem_id = driver.find_element_by_id(
                    "VIDEO_THUMBNAIL_IMPRESSIONS-tab")  # показы
                # elem_id = driver.find_element_by_id("VIEWS-tab") #просмотры
                elem_id.click()
                time.sleep(2)

                if (date_curr != yesterday):
                    elem_id = driver.find_element_by_xpath(
                        '//div[@class="label-text style-scope ytcp-dropdown-trigger"]')
                    curr_period = elem_id.text.strip()
                    # print(curr_period)

                # ищем график и клмикаем в него. при этом почему-то всплывает окошко показаний на последнюю дату, что нам и надо

                # elem_id = driver.find_element_by_xpath('//*[name()="svg"]/*[name()="g"]/*[name()="rect"]')
                elem_id = driver.find_element_by_xpath(
                    '//div[@ id="aspect-ratio-four-one-container"]')
                time.sleep(1)
                elem_id.click()
                time.sleep(3)

                elem_id = driver.find_element_by_xpath(
                    '//div[@id="title" and @class="style-scope yta-hovercard"]')
                #  забираем дату в формате по примеру "Пн, 10 мая 2021 г."
                # print(elem_id.text)
                #  преобразуем в нужный вид
                curr_end_date_text = int_value_from_ru_month(
                    elem_id.text[4:][:-3])
                curr_end_date = datetime.strptime(
                    curr_end_date_text, '%d %m %Y')
                elem_id = driver.find_element_by_xpath(
                    '//div[@id="value" and @class="style-scope yta-hovercard"]')
                views_curr = elem_id.text.replace(" ", "")
                time.sleep(3)

                #  заполняем значения
                if (day == curr_end_date.date()):
                    print(day, ' ',  views_curr)
                    num_filled_cells += 1
                    row_num = num_filled_cells + 3
                    worksheet.update_cell(row_num, 1, str(date_curr)[:10])
                    worksheet.update_cell(row_num, column_num, views_curr)
                    time.sleep(3)

    driver.quit()
    print("Данные занесены")


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
