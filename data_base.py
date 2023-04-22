# def create_database(database_name: str, params: dict) -> None:
import psycopg2
from typing import Any
from config import config
# from httplib2.auth import params


# conn = psycopg2.connect(dbname='postgres', **params)
# cur = conn.cursor()
# try:
#     with conn:
#         with conn.cursor() as cur:
#             cur.execute(f'DROP DATABASE ')
#             cur.execute("INSERT INTO user_account VALUES (%s, %s)", (8, 'Olya'))
#             cur.execute('SELECT * FROM user_account')
#
#             rows = cur.fetchall()
#             for row in rows:
#                 print(row)
#
# finally:
#     conn.close()

def create_database(database_name: str, params: dict) -> None:
    """Создание базы данных и таблиц для сохранения данных о каналах и видео."""
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
                sequence_number SERIAL PRIMARY KEY,
                id_employer INT,
                name_employer VARCHAR(255) NOT NULL,
                open_vacancies VARCHAR,
                url_employer TEXT
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                sequence_number SERIAL PRIMARY KEY,
                id_vacancy INT,
                name_vacancy VARCHAR(255) NOT NULL,
                id_employer INT,
                name_employer VARCHAR NOT NULL,
                experience TEXT,
                requirement TEXT,
                url TEXT
            )
        """)

    conn.commit()
    conn.close()


def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for employer in data:
            # channel_data = employer['channel']['snippet']
            # channel_stats = employer['channel']['statistics']
            cur.execute(
                """
                INSERT INTO employers (id_employer, name_employer, open_vacancies, url_employer)
                VALUES (%s, %s, %s, %s)
                RETURNING id_employer
                """,
                (employer['id'], employer['name'], employer['open_vacancies'], employer['alternate_url']))
            # channel_id = cur.fetchone()[0]
            # videos_data = channel['videos']
            # for video in videos_data:
            #     video_data = video['snippet']
            #     cur.execute(
            #         """
            #         INSERT INTO videos (channel_id[i]['id'], title, publish_date, video_url)
            #         VALUES (%s, %s, %s, %s)
            #         """,
            #         (channel_id, video_data['title'], video_data['publishedAt'],
            #          f"https://www.youtube.com/watch?v={video['id']['videoId']}")
            #     )

    conn.commit()
    conn.close()