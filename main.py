from utils import *


def main():
    params = config()
    db = DBCreate('hh_database', params)
    db.create_database()
    print("Добрый день! Давайте искать работодателей и их вакансии.")
    print("Придумайте 10 уникальных компаний, по названиям которых мы будем осуществлять поиск.")
    user_interaction('hh_database')
    while True:
        db_manager = DBManager('hh_database', params)
        emp_and_count = db_manager.get_companies_and_vacancies_count()
        print('\nНажмите 1, чтобы просмотреть сколько вакансий в компании.')
        print('Нажмите 2, чтобы узнать среднюю зарплату.')
        print('Нажмите 3, чтобы узнать вакансии, зарплата по которым выше средней из найденных.')
        print('Нажмите 4, чтобы посмотреть все вакансии по ключевому слову.')
        print('Нажмите 5, чтобы закончить работу программы.')
        user_number = input()
        if user_number == 1 or user_number == '1':
            print(f"Cписок всех компаний и количество вакансий у каждой компании: \n{emp_and_count}")
        elif user_number == 2 or user_number == '2':
            print(f"Средняя зарплата среди всех найденных: {db_manager.get_avg_salary()}")
        elif user_number == 3 or user_number == '3':
            print(f'Это вакансии, зарплата по которым выше средней из найденных: \n{db_manager.get_vacancies_with_higher_salary()}')
        elif user_number == 4 or user_number == '4':
            word_key = input('Введите ключевое слово:  ')
            print(f'Эти вакансии найдены по Вашему ключевому слову: \n{db_manager.get_vacancies_with_keyword(word_key)}')
        elif user_number == 5 or user_number == '5':
            exit('До свидания!')
        else:
            print("Такого варианта нет, попробуйте еще раз")
            print('Показать еще меню? ДА/НЕТ')
            choice = input().upper()
            if choice == 'ДА':
                continue
            else:
                print('Программа завершает работу')
                break


if __name__ == '__main__':
    main()
