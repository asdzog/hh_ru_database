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
        config["dbname"] = db_name

        conn = psycopg2.connect(**config)
        conn.autocommit = True

        with conn.cursor() as cur:
            query = f'DROP DATABASE IF EXIST {self.__config["dbname"]}'
            cur.execute(query)
            query = f'CREATE DATABASE {self.__config["dbname"]}'
            cur.execute(query)

        conn.close()
        print(f'База данных {self.__config["dbname"]} создана')

    def create_tables(self) -> None:
        query = """
        CREATE TABLE employers (
            employer_id SERIAL,
            title VARCHAR(50)
            ); 
        """
        self.__execute(query)
        print('Таблица employers создана')

        query = """
        CREATE TABLE vacancies (
            vacansy_id SERIAL,
            title VARCHAR(100)
            employer_id INT REFERENCES employers (employer_id),
            salary_min FLOAT,
            url VARCHAR(100)
            );
        """
        self.__execute(query)
        print('Таблица vacancies создана')

    def fill_employers(self, values):
        employers = [(value, key) for key, value in values.items()]
        query = """
            INSERT INTO emlpoyers ('emlpoyer_id', 'title')
            VALUES
            (%s, %s)
            """
        self.__insert_many(query, employers)

    def fill_vacancies(self, values):
        employers = [(value, key) for key, value in values.items()]
        query = """
            INSERT INTO emlpoyers ('emlpoyer_id', 'title')
            VALUES
            (%s, %s)
            """
        self.__insert_many(query, employers)

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
