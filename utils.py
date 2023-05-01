from data_base import *
from config import config
from classes_HH import *


def user_interaction(hh_database):
    params = config()
    db = DBCreate(hh_database, params)
    db.create_database()
    i = 1
    list_emp = []
    while i <= 10:
        customers_word = input("Напишите название работодателя, чьи вакансии мы будем искать: ")
        list_emp.append(customers_word)
        hh = Employers(customers_word)
        data = hh.get_request
        for number in range(len(data)):
            id_emp = data[number]["id"]
            vac = Vacancy(id_emp)
            vacancy_list = vac.put_vacancies_in_list()
            db.save_employers_to_database(data)
            db.save_vacancies_to_database(vacancy_list)
        i += 1
