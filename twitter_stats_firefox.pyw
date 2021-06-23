'''
Переписал сниппет под firefox.
Драйвер берём https://github.com/mozilla/geckodriver/releases
Последий релиз был 0.29.1
'''

import ast
import os
import sys
import time
from datetime import date, datetime, timedelta

# pip install gspread
import gspread
import pyautogui  # pip install pyautogui
# Подключаем библиотеки для работы с таблицами
import requests
from dateutil.relativedelta import relativedelta  # pip install python-dateutil
from selenium import webdriver  # pip install selenium
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

from data import config



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

# COUNTRIES = ['AB', 'AM', 'AZ', 'GE', 'BL', 'ML',
#  'OS',  'LV', 'LT', 'TJ', 'UZ', 'KZ', 'KG', 'BN', 'UA', 'SRU']
COUNTRIES = ['AB','MMV']

TW_CHANNELS = config.TW_CHANNELS
COLUMNS_TW_CHANNELS = config.COLUMNS_TW_CHANNELS
TITLES_TW_CHANNELS = config.TITLES_TW_CHANNELS
'''
#  Для перевода месяцев на русском в номер месяца
RU_MONTH_VALUES = {
    'января': 1,
    'февраля': 2,
    'марта': 3,
    'апреля': 4,
    'мая': 5,
    'июня': 6,
    'июля': 7,
    'августа': 8,
    'сентября': 9,
    'октября': 10,
    'ноября': 10,
    'декабря': 12,
    'янв.': 1,
    'февр.': 2,
    'мар.': 3,
    'апр.': 4,
    'июн.': 6,
    'июл.': 7,
    'авг.': 8,
    'сент.': 9,
    'окт.': 10,
    'нояб.': 10,
    'дек.': 12,

}
'''
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

# переход на первое число месяца левого календаря


def first_day_calendar_left(driver):
    # left_calendar_date_id = driver.find_element_by_xpath('//div[@class="calendar-date"]/table/tbody/tr[1]/td[@class="available"]')
    left_calendar_date_id = driver.find_element_by_xpath(
        '//div[@class="calendar left"]/div[@class="calendar-date"]/table/tbody/tr[1]/td[@class="available"]')
    time.sleep(1)
    left_calendar_date_id.click()
    input_id = driver.find_element_by_xpath(
        '//div[@class="calendar left"]/input')
    time.sleep(1)
    old_value = input_id.get_property('value')
    curr_date_begin = datetime.strptime(old_value, '%m/%d/%Y')
    return curr_date_begin

# переход на первое доступное число месяца правого календаря
def first_day_calendar_right(driver):
    right_calendar_date_id = driver.find_element_by_xpath(
        '//div[@class="calendar right"]/div[@class="calendar-date"]/table/tbody/*/td[@class="available in-range"]') 
    time.sleep(1)
    right_calendar_date_id.click()
    input_id = driver.find_element_by_xpath(
        '//div[@class="calendar right"]/input')
    time.sleep(1)
    old_value = input_id.get_property('value')
    curr_date_end = datetime.strptime(old_value, '%m/%d/%Y')
    return curr_date_end

def get_date_begin(driver):
    input_id = driver.find_element_by_xpath('//div[@class="calendar left"]/input')
    old_value = input_id.get_property('value')
    curr_date_begin = datetime.strptime(old_value, '%m/%d/%Y')
    return curr_date_begin

def get_date_end(driver):
    input_id = driver.find_element_by_xpath('//div[@class="calendar right"]/input')
    old_value = input_id.get_property('value')
    curr_date_end = datetime.strptime(old_value, '%m/%d/%Y')
    return curr_date_end

