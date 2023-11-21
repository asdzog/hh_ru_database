import psycopg2
from dbmanager import DBManager
from hh_api import HeadHunterAPI
from utils import get_employers
from pprint import pprint


def main():

    db_name = 'hh_ru_vacancies'
    try:
        db_manager = DBManager()
        db_manager.create_database(db_name)
        db_manager.create_tables()
    except FileNotFoundError as e:
        print(f'Ошибка чтения файла конфигурации: {e}')
        exit()
    except psycopg2.Error as e:
        print(f'Ошибка инициализации базы данных: {e}')
        exit()
    except Exception as e:
        print(f'Ошибка чтения файла конфигурации: {e}')
        exit()

    try:
        # получение списка работодателей и их id
        employers = get_employers()

        # заполнение таблицы с работодателями в базе данных
        db_manager.fill_employers(employers)

    except FileNotFoundError as e:
        print(f'Ошибка заполнения данными таблицы \'employers\': {e}')
        exit()

    # парсинг вакансий с сайта hh.ru
    hh_api = HeadHunterAPI()
    vacancies = []
    for employer_id in employers:
        vacancies.extend(hh_api.get_vacancies(employer_id))

    # заполнение таблицы с вакансиями в базе данных
    db_manager.fill_vacancies(vacancies)

    # взаимодействие с пользователем для получения данных из базы
    while True:

        user_choice = input('''База данных вакансий готова к работе. Выберите, что хотите получить:
1 - список компаний и количество вакансий у каждой компании
2 - список вакансий с их названиями, указанием компании, зарплаты и ссылки на вакансию
3 - среднюю зарплату по вакансиям
4 - список вакансий, у которых зарплата выше средней по всем вакансиям
5 - список вакансий, в названии которых содержится искомое слово
exit - выход\n''').strip()

        match user_choice:
            case "1":
                pprint(db_manager.get_companies_and_vacancies_count())
            case "2":
                pprint(db_manager.get_all_vacancies())
            case "3":
                pprint(db_manager.get_avg_salary())
            case "4":
                pprint(db_manager.get_vacancies_with_higher_salary())
            case "5":
                keyword = input('Введите нужное слово для поиска по вакансиям \n').strip()
                pprint(db_manager.get_vacancies_with_keyword(keyword))
            case "exit":
                break
            case _:
                print('Ошибка ввода, попробуйте снова\n')


if __name__ == '__main__':
    main()
