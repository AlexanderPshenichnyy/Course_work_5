import psycopg2
import json
import os
from config import config, JSON_DATA_DIR


class DBManager:
	"""Класс для работы с базой данных"""

	def __init__(self):
		self.database_name = None

	def connect_to_database(self):
		"""Метод для подключения к базе данных"""
		params = config()
		return psycopg2.connect(dbname=self.database_name, **params)

	def create_database(self, dbname: str) -> None:
		"""
		Метод для создания базы данных
		:param dbname: имя создаваемой базы данных
		"""
		try:
			connection = self.connect_to_database()
			connection.autocommit = True
			# Создаём базу данных
			with connection.cursor() as cur:
				cur.execute(f'DROP DATABASE IF EXISTS {dbname}')
				cur.execute(f'CREATE DATABASE {dbname}')
				self.database_name = dbname
				print(f'База данных {dbname} успешно создана')

			connection.close()

		except psycopg2.OperationalError as e:
			print(f'Ошибка создания базы данных: {e}')

	def create_table(self):
		"""
		Метод для создания таблиц в базе данных
		"""
		create_tables = """
                        CREATE TABLE IF NOT EXISTS employers (
                        employer_id serial PRIMARY KEY,
                        employer_name varchar NOT NULL
                        );

                        CREATE TABLE IF NOT EXISTS vacancies (
                        vacancy_id serial PRIMARY KEY,
                        employer_id int REFERENCES employers(employer_id) ON DELETE CASCADE,
                        vacancy_title varchar(255) NOT NULL,
                        vacancy_url varchar(150) NOT NULL,
                        vacancy_area varchar(80),
                        salary_from int,
                        salary_to int
                        );
                        """
		try:
			with self.connect_to_database() as connection:
				# Создаём таблицы
				with connection.cursor() as cur:
					cur.execute(create_tables)
					print('Таблицы успешно созданы')
			connection.commit()
			connection.close()

		except psycopg2.OperationalError as e:
			print(e)

	def insert_data_to_table(self, data_filename: str):
		"""
		Метод для заполнения таблиц в базе данных из файла json
		:param data_filename: файл json с данными
		:param insert_to_employers: запрос для заполнения таблицы работодателей
		:param insert_to_vacancies: запрос для заполнения таблицы вакансий
		"""
		# Читаем данные из файла
		insert_to_employers = """INSERT INTO employers (employer_name) 
		                         SELECT %s
		                         WHERE NOT EXISTS (
		                         SELECT employer_name 
		                         FROM employers
		                         WHERE employer_name = %s)
		                         """

		# Запрос для вставки данных в таблицу с вакансиями, где employer_id берём из таблицы employers
		insert_to_vacancies = """INSERT INTO vacancies (employer_id, vacancy_title, vacancy_url, vacancy_area,
		                         salary_from, salary_to)
		                         VALUES (%s, %s, %s, %s, %s, %s)
		                         """
		with open(data_filename, 'r', encoding='utf-8') as file:
			data = json.load(file)
		# Заполняем таблицы данными из файла
		try:
			with self.connect_to_database() as connection:
				connection.autocommit = True
				with connection.cursor() as cur:
					for vacancy in data:
						cur.execute(insert_to_employers, (vacancy['employer'], vacancy['employer']))

						cur.execute("SELECT employer_id FROM employers ORDER BY employer_id DESC LIMIT 1")
						employer_id = cur.fetchone()

						cur.execute(insert_to_vacancies, (employer_id, vacancy['name'],
													  vacancy['url'], vacancy['area'],
													  vacancy['salary_from'], vacancy['salary_to']))

				print(f'Таблицы успешно заполнены данными из файла {data_filename}')

			connection.close()

		except psycopg2.Error as e:
			print(f"Ошибка заполнения: {e}")

	def get_companies_and_vacancies_count(self):
		"""Получает список всех компаний и количество вакансий у каждой компании"""
		with self.connect_to_database() as connection:
			with connection.cursor() as cur:
				cur.execute('''select employer_name, count(*)
								from employers
								join vacancies using (employer_id)
								group by employer_name''')
				res = cur.fetchall()
		connection.close()
		return res

	def get_all_vacancies(self):
		"""Получает список всех вакансий с указанием названия компании,
		названия вакансии и зарплаты и ссылки на вакансию"""
		with self.connect_to_database() as connection:
			with connection.cursor() as cur:
				cur.execute("""
                          SELECT employers.employer_name, vacancies.vacancy_title,
                          (vacancies.salary_from + vacancies.salary_to) / 2 AS average_salary, vacancies.vacancy_url
                          FROM vacancies
                          JOIN employers ON vacancies.employer_id = employers.employer_id
                          ORDER BY employers.employer_name;
                          """)
				res = cur.fetchall()
		connection.close()
		return res

	def get_avg_salary(self):
		"""Получает среднюю зарплату по вакансиям"""
		with self.connect_to_database() as connection:
			with connection.cursor() as cur:
				cur.execute("SELECT CAST(AVG((salary_from+salary_to)/2) AS INT) FROM vacancies")
				res = cur.fetchone()[0]
		connection.close()
		return res

	def get_vacancies_with_higher_salary(self):
		"""Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
		with self.connect_to_database() as connection:
			with connection.cursor() as cur:
				cur.execute("""
                        SELECT employers.employer_name, vacancies.vacancy_title, 
                        (vacancies.salary_from + vacancies.salary_to) / 2, vacancies.vacancy_url 
                        FROM vacancies 
                        JOIN employers ON vacancies.employer_id = employers.employer_id 
                        WHERE (vacancies.salary_from + vacancies.salary_to) / 2 >  
                        (SELECT CAST(AVG((vacancies.salary_from+vacancies.salary_to)/2) AS INT) FROM vacancies) 
                        ORDER BY employers.employer_name;
                        """)
				res = cur.fetchall()
		connection.close()
		return res

	def get_vacancies_with_keyword(self, keyword):
		"""Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
		vacancies_with_keyword_query = f"""
                                        SELECT employers.employer_name, vacancies.vacancy_title,
                                        (vacancies.salary_from + vacancies.salary_to) / 2, vacancies.vacancy_url
                                        FROM vacancies
                                        JOIN employers ON vacancies.employer_id = employers.employer_id
                                        WHERE vacancy_title LIKE '%{keyword}%'
                                        ORDER BY employers.employer_name;
                                        """

		with self.connect_to_database() as connection:
			with connection.cursor() as cur:
				cur.execute(vacancies_with_keyword_query)
				res = cur.fetchall()
		connection.close()
		return res