def main():

    #  Подготавливаем граббер Firefox

    binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
    # "C:\\Users\\mitkevich\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\t2200nfq.statbot"
    profile = FirefoxProfile(
        "C:\\Users\\mitkevich\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\t2200nfq.statbot")  # "C:\\Users\\bookvar\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\v2qtafeu.statbot"
    driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary,
                               executable_path="C:\\bot\\statbot\\BrowserDrivers\\geckodriver.exe")
    #    , log_path='geckodriver.log'

    # цикл по странам
    for country in COUNTRIES:
        # выбираем лист страны
        print(country)
        worksheet = sheet.worksheet(country)

        # берём список каналов Youtube страны
        eTW_CHANNELS = ast.literal_eval(TW_CHANNELS)
        GROUP_CHANNELS = eTW_CHANNELS.get(country, None)

        for channel in GROUP_CHANNELS:

            # Переключаем на нужный аккаунт  "https://analytics.twitter.com/user/MaratMitkevich/tweets"
            country_url = 'https://analytics.twitter.com/user/'+channel+"/tweets"
            driver.maximize_window()
            driver.get(country_url)
            time.sleep(3)

            eCOLUMNS_CHANNELS = ast.literal_eval(COLUMNS_TW_CHANNELS)
            COL_CHANNELS = eCOLUMNS_CHANNELS.get(country, None)
            eTITLES_TW_CHANNELS = ast.literal_eval(TITLES_TW_CHANNELS)
            titles_tw_channels = eTITLES_TW_CHANNELS.get(country, None)
            # берем индекс группы
            idx = GROUP_CHANNELS.index(channel)
            title_channel = titles_tw_channels[idx]
            column_name = COL_CHANNELS[idx]
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

                date_curr = datetime.combine(day, datetime.min.time())

                elem_id = driver.find_element_by_id("daterange-button")  #
                elem_id.click()
                time.sleep(1)

                # РАБОТА С ЛЕВЫМ КАЛЕНДАРЁМ
                # смотрим месяц
                curr_date_begin = get_date_begin(driver)
                while (day.month < curr_date_begin.month):
                    # листаем календарь влево
                    icon_id = driver.find_element_by_xpath(
                        '//div[@class="calendar left"]/div[@class="calendar-date"]/table/thead/tr[1]/th[@class="prev available"]/span')  # right
                    icon_id.click()
                    left_calendar_date_id = driver.find_element_by_xpath(
                        '//div[@class="calendar left"]/div[@class="calendar-date"]/table/tbody/*/td[@class="available"]')
                    left_calendar_date_id.click()
                    curr_date_begin = get_date_begin(driver)
                while (day.month > curr_date_begin.month):
                    # листаем календарь вправо
                    icon_id = driver.find_element_by_xpath(
                        '//div[@class="calendar left"]/div[@class="calendar-date"]/table/thead/tr[1]/th[@class="next available"]/span')  # right
                    icon_id.click()
                    left_calendar_date_id = driver.find_element_by_xpath(
                        '//div[@class="calendar left"]/div[@class="calendar-date"]/table/tbody/*/td[@class="available"]')
                    left_calendar_date_id.click()
                    curr_date_begin = get_date_begin(driver)

                # ищем текущую дату в левом календаре
                time.sleep(1)
                elem_id = driver.find_element_by_xpath(
                    '//td[contains(@class,"available active start-date")]')
                # if (elem_id.text == str(curr_date_begin.day)):
                if (elem_id.text == str(day.day)):
                    elem_id.click()
                else:
                    elem_ids = driver.find_elements_by_xpath(
                        '//td[contains(@class,"available")]') # in-range
                    for elem_id in elem_ids:
                        # if (elem_id.text == str(curr_date_begin.day)):
                        if (elem_id.text == str(day.day)):
                            hhh = elem_id.get_attribute("class") 
                            if hhh == "available off":
                                continue
                            else:
                                elem_id.click()
                                break
                time.sleep(1)

                # РАБОТА С ПРАВЫМ КАЛЕНДАРЁМ
                # смотрим месяц
                curr_date_end = get_date_end(driver)
                while (day.month < curr_date_end.month):
                    # листаем календарь влево
                    icon_id = driver.find_element_by_xpath(
                        '//div[@class="calendar right"]/div[@class="calendar-date"]/table/thead/tr[1]/th[@class="prev available"]/span')  # 
                    icon_id.click()
                    right_calendar_date_id = driver.find_element_by_xpath(
                        '//div[@class="calendar right"]/div[@class="calendar-date"]/table/tbody/*/td[@class="available in-range"]')
                    right_calendar_date_id.click()
                    curr_date_end = get_date_end(driver)
                while (day.month > curr_date_end.month):
                    # листаем календарь вправо
                    icon_id = driver.find_element_by_xpath(
                        '//div[@class="calendar right"]/div[@class="calendar-date"]/table/thead/tr[1]/th[@class="next available"]/span')  # right
                    icon_id.click()
                    right_calendar_date_id = driver.find_element_by_xpath(
                        '//div[@class="calendar right"]/div[@class="calendar-date"]/table/tbody/*/td[@class="available"]')
                    right_calendar_date_id.click()
                    curr_date_end = get_date_end(driver)

                # ищем текущую дату в правом календаре
                time.sleep(1)
                elem_id = driver.find_element_by_xpath(
                    '//td[contains(@class,"available active start-date")]')
                # if (elem_id.text == str(curr_date_end.day)):
                if (elem_id.text == str(day.day)):
                    elem_id.click()
                else:
                    elem_ids = driver.find_elements_by_xpath(
                        '//td[contains(@class,"available")]') # in-range
                    for elem_id in elem_ids:
                        # if (elem_id.text == str(curr_date_end.day)):
                        if (elem_id.text == str(day.day)):    
                            hhh = elem_id.get_attribute("class") 
                            if hhh == "available off":
                                continue
                            else:
                                elem_id.click()
                                break


                btn_id = driver.find_element_by_class_name('applyBtn')
                #  Пока по кнопке не кликаем или кликаем?
                btn_id.click()

                print("Календарь выставили")
                # //*[@id="tweet-impression-chart"]/div[2]/table/tbody/tr[1]/td[3]


                chart_id = driver.find_element_by_id('tweet-impression-header')
                action = ActionChains(driver)
                action.move_to_element(chart_id).click().perform()
                chart_id = driver.find_element_by_id('tweet-impression-chart')
                action = ActionChains(driver)
                action.move_to_element(chart_id).click().perform()

                time.sleep(3)
                barshart_id = driver.find_element_by_xpath(
                    '//div[@class="barchart-tooltip"]/table/tbody/tr[1]/td[3]')  #
                views_curr = barshart_id.text
                views_curr = views_curr.replace(',', '')

                #  заполняем значения
                # if (day == curr_end_date.date()):
                print(day, ' ',  views_curr)
                num_filled_cells += 1
                row_num = num_filled_cells + 3
                worksheet.update_cell(row_num, 1, str(date_curr)[:10])
                worksheet.update_cell(row_num, column_num, views_curr)
                time.sleep(1)

    driver.quit()
    print("Данные занесены")


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
