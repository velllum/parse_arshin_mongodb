import os

import requests
from pymongo import MongoClient


class ParseArshin:
    _PAGE_NUMBER = 1
    _PAGE_SIZE = 1000

    _MONGO_CONNECTION = f"mongodb+srv://{os.environ.get('MONGO_LOGIN')}:{os.environ.get('MONGO_PASS')}@cluster0.fs8kg.mongodb" \
                       f".net/{os.environ.get('MONGO_DB')}?retryWrites=true&w=majority "

    def __init__(self):
        self._client = MongoClient(ParseArshin._MONGO_CONNECTION)
        self._db = self._client.metrolog
        self._response = None
        self._headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"
        }

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
            response = session.get(url=os.environ.get("URL"))
            if response.ok:
                self._response = response
            else:
                print('ОШИБКА - 404')

    def _seve_data(self):
        """
        - Сохраняет собранные данные в удаленную базу mongodb

        :return: None
        """

        self.list_data = self._response.json()["result"]["items"]

        while True:
            try:
                if not self.list_data:
                    break
                self._db.dataArshin.insert_many(self.list_data)
            except Exception as e:
                print(f"Произошла ошибка {e}")

    def remove_data(self):
        """
        - Отчистить базу от всех данных

        :return: None
        """

        self._db.dataArshin.count_documents({})
        self._db.dataArshin.remove()
        self._db.dataArshin.count()

    def coll_data(self):
        """
        - Метод старта программ

        :return: None
        """
        # self._get_respose()
        # self._seve_data()
        #
        # ParseArshin._PAGE_NUMBER += 1

        print(self._db.dataArshin.find({}))

        for i in self._db.dataArshin.find({}):
            print(i)




if __name__ == '__main__':
    parse = ParseArshin()
    # parse.remove_data()
    parse.coll_data()
