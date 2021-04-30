
# -*- coding: utf-8 -*-

# pip install --upgrade google-api-python-client
# pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2

import os
from datetime import datetime, timedelta
import pickle
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
# 
# Подключаем библиотеки для работы с таблицами
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	


# Google's Request
from google.auth.transport.requests import Request


# SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'client_secret.json'

START_DATE = '2021-04-01'
END_DATE = '2021-12-31'

# COUNTRIES = ["LV","KZ"]
COUNTRIES = ['LV']
YOUTUBE_CHANNELS = {'LV':'UCxOgmpeNDyP_C6efcYRdYSQ',
                    'KZ':'UCN6bgSC5mdl8J7y7S9N2qSQ',
                    'BN':'UCwDdQgITt3pgdc_j3O764Hg'}
# credentials = {'LV':'',KZ:''}
# CREDENTIALS = {'LV':None}

for country in COUNTRIES:
    credentials = None
    # token.pickle stores the user's credentials from previously successful logins
    token_pickle = 'token' + country + '.pickle'
    if os.path.exists(token_pickle):
        print('Loading Credentials From File...')
        with open(token_pickle, 'rb') as token:
            credentials = pickle.load(token)

    def get_service():
        global credentials
        # If there are no valid credentials available, then either refresh the token or log in.
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                print('Refreshing Access Token...')
                credentials.refresh(Request())
            else:
                print('Fetching New Tokens...')
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                flow.run_local_server(port=8080, prompt="consent")
                credentials = flow.credentials
                # Save the credentials for the next run
                with open(token_pickle, 'wb') as f:
                    print('Saving Credentials for Future Use...')
                    pickle.dump(credentials, f)
                print(credentials.to_json())
        return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

    def execute_api_request(client_library_function, **kwargs):
        response = client_library_function(
        **kwargs
        ).execute()
        print(response)
        return response 

    if __name__ == '__main__':
        youtubeAnalytics = get_service()
        '''
        print('channel==MINE')
        execute_api_request(
            youtubeAnalytics.reports().query,
            ids='channel==MINE',
            startDate='2021-04-01',
            endDate='2021-04-30',
            metrics='estimatedMinutesWatched,views,likes,subscribersGained',
            dimensions='day',
            sort='day'
        )
        '''
        print('channel==' + country)
        views=execute_api_request(
            youtubeAnalytics.reports().query,
            ids='channel=='+YOUTUBE_CHANNELS.get(country,'MINE') ,
            startDate='2021-04-01',
            endDate='2021-12-31',
            metrics='estimatedMinutesWatched,views,likes,subscribersGained',
            dimensions='day',
            sort='day'
        )

        #  Работа с таблицей

        # Читаем ключи из файла
        CREDENTIALS_FILE = 'sputnik-analitics-python.json'  # Имя файла с закрытым ключом для таблиц, вы должны подставить свое
        credentials_sheets = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials_sheets.authorize(httplib2.Http()) # Авторизуемся в системе
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 
        '''
        spreadsheet = service.spreadsheets().create(body = {
            'properties': {'title': 'Первый тестовый документ', 'locale': 'ru_RU'},
            'sheets': [{'properties': {'sheetType': 'GRID',
                                        'sheetId': 0,
                                        'title': 'Лист номер один',
                                        'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
        }).execute()
        spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
        print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

        driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
        access = driveService.permissions().create(
            fileId = spreadsheetId,
            body = {'type': 'user', 'role': 'writer', 'emailAddress': 'vbnrtdbx@gmail.com'},  # Открываем доступ на редактирование
            fields = 'id'
        ).execute()
        '''

        #  https://docs.google.com/spreadsheets/d/1DSDFv5uXJkTcDOyuG2Yx_IW_zw4DfTgp9u5dpJzzLZ4

        spreadsheetId = "1DSDFv5uXJkTcDOyuG2Yx_IW_zw4DfTgp9u5dpJzzLZ4"

        '''
        driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
        access = driveService.permissions().create(
            fileId = spreadsheetId,
            body = {'type': 'user', 'role': 'writer', 'emailAddress': 'vbnrtdbx@gmail.com'},  # Открываем доступ на редактирование
            fields = 'id'
        ).execute()

        access = driveService.permissions().create(
            fileId = spreadsheetId,
            body = {'type': 'user', 'role': 'writer', 'emailAddress': 'service-account@sputnik-analitics-python.iam.gserviceaccount.com'},  # Открываем доступ на редактирование
            fields = 'id'
        ).execute()


        '''

        '''
        # Добавление листа
        results = service.spreadsheets().batchUpdate(
            spreadsheetId = spreadsheetId,
            body = 
        {
            "requests": [
            {
                "addSheet": {
                "properties": {
                    "title": "Еще один лист",
                    "gridProperties": {
                    "rowCount": 20,
                    "columnCount": 12
                    }
                }
                }
            }
            ]
        }).execute()
        '''
        '''
        # Получаем список листов, их Id и название
        spreadsheet = service.spreadsheets().get(spreadsheetId = spreadsheetId).execute()
        sheetList = spreadsheet.get('sheets')
        for sheet in sheetList:
            sheetId = sheet['properties']['sheetId']
            title = sheet['properties']['title']
            print(sheet['properties']['sheetId'], sheet['properties']['title'])
            if (title == "LV"):
                sheetId_LV = sheetId # Латвия  

        # sheetId = sheetList[0]['properties']['sheetId']
        # 
        print('Мы будем использовать лист с Id = ', sheetId_LV)
        '''

        

        # ищем число строк на листе
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
        last_date = datetime.strptime(sheet_values, '%d.%m.%Y').date()
        # print(date)
        next_date = last_date + timedelta(days=1)
        # print(next_date)
        for row in views.get('rows'):
            curr_date =  datetime.strptime(row[0], '%Y-%m-%d').date()
            curr_views = row[2]
            if (curr_date > last_date):
                print('На {} {} просмотров'.format(curr_date, curr_views)  )


                #  заполняем новую строчку
                new_range = country +"!A"+str(new_row)+":B"+str(new_row)
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
                new_row = new_row + 1


