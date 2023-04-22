import psycopg2
from typing import Any


def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях."""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    cur.close()
    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

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
                salary VARCHAR,
                city VARCHAR(255),
                experience TEXT,
                requirement TEXT,
                url TEXT
            )
        """)

    conn.commit()
    conn.close()


def save_employers_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о работодателях в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            cur.execute(
                """
                INSERT INTO employers (id_employer, name_employer, open_vacancies, url_employer)
                VALUES (%s, %s, %s, %s)
                RETURNING id_employer
                """,
                (employer['id'], employer['name'], employer['open_vacancies'], employer['alternate_url']))
    conn.commit()
    conn.close()


def save_vacancies_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о вакансиях в базу данных."""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        for vacancy in data:
            # print(vacancy)
            cur.execute(
                """
                INSERT INTO vacancies (id_vacancy, name_vacancy, id_employer, name_employer, salary, city, experience, requirement, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (vacancy['id_vacancy'], vacancy['name_vacancy'], vacancy['id_employer'], vacancy['name_employer'], vacancy['city'],
                 vacancy['salary'], vacancy['experience'], vacancy['requirement'], vacancy['url']))

    conn.commit()
    conn.close()