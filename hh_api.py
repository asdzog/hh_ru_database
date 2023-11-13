import copy
import requests
from utils import remove_tags, convert_currency


class HeadHunterAPI:
    """
    Класс для работы с API hh.ru
    """
    HH_API_URL = 'https://api.hh.ru/employers'

    params_default = {
        'text': [],  # ключевое слово или их список
        'area': 1,  # поиск осуществляется по вакансиям города 1 - Москва
        'per_page': 100,  # число вакансий на странице
        'date': 7  # период времени для поиска
    }

    def get_vacancies(self):
        vc_list = []
        hh_ru_data = requests.get(self.HH_API_URL, self.params)
        code = hh_ru_data.status_code
        if code != 200:
            raise ParsingError(f'Ошибка получения вакансий! Статус-код: {code}')
        vacancies = hh_ru_data.json()['items']

        for vc in vacancies:
            if vc['salary'] is None:
                salary_from = 0
                salary_to = 0
                salary = 'Зарплата не указана'
            else:
                amount_to = int(vc['salary']['to']) if vc['salary']['to'] else 0
                salary_to = convert_currency(vc['salary']['currency'], amount_to)
                amount_from = int(vc['salary']['from']) if vc['salary']['from'] else 0
                salary_from = convert_currency(vc['salary']['currency'], amount_from)
                if salary_from:
                    if salary_to:
                        salary = f'Зарплата от {salary_from} до {salary_to}'
                    else:
                        salary = f'Зарплата от {salary_from}'
                else:
                    if salary_to:
                        salary = f'Зарплата до {salary_to}'
                    else:
                        salary = 'Зарплата не указана'

            # убираем html-теги из строки с требованиями
            if vc['snippet']['requirement']:
                reqs_without_text = remove_tags(vc['snippet']['requirement'])
            else:
                reqs_without_text = 'Требования не указаны'

            vc_list.append({
                'resource': 'HeadHunter',
                'id': vc['id'], 'name': vc['name'], 'city': vc['area']['name'], 'salary': salary,
                'url': vc['alternate_url'], 'work_mode': vc['employment']['name'],
                'salary_from': salary_from, 'salary_to': salary_to,
                'experience': vc['experience']['name'], 'employer': vc['employer']['name'],
                'employer_url': vc['employer'].get('alternate_url', 'Employer has not URL'), 'requirements': reqs_without_text[:170] + '...'
            })
        return vc_list