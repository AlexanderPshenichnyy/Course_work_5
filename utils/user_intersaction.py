from utils.dbmanager import DBManager
def user_interaction(db_manager):
	"""
	Функция для вывода запросов к БД
	:param db_manager: экземпляр класса для работы с БД
	"""
	choice_one = input('Показать всех работодателей и количество вакансий от каждого? (1 - да): ')
	if choice_one == '1':
		list_employers_and_vacancies_count = db_manager.get_companies_and_vacancies_count()
		for one_employer in list_employers_and_vacancies_count:
			print(f'Получено {one_employer[1]} вакансий от работодателя {one_employer[0]} \n')
	else:
		input('Для продолжения нажмите любую клавишу')

	choice_two = input('Показать всех работодателей и количество вакансий от каждого? (1 - да): ')
	if choice_two == '1':
		all_vacancies_list = db_manager.get_all_vacancies()
		for one_vacancy in all_vacancies_list:
			print(*one_vacancy, sep=' ::::')
	else:
		input('Для продолжения нажмите любую клавишу')

	choice_three = input('Показать среднюю зарплату по всем вакансиям? (1 - да): ')
	if choice_three == '1':
		print(f'\nСредняя зарплата по вакансиям равна - {db_manager.get_avg_salary()} руб.\n')
	else:
		input('Для продолжения нажмите любую клавишу')

	choice_four = input('Показать вакансии с з/п выше средней? (1 - да): ')
	if choice_four == '1':
		print('\nВот наиболее высокооплачиваемые вакансии:\n')
		vacancies_with_high_salary = db_manager.get_vacancies_with_higher_salary()
		for one_vacancy in vacancies_with_high_salary:
			print(*one_vacancy, sep=' :::: ')
	else:
		input('Для продолжения нажмите любую клавишу')

	keyword = input('Введите ключевое слово для поиска в названиях вакансий: ')
	if keyword:
		vacancies_with_keyword = db_manager.get_vacancies_with_keyword(keyword)
		if vacancies_with_keyword:
			print('\nВот вакансии по вашему запросу:\n')
			for one_vacancy in vacancies_with_keyword:
				print(*one_vacancy, sep=' :::: ')
		else:
			print('По вашему запросу не нашлось вакансий')

	else:
		exit('Кончились фильтры :(')

