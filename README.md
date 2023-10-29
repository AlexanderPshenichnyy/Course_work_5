Привет! Это мой курсовой проект по базам данных, вот его основной функционал:

0. Подключается по API к HH.ru;
1. Собирает информацию о 10 -ти интересных компаниях и их вакансиях в json файл;
2. Заполняет этими данными БД в postgresSQL с помощью библиотеки psycopg2;
3. Получает список всех компаний и количество вакансий у каждой компании;
4. Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию;
5. Получает среднюю зарплату по вакансиям;
6. Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям;
7. Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.