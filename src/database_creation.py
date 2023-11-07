import psycopg2
from config import config


def create_database(db_name, params) -> None:
    """Функция создания базы данных"""
    connection = psycopg2.connect(dbname='postgres', **params)
    connection.autocommit = True
    cur = connection.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
    cur.execute(f"CREATE DATABASE {db_name};")

    cur.close()
    connection.close()


def create_table(table_name, params) -> None:
    """
    Функция создания таблицы для ее последующего заполнения данными о вакансиях
    """
    conn = None
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                cur.execute(f'CREATE TABLE "{table_name}"'
                            f'(name_company varchar(50),'
                            f'vacancy_id smallint,'
                            f'company_id smallint,'
                            f'name_vacancy varchar(100),'
                            f'salary_from smallint,'
                            f'city varchar(50),'
                            f'url_vacancy character varying(50)'    
                            f'schedule varchar(50),'
                            f'experience character varying(50)'
                            f'url_company character varying(50))')

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_data_to_database(table_name, data: list[dict], params) -> None:
    """
    Функция для заполнения таблицы базы данных
    :param table_name: название таблицы для заполнения
    :param data: список с вакансиями компании
    :param params: параметры для подключения к базе данных
    :return: None
    """
    conn = None
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                for vacancy in data:
                  # Запрос для заполнения таблицы
                    cur.execute(f'INSERT INTO "{table_name}" '
                                f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (vacancy['name_company'],
                                                                                     vacancy['vacancy_id'],
                                                                                     vacancy['company_id'],
                                                                                     vacancy['name_vacancy'],
                                                                                     vacancy['salary_from'],
                                                                                     vacancy['city'],
                                                                                     vacancy['url_vacancy'],
                                                                                     vacancy['schedule'],
                                                                                     vacancy['experience'],
                                                                                     vacancy['url_company']))

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# params = config()
# # company_id_add = HeadhunterVacancy("Воронеж")
# # database = company_id_add.company_information()
# create_database('Employer_vacancy', params)
# params.update({'dbname': 'Employer_vacancy'})
# create_table_company('Employer', params)
# # add_company_to_database('Company', database, params)

# params = config()  # Параметры для подключения к базе данных

# create_database(DB_NAME, params)  # создание базы данных
# params.update({'database': DB_NAME})  # обновление параметров для подключения к базе данных
# print(f"БД {DB_NAME} успешно создана")

#
# params.update({'dbname': db_name})
# create_table(table_name, params)  # Создание в базе данных таблицы для заполнения
# print(f"Таблица {table_name} успешно создана")
