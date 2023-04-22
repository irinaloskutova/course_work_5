import json
import time
from abc import ABC, abstractmethod
import os
import requests


class Employers:
    """Возвращает работодателей с сайта HeadHunter по ключевому слову"""
    def __init__(self, data: str):
        """Инициализирует класс где data - название по которому будет происходить поиск"""
        self.data = data

    @property
    def get_request(self):
        """Возвращает работодателей с сайта HeadHunter"""
        try:
            employers = []
            params = {
                    "text": f"{self.data}",
                    "area": 113,
                    "only_with_vacancies": True,
                    # "page": page,
                    # "per_page": 20,
                }
            employers.extend(requests.get('https://api.hh.ru/employers', params=params).json()["items"])
            return employers
        except requests.exceptions.ConnectTimeout:
            print('Oops. Connection timeout occured!')
        except requests.exceptions.ReadTimeout:
            print('Oops. Read timeout occured')
        except requests.exceptions.ConnectionError:
            print('Seems like dns lookup failed..')
        except requests.exceptions.HTTPError as err:
            print('Oops. HTTP Error occured')
            print('Response is: {content}'.format(content=err.response.content))


    # @property
    # def put_employers_in_list(self):
    #     with open('employers.json', 'r') as f:
    #         get_employers = json.load(f)
    #         list_employers = []
    #         for i in range(len(get_employers)):
    #             # if self.get_vacancy[i]['snippet']['requirement'] is not None:
    #             #     s = self.get_vacancy[i]['snippet']['requirement']
    #             #     for x, y in ("<highlighttext>", ""), ("</highlighttext>", ""):
    #             #         s = s.replace(x, y)
    #             info = {
    #                 "id_employer": get_employers[i]['id'],
    #                 'name_employer': get_employers[i]['name'],
    #                 "open_vacancies": get_employers[i]['open_vacancies'],
    #                 'url_employer': get_employers[i]['alternate_url'],
    #             }
    #             list_employers.append(info)
    #         return list_employers
    #
    # def to_json(self):
    #     with open('hhemp.json', 'w', encoding='UTF-8') as f:
    #         json.dump(self.put_employers_in_list, f, indent=2)


class Vacancy:
    def __init__(self, id_employer):
        self.id_employer = id_employer
        self.get_vacancy = self.get_vacancy()
        self.put_vacancies_in_list = self.put_vacancies_in_list()
    # @property
    def get_vacancy(self):
        try:
            vacancy = []
            # for page in range(1, 11):
            params = {"employer_id": f"{self.id_employer}",}
            vacancy.extend(requests.get('https://api.hh.ru/vacancies?', params=params).json()['items'])
            time.sleep(0.22)
            return vacancy
        except requests.exceptions.ConnectTimeout:
            print('Oops. Connection timeout occured!')
        except requests.exceptions.ReadTimeout:
            print('Oops. Read timeout occured')
        except requests.exceptions.ConnectionError:
            print('Seems like dns lookup failed..')
        except requests.exceptions.HTTPError as err:
            print('Oops. HTTP Error occured')
            print('Response is: {content}'.format(content=err.response.content))


    def put_vacancies_in_list(self):
        list_vacancy = []
        for i in range(len(self.get_vacancy)):
            info = {
                'id_vacancy': self.get_vacancy[i].get('id'),
                'name_vacancy': self.get_vacancy[i].get('name'),
                'id_employer': 0 if self.get_vacancy[i]['employer']['id'] == None else self.get_vacancy[i]['employer']['id'],
                'name_employer': "Не указано" if self.get_vacancy[i]['employer']['name'] == None else self.get_vacancy[i]['employer']['name'],
                'city': "Не указано" if self.get_vacancy[i]['area']['name'] == None else self.get_vacancy[i]['area']['name'],
                'salary': "Не указано" if (self.get_vacancy[i]['salary'] == None or self.get_vacancy[i]['salary']['from'] == 0 or
                                               self.get_vacancy[i]['salary']['from'] == None) else self.get_vacancy[i]['salary']['from'],
                'experience': self.get_vacancy[i]['experience'].get('name'),
                'url': self.get_vacancy[i].get('alternate_url'),
                "requirement": "Не указано" if self.get_vacancy[i]['snippet']['requirement'] else self.get_vacancy[i]['snippet']['requirement'],
            }
            list_vacancy.append(info)
        return list_vacancy

    def to_json(self):
        with open('vacancy.json', 'w') as f:
            json.dump(self.put_vacancies_in_list, f, indent=2)


