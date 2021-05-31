from ok_api import OkApi
# pip install ok_api
from datetime import datetime, timedelta, date
import time


def main():
    """
        Простой запрос на примере метода friends.get с
        необязательным параметром типа сортировки
        (https://apiok.ru/dev/methods/rest/friends/friends.get)
    """

    ok = OkApi(access_token='tkn1gm9zHPSu4dSQL6pWK97RvjLb8nZJIQ1fs3v5XXLc7Cak2ma4pzy8LgGTdePHPkEPj',
               application_key='CLIHLCKGDIHBABABA',
               application_secret_key='0FE3705B47B45ADB5BDE14D3')

    response = ok.friends.get(sort_type='PRESENT')
    print(response.json())

    response2 = ok.group.getStatOverview(
        gid='53622940434687', period='DAY', fields='ENGAGEMENT')
    print(response2.json())

    # первая дата, с которой всё заносим 01.04.2021
    date_begin = date(2021, 4, 1)
    #  последняя дата, на которую должны занести данные, это вчера
    date_end = (datetime.today().replace(hour=0, minute=0,
                second=0, microsecond=0) - timedelta(days=1)).date()
    # таким образом мы знаем сколько записей должно быть в таблице, как разницу дат в днях

    date_from = date_begin
    date_to = date_from+timedelta(days=1)
    timestamp_from = int(time.mktime(date_from.timetuple()))
    timestamp_to = int(time.mktime(date_to.timetuple())-1)

    response3 = ok.group.getStatTrends(
        gid='53622940434687', start_time=timestamp_from, end_time=timestamp_to, fields='RENDERINGS')
    print(response3.json())

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
