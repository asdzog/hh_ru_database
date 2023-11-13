from configparser import ConfigParser
from copy import copy
import psycopg2


class DBManager:

    def __init__(self) -> None:
        self.__config = self.__get_config

    def __get_config(self) -> dict:
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

    def create_database(self) -> None:
        config = self.__config.copy()
        config['dbname'] = 'postgres'

        conn = psycopg2.connect(**config)
        conn.autocommit = True

        with conn.cursor() as cur:
            query = f'DROP DATABASE IF EXIST {self.__config["dbname"]}'
            cur.execute(query)
            query = f'CREATE DATABASE {self.__config["dbname"]}'
            cur.execute(query)

        conn.close()
        print(f'База данных {self.__config["dbname"]} создана')


    def get_companies_and_vacancies_count(self):
        pass

    def get_all_vacancies(self):
        pass

    def get_avg_salary(self):
        pass

    def get_vacancies_with_higher_salary(self):
        pass

    def get_vacancies_with_keyword(self):
        pass
