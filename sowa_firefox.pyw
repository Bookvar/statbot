'''
Переписал сниппет под firefox.
Драйвер берём https://github.com/mozilla/geckodriver/releases
Последий релиз был 0.29.1
'''

import gspread
from data import config
import requests
from selenium import webdriver  # pip install selenium
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import Select
import pyautogui  # pip install pyautogui
import os
import time
import sys
from datetime import datetime, timedelta

'''
# Подключаем библиотеки для работы с таблицами
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	
'''
# Подключаем библиотеки для работы с таблицами
# pip install gspread


COUNTRIES = ['AB', 'AM', 'AZ', 'BL', 'GE', 'ML', 'OS', 'LV',
             'LT', 'TJ', 'UZ', 'KZ', 'KG', 'BN', 'SBZ', 'SRU', 'UA']
BRANDS = {
    'AB': 'Sputnik Abkhazia',
    'AM': 'Sputnik Armenia',
    'AZ': 'Sputnik Azerbaijan',
    'BL': 'Sputnik Belarus',
    'GE': 'Sputnik Georgia',
    'ML': 'Sputnik Moldova',
    'OS': 'Sputnik Ossetia',
    'LV': 'Sputnik Latvia',
    'LT': 'Sputnik Lithuania',
    'TJ': 'Sputnik Tajikistan',
    'UZ': 'Sputnik Uzbekistan',
    'KZ': 'Sputnik Kazakhstan',
    'KG': 'Sputnik Kyrgyzstan',
    'BN': 'Baltnews',
    'SBZ': 'Sputnik Ближнее зарубежье',
    'SRU': 'Sputnik на русском',
    'UA': 'Ukraina.ru'
}


def main():

    #  Подготавливаем webdriver
    binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
    profile = FirefoxProfile(
        "C:\\Users\\mitkevich\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\t2200nfq.statbot")
    driver = webdriver.Firefox(firefox_profile=profile, firefox_binary=binary,
                               executable_path="C:\\bot\\statbot\\BrowserDrivers\\geckodriver.exe")

    #  Готовим таблицу
    # получаем доступ к таблице гугл
    spreadsheetId = "1DSDFv5uXJkTcDOyuG2Yx_IW_zw4DfTgp9u5dpJzzLZ4"
    gc = gspread.service_account(filename='sputnik-analitics-python.json')
    sheet = gc.open_by_key(spreadsheetId)

    #  дата, на которую должны занести данные
    yesterday_date = (datetime.today().replace(
        hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1))
    print(yesterday_date)

    country_url = 'http://ciad-etl2.rian.off:50080/social_views/'
    driver.get(country_url)
    # ищем табулятор просмотров
    time.sleep(5)

    #  цикл по странам
    for country in COUNTRIES:

        select = Select(driver.find_element_by_id('region-select'))
        select.select_by_value('52')  # Ближнее Зарубежье
        time.sleep(3)

        brand = BRANDS.get(country, None)
        select = Select(driver.find_element_by_id('brand-select'))
        select.select_by_value(brand)
        time.sleep(1)

        # Теперь открылось поле даты ввода, вставляем сюда кусок что раньше был за пределами цикла
        #
        elem_id = driver.find_element_by_id("input-date")
        value = elem_id.get_property('value')
        # print(value)
        input_date = datetime.strptime(value, '%Y-%m-%d')  # .date()
        if (input_date != yesterday_date):
            sys.exit()
        # print(input_date)
        print(country)
        worksheet = sheet.worksheet(country)
        # берём последнюю заполненную строку из колонки дат
        column_values_list = worksheet.col_values(1)
        # всего заполненных значений
        number_of_rows = len(column_values_list)
        #  берём дату
        date_end = worksheet.cell(number_of_rows, 1).value
        print(date_end)
        if (input_date != datetime.strptime(date_end, '%d.%m.%Y')):
            print("Даты данных и ввода не совпадают. Не пишем.")
            continue
        list_of_channels = worksheet.row_values(3)
        number_of_channels = len(list_of_channels)
        list_of_values = worksheet.row_values(number_of_rows)
        for i in range(1, number_of_channels):
            if i < len(list_of_values) and list_of_channels[i] != "":
                #  lll
                input_id = driver.find_element_by_id(list_of_channels[i])
                # time.sleep(1)
                old_value = input_id.get_property('placeholder')
                input_id.click()
                new_value = list_of_values[i]
                if (new_value != ''):
                    if (old_value == "0"):
                        input_id.send_keys(new_value)
                    else:
                        # todo если данные старые неправильные, то их надо заменить
                        if (new_value != old_value):
                            # breakpoint()
                            input_id.send_keys(new_value)
                            print(
                                "Поле уже заполнено: старое значение {} будет перзаписано новым  {} ".format(old_value, new_value))
                        else:
                            print(
                                "Поле уже заполнено: старое {} и новое {} значения совпадают".format(old_value, new_value))
                        
            # конец выгрузки данных из таблицы
        elem_id = driver.find_element_by_id('button-submit')
        #  Пока по кнопке не кликаем или кликаем?
        elem_id.click()

        time.sleep(5)
        try:
            elem_id = driver.find_element_by_id('submit-modal-button')
            elem_id.click()
            time.sleep(1)
            print("Окно подтверждения было закрыто")
        except Exception as ex:
            # print('Exception:', ex)
            pass
    print ("Данные занесены")
    driver.quit()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
