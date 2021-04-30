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
# credentials = {'LV':'',KZ:''}
# CREDENTIALS = {'LV':None}



def main():

    #  Работа с таблицей

    # Читаем ключи из файла
    CREDENTIALS_FILE = 'sputnik-analitics-python.json'  # Имя файла с закрытым ключом для таблиц, вы должны подставить свое
    credentials_sheets = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials_sheets.authorize(httplib2.Http()) # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

    spreadsheetId = "1DSDFv5uXJkTcDOyuG2Yx_IW_zw4DfTgp9u5dpJzzLZ4"

    # ищем число строк на листе
    for country in COUNTRIES:

        ranges = [country]
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                            ranges = ranges).execute()  
        last_row = len(results['valueRanges'][0].get('values'))
        new_row = last_row + 1

        # смотрим дату в последней строке
        ranges = [country +"!A"+str(last_row)+":B"+str(last_row)] # 
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                            ranges = ranges, 
                                            valueRenderOption = 'FORMATTED_VALUE',  
                                            dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        sheet_values = results['valueRanges'][0]['values'][0][0]
        last_date = datetime.strptime(sheet_values, '%d.%m.%Y') #.datetime()
        yesterday = (datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1))
        if (last_date ==  yesterday ):
            print("Данные за сегодня надо брвть завтра")
            sys.exit()
        next_date = last_date + timedelta(days=1)
        
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
        #  вычисляем границы даты
        epoch = datetime.utcfromtimestamp(0)
        ds = next_date + timedelta(hours=7)
        de = next_date + timedelta(days=1)  + timedelta(hours=7)
        date_start = int((ds  - epoch).total_seconds()) * 1000
        date_end = int((de  - epoch).total_seconds()) * 1000

        # получаем url страны

        channel = YOUTUBE_CHANNELS.get(country,'MINE')
        # channel = 'UCxOgmpeNDyP_C6efcYRdYSQ'  1619679600000
        country_url = 'https://studio.youtube.com/channel/'+ channel +'/analytics/tab-reach_viewers/period-'+ str(date_start)+','+str(date_end)
        driver.get(country_url)
        # ищем табулятор просмотров
        time.sleep(5)
        elem_id = driver.find_element_by_id("VIDEO_THUMBNAIL_IMPRESSIONS-tab") # показы
        # elem_id = driver.find_element_by_id("VIEWS-tab") #просмотры
        elem_id.click()
        time.sleep(3)
        # ищем график и клмикаем в него
        elem_id = driver.find_element_by_xpath('//*[name()="svg"]/*[name()="g"]/*[name()="rect"]')
        elem_id.click()
        time.sleep(3)
        elem_id = driver.find_element_by_xpath('//div[@id="title" and @class="style-scope yta-hovercard"]')
        print(elem_id.text)
        elem_id = driver.find_element_by_xpath('//div[@id="value" and @class="style-scope yta-hovercard"]')
        curr_views = elem_id.text.strip()
        print(curr_views)
        time.sleep(5)

        #  заполняем новую строчку
        new_range = country +"!A"+str(new_row)+":B"+str(new_row)
        curr_date = next_date.date()
        results = service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
            "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
            "data": [
                {"range":  new_range,
                "majorDimension": "ROWS",     # Сначала заполнять строки, затем столбцы
                "values": [
                            [str(curr_date), curr_views] # Заполняем одну строку
                ]}
            ]
        }).execute()
        print ("Данные занесены")
        driver.quit()

    
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

 