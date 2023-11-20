from configparser import ConfigParser
import psycopg2


class DBManager:

    def __init__(self) -> None:
        self.__config = self.__get_config()

    @staticmethod
    def __get_config() -> dict:
        parser = ConfigParser()
        parser.read('database.ini')
        config = {}
        if parser.has_section('postgresql'):
            params = parser.items('postgresql')
            for prm in params:
                config[prm[0]] = prm[1]
        else:
            raise Exception('Секция postgresql не найдена в database.ini')
        return config

    def __execute(self, query):
        conn = psycopg2.connect(**self.__config)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.execute(query)
        conn.close()

    def __insert_many(self, query, values):
        conn = psycopg2.connect(**self.__config)
        conn.autocommit = True

        with conn.cursor() as cur:
            cur.executemany(query, values)
        conn.close()

    def __fetch_all(self, query):
        conn = psycopg2.connect(**self.__config)

        with conn.cursor() as cur:
            cur.execute(query)
            values = cur.fetchall()
        conn.close()
        return values

    def __fetch_one(self, query):
        conn = psycopg2.connect(**self.__config)

        with conn.cursor() as cur:
            cur.execute(query)
            value = cur.fetchone()
        conn.close()
        return value

    def create_database(self, db_name) -> None:

        config = self.__config.copy()
        conn = psycopg2.connect(**config)

        try:
            conn.autocommit = True
            # Создаем объект курсора
            with conn.cursor() as cur:
                # Проверяем существование базы данных
                query = f'DROP DATABASE IF EXISTS {db_name}'
                cur.execute(query)
                # Создаем чистую базу данных
                query = f'CREATE DATABASE {db_name}'
                cur.execute(query)
        finally:
            conn.close()
            self.__config['database'] = db_name
            print(f'База данных {db_name} создана')

    def create_tables(self) -> None:
        query = """
        CREATE TABLE employers (
            employer_id INT PRIMARY KEY,
            title VARCHAR(50)
            ); 
        """
        self.__execute(query)
        print('Таблица employers создана')

        query = """
        CREATE TABLE vacancies (
            id SERIAL PRIMARY KEY,
            vacanсy_id INT,
            title VARCHAR(100),
            salary_min FLOAT,
            city VARCHAR(80),
            url VARCHAR(100),
            employer_id INT REFERENCES employers (employer_id),
            work_mode VARCHAR(100),
            experience VARCHAR(80),
            requirements TEXT
            );
        """
        self.__execute(query)
        print('Таблица vacancies создана')

    def fill_employers(self, employers):
        print('Заполнение данными таблицы employers...')
        employers = [(int(e_id), name) for e_id, name in employers.items()]
        query = """
            INSERT INTO employers (employer_id, title)
            VALUES (%s, %s)
            """
        self.__insert_many(query, employers)
        print('Таблица employers заполнена данными')

    def fill_vacancies(self, vacancies):
        print('Заполнение данными таблицы vacancies...')
        vacancies_info = set()
        for vacancy in vacancies:
            salary_min = min(vacancy['salary_from'], vacancy['salary_to'])
            if not salary_min:
                continue
            else:
                vacancies_info.add((
                    vacancy['id'],
                    vacancy['name'],
                    salary_min,
                    vacancy['city'],
                    vacancy['url'],
                    vacancy['employer_id'],
                    vacancy['work_mode'],
                    vacancy['experience'],
                    vacancy['requirements'],
                ))
            vacancies_list = list(vacancies_info)
            query = """
                        INSERT INTO vacancies (vacanсy_id, title, salary_min, city,
                        url, employer_id, work_mode, experience, requirements)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
            self.__insert_many(query, vacancies_list)
        print('Таблица vacancies заполнена данными')

    def get_companies_and_vacancies_count(self):
        query = """SELECT company_name, COUNT(*)
        FROM vacancies
        JOIN companies USING (company_id)
        GROUP BY company_name"""
        count = self.__fetch_all(query)
        return count

    def get_all_vacancies(self):
        query = """SELECT company_name, vacancy_name, salary_average, url
        FROM vacancies
        JOIN companies USING (company_id)
        """
        all_vacancies = self.__fetch_all(query)
        return all_vacancies

    def get_avg_salary(self):
        query = """
            SELECT AVG(vacancies.salary_min)
            FROM vacancies
            """
        value = self.__fetch_all(query)[0][0]
        return value

    def get_vacancies_with_higher_salary(self):
        query = """SELECT company_name, vacancy_name, salary_average, url
        FROM vacancies
        JOIN companies USING (company_id_hh)
        WHERE salary_average > (SELECT AVG(salary_average)
        FROM vacancies
        WHERE salary_average > 0)
        ORDER BY salary_average DESC"""
        vacancies = self.__fetch_all(query)
        return vacancies

    def get_vacancies_with_keyword(self):
        query = """SELECT company_name, vacancy_name, salary_average, url
        FROM vacancies
        JOIN companies USING (company_id_hh)
        WHERE vacancy_name LIKE '%{word.lower()}%'
        OR vacancy_name LIKE '%{word.title()}%'
        OR vacancy_name LIKE '%{word.upper()}%'"""
        vacancies = self.__fetch_all(query)
        return vacancies
