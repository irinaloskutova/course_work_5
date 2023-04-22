import json
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
            for page in range(1, 11):
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


    @property
    def put_employers_in_list(self):
        with open('employers.json', 'r') as f:
            get_employers = json.load(f)
            list_employers = []
            for i in range(len(get_employers)):
                # if self.get_vacancy[i]['snippet']['requirement'] is not None:
                #     s = self.get_vacancy[i]['snippet']['requirement']
                #     for x, y in ("<highlighttext>", ""), ("</highlighttext>", ""):
                #         s = s.replace(x, y)
                info = {
                    "id_employer": get_employers[i]['id'],
                    'name_employer': get_employers[i]['name'],
                    "open_vacancies": get_employers[i]['open_vacancies'],
                    'url_employer': get_employers[i]['alternate_url'],
                }
                list_employers.append(info)
            return list_employers

    def to_json(self):
        with open('hhemp.json', 'w', encoding='UTF-8') as f:
            json.dump(self.put_employers_in_list, f, indent=2)


class Vacancy:
    def __init__(self, id_employer):
        self.id_employer = id_employer

    @property
    def get_vacancy(self):
        try:
            vacancy = []
            for page in range(1, 11):
                params = {
                    "employer_id": f"{self.id_employer}",
                }
                vacancy.extend(requests.get('https://api.hh.ru/vacancies?', params=params).json())
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


    @property
    def put_vacancies_in_list(self):
        with open('vacancy_1.json', 'r') as f:
            get_vacancy = json.load(f)
            list_vacancy = []
            for i in range(len(get_vacancy)):
                # if self.get_vacancy[i]['snippet']['requirement'] is not None:
                #     s = self.get_vacancy[i]['snippet']['requirement']
                #     for x, y in ("<highlighttext>", ""), ("</highlighttext>", ""):
                #         s = s.replace(x, y)
                info = {
                    'id_vacancy': get_vacancy[i]['id'],
                    'name_vacancy': get_vacancy[i]['name'],
                    'id_employer': get_vacancy[i]['employer']['id'],
                    'name_employer': get_vacancy[i]['employer']['name'],
                    'city': get_vacancy[i]['area']['name'],
                    'salary': "Не указано" if (get_vacancy[i]['salary'] == None or get_vacancy[i]['salary']['from'] == 0 or
                                       get_vacancy[i]['salary']['from'] == None) else get_vacancy[i]['salary']['from'],
                    'experience': get_vacancy[i]['experience']['name'],
                    "requirement": get_vacancy[i]['snippet']['requirement'],
                    'url': get_vacancy[i]['alternate_url'],
                }
                list_vacancy.append(info)
            return list_vacancy
        # list_vacancy = []
        # for i in range(len(self.get_vacancy)):
        #     # if self.get_vacancy[i]['snippet']['requirement'] is not None:
        #     #     s = self.get_vacancy[i]['snippet']['requirement']
        #     #     for x, y in ("<highlighttext>", ""), ("</highlighttext>", ""):
        #     #         s = s.replace(x, y)
        #     info = {
        #         'id_vacancy': self.get_vacancy[i]['id'],
        #         'name_vacancy': self.get_vacancy[i]['name'],
        #         'id_employer': self.get_vacancy[i]['employer']['id'],
        #         'name_employer': self.get_vacancy[i]['employer']['name'],
        #         'city': self.get_vacancy[i]['area']['name'],
        #         'salary': "Не указано" if (self.get_vacancy[i]['salary'] == None or self.get_vacancy[i]['salary']['from'] == 0 or
        #                                        self.get_vacancy[i]['salary']['from'] == None) else self.get_vacancy[i]['salary']['from'],
        #         'experience': self.get_vacancy[i]['experience']['name'],
        #         'currency': self.get_vacancy[i]['salary'],
        #         'url': self.get_vacancy[i]['alternate_url'],
        #         "requirement": self.get_vacancy[i]['snippet']['requirement'],
        #     }
        #     list_vacancy.append(info)
        # return list_vacancy

    def to_json(self):
        with open('vacancy.json', 'w') as f:
            json.dump(self.put_vacancies_in_list, f, indent=2)


if __name__ == '__main__':
    hh=Employers('Сбербанк')
    print(hh.put_employers_in_list)
    hh.to_json()
    # vacancies = Vacancy(2543027)
    # print(vacancies.get_vacancy)
    # print(vacancies.put_vacancies_in_list)
    # vacancies.to_json()
    # vac = Vacancy('Сбербанк')
    # vac.to_json()
