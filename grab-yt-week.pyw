#  В прошлом варианте не учитывался факт того, что ютуб придерживает выбор даты, пока данные за неё  не подготовлены окончательно, 
# а у нас был прямой забор данных, на время запроса, а это всё-таки не итоговые данные. 
# меняем алгоритм, но забирать сможем за последние 7 доступных дней

from selenium import webdriver # pip install selenium
import pyautogui # pip install pyautogui
import os, time, sys
from datetime import datetime, timedelta
# Подключаем библиотеки для работы с таблицами
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	

COUNTRIES = ['LV']
YOUTUBE_CHANNELS = {'LV':'UCxOgmpeNDyP_C6efcYRdYSQ',
                    'KZ':'UCN6bgSC5mdl8J7y7S9N2qSQ',
                    'BN':'UCwDdQgITt3pgdc_j3O764Hg'}

COLUMNS_CHANNELS =  {'LV':'F'}     

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
}

def int_value_from_ru_month(date_str):
    for k, v in RU_MONTH_VALUES.items():
        date_str = date_str.replace(k, str(v))
    return date_str


def shits_column_name_to_number(column_name):
    column_name = column_name.upper()
    sum = 0
    for i in column_name:
        sum = sum * 26
        sum = sum + (ord(i) - ord('A') )
    return sum
    

