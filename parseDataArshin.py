import env
import os

import requests
from pymongo import MongoClient


class ParseArshin:

    _PAGE_NUMBER = 1
    _PAGE_SIZE = 1000
    _MONGO_CONNECTION = f"mongodb+srv://{os.getenv('MONGO_LOGIN')}:{os.getenv('MONGO_PASS')}@cluster0.fs8kg.mongodb" \
                       f".net/{os.getenv('MONGO_DB')}?retryWrites=true&w=majority"

    def __init__(self):
        self._client = MongoClient(ParseArshin._MONGO_CONNECTION)
        self.db = self._client.metrolog
        self._response = None
        self.list_items = None
        self._headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
        }

    @property
    def page_number(self):
        """
        - Вернет количество пройденных страниц

        :return:
        """
        return ParseArshin._PAGE_NUMBER

    def _get_respose(self):
        """
        - Получить ответ запросы по ссылке

        :return: None
        """
        with requests.Session() as session:
            session.headers = self._headers
            session.params = {
                "pageNumber": ParseArshin._PAGE_NUMBER,
                "pageSize": ParseArshin._PAGE_SIZE,
                "orgID": "CURRENT_ORG",
            }
            response = session.get(url=os.getenv("URL"))
            if response.ok:
                self._response = response
            else:
                print('ОШИБКА - 404')

    def _seve_data(self):
        """
        - Сохраняет собранные данные в удаленную базу mongodb

        :return: None
        """
        try:
            self.db.dataArshin.insert_many(self.list_items["result"]["items"])
        except Exception as e:
            print(f"Произошла ошибка {e}")

    def remove_data(self):
        """
        - Отчистить базу от всех данных

        :return: None
        """
        self.db.dataArshin.delete_many({})

    def get_all_flelds(self):
        """
        - Вывод данных

        :return:
        """
        return self.db.dataArshin.find({}, {"_id": 0})

    def get_count_fields(self):
        """
        - Получить количество всех записей в базе

        :return:
        """
        return self.db.dataArshin.count_documents({})

    def coll_data(self):
        """
        - Метод старта программ

        :return: None
        """
        self._get_respose()
        self.list_items = self._response.json()

        if not self.list_items["result"]["items"]:
            print("Массив пуст")
            return False

        self._seve_data()

        ParseArshin._PAGE_NUMBER += 1


if __name__ == '__main__':
    parse = ParseArshin()

    # parse.remove_data()
    # while True:
    #     print(f"{parse.page_number} | {parse.page_number*1000}")
    #     if parse.coll_data() is False:
    #         break

    # for en, dic in enumerate(parse.get_all_flelds(), 1):
    #     # print(en, dic["properties"][1]["value"])
    #     print(en, dic["properties"][1]["value"])

    for i in parse.db.dataArshin.find({"properties.4.value": "37049-08"}):
        print(i)
