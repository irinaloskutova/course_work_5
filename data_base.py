import psycopg2
from typing import Any


class DBCreate:
    """Создает и заполняет базы данных"""
    def __init__(self, database_name: str, params: dict) -> None:
        self.database_name = database_name
        self.params = params

    def create_database(self):
        """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях."""
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    id_employer INT PRIMARY KEY,
                    name_employer VARCHAR(255) NOT NULL,
                    open_vacancies VARCHAR,
                    url_employer TEXT
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    id_vacancy INT PRIMARY KEY,
                    name_vacancy VARCHAR(255) NOT NULL,
                    id_employer INT REFERENCES employers(id_employer),
                    name_employer VARCHAR NOT NULL,
                    salary_from INT,
                    salary_to INT,
                    salary_avg INT,
                    city VARCHAR(255),
                    experience TEXT,
                    requirement TEXT,
                    url TEXT
                )
            """)

        conn.commit()
        conn.close()

    def save_employers_to_database(self, data: list[dict[str, Any]]):
        """Сохранение данных о работодателях в базу данных."""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            for employer in data:
                cur.execute(
                    """
                    INSERT INTO employers (id_employer, name_employer, open_vacancies, url_employer)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id_employer) DO NOTHING
                    RETURNING id_employer
                    """,
                    (employer['id'], employer['name'], employer['open_vacancies'], employer['alternate_url']))
        conn.commit()
        conn.close()

    def save_vacancies_to_database(self, data: list[dict[str, Any]]):
        """Сохранение данных о вакансиях в базу данных."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            for vacancy in data:
                cur.execute(
                    """
                    INSERT INTO vacancies (id_vacancy, name_vacancy, id_employer, name_employer, city, salary_from, 
                    salary_to, salary_avg, experience, requirement, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy['id_vacancy'], vacancy['name_vacancy'], vacancy['id_employer'], vacancy['name_employer'],
                     vacancy['city'], vacancy['salary_from'], vacancy['salary_to'], vacancy['salary_avg'], vacancy['experience'],
                     vacancy['requirement'], vacancy['url']))

        conn.commit()
        conn.close()


class DBManager(DBCreate):
    """Работает с базами данных"""
    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        list_companies_and_vacancies_count = []
        with conn.cursor() as cur:
            cur.execute("SELECT name_employer, open_vacancies FROM employers")
            rows = cur.fetchall()
            for row in rows:
                list_companies_and_vacancies_count.append(row)
            return list_companies_and_vacancies_count

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты, и ссылки, на вакансию."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        list_all_vacancies = []
        with conn.cursor() as cur:
            cur.execute("SELECT name_employer, name_vacancy, salary_from, salary_to, url FROM vacancies")
            rows = cur.fetchall()
            for row in rows:
                list_all_vacancies.append(row)
            return list_all_vacancies

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("SELECT ROUND(AVG(salary_avg)) as avg_salary FROM vacancies")
            return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        list_with_higher_salary_vacancies = []
        with conn.cursor() as cur:
            cur.execute(
                "SELECT name_employer, name_vacancy, salary_avg, url FROM vacancies"
                " WHERE salary_avg > (SELECT AVG(salary_avg) FROM vacancies)"
                )
            rows = cur.fetchall()
            for row in rows:
                list_with_higher_salary_vacancies.append(row)
            return list_with_higher_salary_vacancies

    def get_vacancies_with_keyword(self, word: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        list_with_keyword_vacancies = []
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM vacancies"
                f" WHERE name_vacancy ILIKE '%{word}%'"
            )
            rows = cur.fetchall()
            for row in rows:
                list_with_keyword_vacancies.append(row)
            return list_with_keyword_vacancies
