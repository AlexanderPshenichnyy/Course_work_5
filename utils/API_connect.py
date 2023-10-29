from config import employer_ids
import json
import requests


class HeadHunterAPI:
	"""Класс для работы с API HeadHunter"""
	_base_url = "https://api.hh.ru/vacancies"

	def __init__(self, area=53, per_page=10):
		self.area = area
		self.per_page = per_page

	def get_vacancies_by_api(self, employer_ids):
		"""
		Выполняет сбор вакансий через API
		"""
		vacancies_list = []
		for employer in employer_ids:
			params = {
				'area': self.area,
				'employer_id': employer,
				'per_page': self.per_page
			}
			response = requests.get(self._base_url, params=params)
			if response.status_code == 200:
				vacancies = response.json()['items']
				vacancies_list.extend(self.organizer(vacancies))

		return vacancies_list

	@staticmethod
	def save_to_json(vacancies_list):
		with open('data.json', 'w', encoding='utf-8') as file:
			json.dump(vacancies_list, file, indent=2, ensure_ascii=False)

	@staticmethod
	def organizer(vacancies):

		organize_vacancies = []

		for vacancy in vacancies:
			employer = vacancy.get('employer')['name']
			id_vacancy = vacancy.get('id')
			title = vacancy.get('name')
			area = vacancy.get('area')["name"]
			salary = vacancy.get('salary')
			if not salary:
				salary_from = 0
				salary_to = 0
			else:
				salary_from = salary.get('from')
				salary_to = salary.get('to')
				if not salary_from:
					salary_from = salary_to
				if not salary_to:
					salary_to = salary_from
			url = vacancy.get('alternate_url')

			vacancy_data = {
				'employer': employer,
				'id_vacancy': id_vacancy,
				'name': title,
				'area': area,
				'salary_from': salary_from,
				'salary_to': salary_to,
				'url': url
			}
			organize_vacancies.append(vacancy_data)

		return organize_vacancies
