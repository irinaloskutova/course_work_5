import os

from data_base import *
from config import config
from classes import *


def main():
    params = config()
    # print("Добрый день! Давайте искать работодателей и их вакансии.")
    # customers_word = input("Напишите название работодателя, чьи вакансии мы будем искать: ")
    # hh = Employers(customers_word)
    hh = Employers('Камаз')
    print(1)
    data = hh.get_request
    print(2)
    # print(data)
    id_employ = get_list_id_employers(data)
    print(3)
    vac = Vacancy(id_employ)
    # print(vac.get_vacancy)
    print(4)
    data_vac = vac.put_vacancies_in_list
    print(data_vac)
    # print(data_vac)
    # print(vac.get_vacancy)
    # print(id_employ)
    create_database('hh_parser', params)
    print(5)
    save_employers_to_database(data, 'hh_parser', params)
    print(6)
    save_vacancies_to_database(data_vac, 'hh_parser', params)


if __name__ == '__main__':
    main()
