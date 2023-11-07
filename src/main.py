import database_creation
from config import config

db_name = 'Employer_vacancy'
table_name = 'Employer'


if __name__ == "__main__":
	params = config()  # Параметры для подключения к базе данных
	# database_creation.create_database(db_name, params)  # создание базы данных
	# print(f"БД {db_name} успешно создана")
	params.update({'dbname': db_name})
	database_creation.create_table(table_name, params)  # Создание в базе данных таблицы для заполнения
	print(f"Таблица {table_name} успешно создана")
