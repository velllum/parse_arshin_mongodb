import env
import os

import requests
from pymongo import MongoClient


class ParseArshin:

    _PAGE_NUMBER = 1
    _PAGE_SIZE = 1000
    # _MONGO_CONNECTION = f"mongodb+srv://{os.getenv('MONGO_LOGIN')}:{os.getenv('MONGO_PASS')}@cluster0.fs8kg.mongodb.net/{os.getenv('MONGO_DB')}?retryWrites=true&w=majority"
    _MONGO_CONNECTION = ('localhost', 27017)

    print(_MONGO_CONNECTION)

    def __init__(self):
        self._client = MongoClient(*ParseArshin._MONGO_CONNECTION)
        self.db = self._client.metrolog[os.getenv("MONGO_COLL")]
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



    def _save_data(self):
        """
        - Сохраняет собранные данные в удаленную базу mongodb

        :return: None
        """
        try:
            self.db.insert_many(self.list_items["result"]["items"])
        except Exception as e:
            print(f"Произошла ошибка {e}")



    def remove_data(self):
        """
        - Отчистить базу от всех данных

        :return: None
        """
        self.db.delete_many({})



    def run(self):
        """
        - Метод старта программ

        :return: None
        """
        while True:
            self._get_respose()
            self.list_items = self._response.json()

            if not self.list_items["result"]["items"]:
                print(f"Загрузка закончена, собранное количество {self.db.count_documents({})}")
                break

            self._save_data()
            ParseArshin._PAGE_NUMBER += 1


    def __str__(self):
        return print(f"{self.list_items} | {self.list_items*1000}")


if __name__ == '__main__':
    parse = ParseArshin()
    # parse.remove_data()
    # parse.run()

    for e, field in enumerate(parse.db.find({"properties.value": "37049-08"}, {"_id": 0}), 1):
        # print(e, field["properties"][1]["value"],   field["properties"][10]["value"][0], field["properties"][4]["value"])
        print(e, )
