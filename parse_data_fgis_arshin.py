import datetime
import os

import pymongo
import requests
import env
COUNT = 0
TOTAL = 0

NUM = 1

BASE_URL = 'https://fgis.gost.ru/fundmetrology/api/registry/4/data'
TOTAL_LINK = f'{BASE_URL}?pageNumber=1&pageSize=1&orgID=CURRENT_ORG'
LINK = f'{BASE_URL}?pageNumber={NUM}&pageSize=1000&orgID=CURRENT_ORG'
print(os.getenv('MONGO_LOGIN'))
# client = pymongo.MongoClient("mongodb+srv://velllum:<password>@cluster0.fs8kg.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# mongo_url = f"mongodb+srv://velllum:0sxfeDlou9i66twP@cluster0.fs8kg.mongodb.net/?retryWrites=true&w=majority"
mongo_url = f"mongodb+srv://{os.getenv('MONGO_LOGIN')}:{os.getenv('MONGO_PASS')}@cluster0.fs8kg.mongodb.net/{os.getenv('MONGO_DB')}?retryWrites=true&w=majority"
CLIENT = pymongo.MongoClient(mongo_url)





# получаем значение по урлу
def get_url():
    with requests.Session() as s:
        response = s.get(BASE_URL)
        if response.ok:
            return response
        else:
            print('ОШИБКА - 404')


def save_data(lis):
    # client = pymongo.MongoClient('localhost', 27017)

    db = CLIENT.metrolog  # Подключает базу данных, и коллекцию
    db.dataArshin.insert_many(lis)


def get_list_data_url():
    response = get_url().json()
    lis = [item for item in response["result"]["items"]]
    return lis


def main():
    # lis = get_list_data_url()
    # save_data(lis)

    db = CLIENT.metrolog  # Подключает базу данных, и коллекцию

    cursor = db.dataArshin.find({}, {"_id": 0, "values": 0})
    cont = db.dataArshin.count_documents({})

    print(cont)

    # lis = [cur for cur in cursor.pretty()]

    for item in cursor:
        print(item)


if __name__ == '__main__':
    main()