def main():
    #  Работа с таблицей
    # Читаем ключи из файла
    CREDENTIALS_FILE = 'sputnik-analitics-python.json'  # Имя файла с закрытым ключом для таблиц, вы должны подставить свое
    credentials_sheets = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials_sheets.authorize(httplib2.Http()) # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

    spreadsheetId = "1DSDFv5uXJkTcDOyuG2Yx_IW_zw4DfTgp9u5dpJzzLZ4"

    # цикл по странам
    for country in COUNTRIES:
        # ищем число строк на листе страны
        col_channel = COLUMNS_CHANNELS.get(country, None)
        ranges = [country]
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                            ranges = ranges).execute()  
        last_row = len(results['valueRanges'][0].get('values'))
        new_row = last_row + 1

        # смотрим дату в последней строке
        ranges = [country +"!A"+str(last_row)+":"+col_channel+str(last_row)] # 
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                            ranges = ranges, 
                                            valueRenderOption = 'FORMATTED_VALUE',  
                                            dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        res_row = results['valueRanges'][0]['values'][0]                                            
        date_values = res_row[0]
        num_col = shits_column_name_to_number(col_channel)
        if (num_col > len(res_row) ):
            view_values = 0
        else:
            view_values = res_row[num_col]       
        #  Последняя дата в таблице
        last_date = datetime.strptime(date_values, '%d.%m.%Y') #.datetime() 
        #  Вычисляем дату вчерашнего дня
        yesterday = (datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1))
        #  Вычисляем дату позавчерашнего  дня
        before_yesterday = yesterday - timedelta(days=1)
        
        # rangesV = [country +"!"+col_channel+str(last_row)+":"+col_channel+str(last_row)] # 
        # request = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, 
        #                                     range=rangesV, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
        # response = request.execute()

        #  Если дата за вчера есть, то надо проверить есть ли там значение показов.
        
        next_date = last_date + timedelta(days=1)
        # новые данные за сегодняшний день брать рано, выходим из скрипта
        if (last_date ==  yesterday ):
            print("Вчерашняя дата в таблице есть. Проверим заполнение.")
            if (int(view_values) > 0):
                print("Число показов {}".format(view_values))
                sys.exit()
            else:
                print("Значений нет. Надо заполнить")
                next_date = last_date + timedelta(days=0)
        
        #  Подготавливаем граббер
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])        
        chrome_options.add_argument('--user-data-dir=C:/Users/mitkevich/AppData/Local/Google/Chrome/User Data') #Tester
        # chrome_options.add_argument('--profile-directory=Profile 1')
        executable_path = os.path.dirname(os.path.abspath(__file__)) + '\chromedriver.exe'
        driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)

        # Если последняя дата в таблице ранее чем позавчера, используем метод выборки конкретного дня, 
        # иначе (то есть за вчера)  используем метод последнего дня последней недели.

        channel = YOUTUBE_CHANNELS.get(country,'MINE')

        if (last_date ==  before_yesterday ):
            #  итак просто берём данные последней доступной недели
            country_url = 'https://studio.youtube.com/channel/'+ channel +'/analytics/tab-reach_viewers/period-week'
        else:
            #  вычисляем границы даты для запроса
            epoch = datetime.utcfromtimestamp(0)
            ds = next_date + timedelta(hours=7)
            de = next_date + timedelta(days=1)  + timedelta(hours=7)
            date_start = int((ds  - epoch).total_seconds()) * 1000
            date_end = int((de  - epoch).total_seconds()) * 1000

            country_url = 'https://studio.youtube.com/channel/'+ channel +'/analytics/tab-reach_viewers/period-'+ str(date_start)+','+str(date_end)

        driver.get(country_url)
        # ищем табулятор показов
        time.sleep(5)
        elem_id = driver.find_element_by_id("VIDEO_THUMBNAIL_IMPRESSIONS-tab") # показы
        # elem_id = driver.find_element_by_id("VIEWS-tab") #просмотры
        elem_id.click()
        time.sleep(3)
        #  если смотрим график на неделю, то смотрим за какой период доступны данные.
        # elem_id = driver.find_element_by_xpath('//div[@id="yta-time-picker" and @class="label-text style-scope ytcp-dropdown-trigger"]')
        
        if (last_date ==  before_yesterday ):
            elem_id = driver.find_element_by_xpath('//div[@class="label-text style-scope ytcp-dropdown-trigger"]')
            curr_period = elem_id.text.strip()
            print(curr_period)
        
        # ищем график и клмикаем в него. при этом почему-то всплывает окошко показаний на последнюю дату, что нам и надо

        # elem_id = driver.find_element_by_xpath('//*[name()="svg"]/*[name()="g"]/*[name()="rect"]')
        elem_id = driver.find_element_by_xpath('//div[@ id="aspect-ratio-four-one-container"]')
        time.sleep(1)
        elem_id.click()
        time.sleep(3)

        elem_id = driver.find_element_by_xpath('//div[@id="title" and @class="style-scope yta-hovercard"]')
        #  забираем дату в формате по примеру "Пн, 10 мая 2021 г."
        print(elem_id.text)
        #  преобразуем в нужный вид
        curr_end_date_text = int_value_from_ru_month(elem_id.text[4:][:-3])
        print(curr_end_date_text)
        curr_end_date = datetime.strptime(curr_end_date_text, '%d %m %Y')
        print(curr_end_date)
        elem_id = driver.find_element_by_xpath('//div[@id="value" and @class="style-scope yta-hovercard"]')
        curr_views = elem_id.text.strip()
        print(curr_views)
        time.sleep(5)


        #  заполняем значения
         
        if (last_date ==  yesterday ): #  если дата уже была
            new_range = country +"!A"+str(last_row)+":A"+col_channel+str(last_row)
        else: 
            new_range = country +"!A"+str(new_row)+":A"+col_channel+str(new_row)

        curr_date = next_date.date()

        results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
            "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {"range":  new_range,
                "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                "values": [
                            [str(curr_date)] # Заполняем одну строку
                ]}
            ]
        }).execute()

        # вставляем показы
        if (last_date ==  yesterday ): #  если дата уже была
            new_range = country +"!"+col_channel+str(last_row)+":"+col_channel+str(last_row)
        else:        
            new_range = country +"!"+col_channel+str(new_row)+":"+col_channel+str(new_row)

        curr_date = next_date.date()
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
            "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {"range":  new_range,
                "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                "values": [
                            [curr_views] # Заполняем одну строку
                ]}
            ]
        }).execute()

        print ("Данные занесены")
        driver.quit()

    
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

 