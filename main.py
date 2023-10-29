from utils.API_connect import HeadHunterAPI
from utils.dbmanager import DBManager
from utils.user_intersaction import user_interaction
from config import JSON_FILE_NAME, employer_ids


def main():
	# Инициализируем класс для поиска вакансий
	hh = HeadHunterAPI()

	# ключевое слово для поиска
	search = hh.get_vacancies_by_api(employer_ids)

	# сохранение в json
	hh.save_to_json(search)

	while True:
		db_name = input('Введите слово на английском для названия базы данных: ')
		if all(one_letter in 'abcdefghijklmnopqrstuvwxyz1234567890' for one_letter in db_name):
			db = DBManager()
			break
		else:
			print("Введите слово на английском")

	db.create_database(db_name)  # создаём БД
	db.create_table()  # создаём таблицы в БД
	db.insert_data_to_table(JSON_FILE_NAME)  # заполняем таблицы

	user_interaction(db)  # работаем с выборками в БД

if __name__ == '__main__':
	main()