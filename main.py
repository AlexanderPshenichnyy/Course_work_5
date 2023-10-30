from utils.dbmanager import DBManager
from utils.API_connect import HeadHunterAPI
from config import JSON_FILE_NAME, employer_ids
from utils.user_interaction import user_interaction


def main():
    hh = HeadHunterAPI()

    vacancies_list = hh.get_vacancies_by_api(employer_ids)  # получаем вакансии

    hh.save_to_json(vacancies_list)  # записываем вакансии в файл

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
