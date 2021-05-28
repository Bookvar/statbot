from selenium import webdriver # pip install selenium
from selenium.webdriver.support.ui import Select
import pyautogui # pip install pyautogui
import os, time, sys
from datetime import datetime, timedelta
# Подключаем библиотеки для работы с таблицами
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	


COUNTRIES = ['BN', 'AB','AM','GE','KZ','LV']
BRANDS = {
    'BN':'Baltnews',
    'AB':'Sputnik Abkhazia',
    'AM':'Sputnik Armenia',
    'AZ':'Sputnik Azerbaijan',
    'GE':'Sputnik Georgia',
    'KZ':'Sputnik Kazakhstan',
    'KG':'Sputnik Kyrgyzstan',
    'LV':'Sputnik Latvia',
    'LT':'Sputnik Lithuania',
    'ML':'Sputnik Moldova',
    'OS':'Sputnik Ossetia',
    'TJ':'Sputnik Tajikistan',
    'UZ':'Sputnik Uzbekistan',
    'SBZ':'Sputnik Ближнее зарубежье',
    'SRU':'Sputnik на русском',
    'UA':'Ukraina.ru'
    }

def main():
    
    #  Подготавливаем webdriver
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])        
    chrome_options.add_argument('--user-data-dir=C:/Users/mitkevich/AppData/Local/Google/Chrome/User Data') #Tester
    # chrome_options.add_argument('--profile-directory=Profile 1')
    executable_path = os.path.dirname(os.path.abspath(__file__)) + '\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=executable_path, options=chrome_options)

    #  Готовим таблицу
    # Читаем ключи из файла
    CREDENTIALS_FILE = 'sputnik-analitics-python.json'  # Имя файла с закрытым ключом для таблиц, вы должны подставить свое
    credentials_sheets = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials_sheets.authorize(httplib2.Http()) # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 

    spreadsheetId = "1DSDFv5uXJkTcDOyuG2Yx_IW_zw4DfTgp9u5dpJzzLZ4"

    #  дата, на которую должны занести данные
    yesterday_date = (datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1))
    print(yesterday_date)


    country_url = 'http://ciad-etl2.rian.off:50080/social_views/'
    driver.get(country_url)
    # ищем табулятор просмотров
    time.sleep(5)

    select = Select(driver.find_element_by_id('region-select'))
    select.select_by_value('52') # Ближнее Зарубежье
    time.sleep(1)

    # elem_id.click()
    time.sleep(3)
    #  цикл по странам
    for country in COUNTRIES:
        brand = BRANDS.get(country, None)
        select = Select(driver.find_element_by_id('brand-select'))
        select.select_by_value(brand)
        time.sleep(1)

        # Теперь открылось поле даты ввода, вставляем сюда кусок что раньше был за пределами цикла
        #  
        elem_id = driver.find_element_by_id("input-date")
        value = elem_id.get_property('value')
        print(value)
        input_date = datetime.strptime(value, '%Y-%m-%d') #.date()
        if (input_date == yesterday_date):
            print('Дата на сайте корректна')
        else:
            print('Дата на сайте некорректна')
            sys.exit()
        print(input_date)
        # 

        # цикл по площадкам страны (берём из гуглтаблицы, третья строка листа должна содержать channels-XXX)
                # ищем число строк на листе страны
        # col_channel = COLUMNS_CHANNELS.get(country, None)
        ranges = [country]
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                            ranges = ranges).execute()  
        last_row = len(results['valueRanges'][0].get('values')) # последняя строка таблицы

        ranges = [country +"!3:3"] 
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                            ranges = ranges, 
                                            valueRenderOption = 'FORMATTED_VALUE',  
                                            dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        channels_row = results['valueRanges'][0]['values'][0]  # третья строка таблицы, содержащая наименования каналов                                           

        # смотрим данные в последней строке last_row
        ranges = [country +"!"+str(last_row)+":"+str(last_row)]  
        results = service.spreadsheets().values().batchGet(spreadsheetId = spreadsheetId, 
                                            ranges = ranges, 
                                            valueRenderOption = 'FORMATTED_VALUE',  
                                            dateTimeRenderOption = 'FORMATTED_STRING').execute() 
        values_row = results['valueRanges'][0]['values'][0]                                            
        row_date =datetime.strptime(values_row[0], '%d.%m.%Y')
        if (row_date == input_date):
            vsego_channels = len(channels_row)
            vsego_values = len(values_row)

            for i in range(1,vsego_channels):
                # print(channels_row[i])
            
                # print(values_row[i])
                if ( i < vsego_values):
                    input_id = driver.find_element_by_id(channels_row[i])
                    time.sleep(1)
                    value = input_id.get_property('placeholder')
                    # value = input_id.get_attribute('placeholder')
                    input_id.click()
                    if ( value== "0"):
                        # print("Поле готово для редактирования")
                        if (values_row[i] != ''):
                            input_id.send_keys(values_row[i])
                    else:
                        # print("Поле уже заполнено")
                        # print(value)
                        pass
                    time.sleep(1)
            # конец выгрузки данных из таблицы

            elem_id = driver.find_element_by_id('button-submit')
            #  Пока по кнопке не кликаем или кликаем?
            elem_id.click()
            time.sleep(5)


    # print ("Данные занесены")
    driver.quit()

    
if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

 