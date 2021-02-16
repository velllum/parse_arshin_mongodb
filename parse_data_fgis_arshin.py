import datetime

import pymongo
import requests

COUNT = 0
TOTAL = 0

NUM = 1

BASE_URL = 'https://fgis.gost.ru/fundmetrology/api/registry/4/data'
TOTAL_LINK = f'{BASE_URL}?pageNumber=1&pageSize=1&orgID=CURRENT_ORG'
LINK = f'{BASE_URL}?pageNumber={NUM}&pageSize=1000&orgID=CURRENT_ORG'


# получаем значение по урлу
def get_url():
    with requests.Session() as s:
        response = s.get(BASE_URL)
        if response.ok:
            return response
        else:
            print('ОШИБКА - 404')


def save_data(lis):
    client = pymongo.MongoClient('localhost', 27017)
    db = client.metrolog  # Подключает базу данных, и коллекцию
    db.dataBaseArshin.insert_many(lis)


def get_list_data_url():
    response = get_url().json()
    lis = [item for item in response["result"]["items"]]
    return lis


def main():
    # lis = get_list_data_url()
    # save_data(lis)

    client = pymongo.MongoClient('localhost', 27017)
    db = client.metrolog  # Подключает базу данных, и коллекцию

    # db.dataBaseArshin.insert_many(lis)

    cursor = db.dataBaseArshin.find({})
    cont = db.dataBaseArshin.count_documents({})

    print(cont)

    # lis = [cur for cur in cursor.pretty()]

    for item in cursor:
        print(item)


if __name__ == '__main__':
    main()
