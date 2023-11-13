import requests
from bs4 import BeautifulSoup as BS
from pprint import pprint
from utils import create_database


def get_employer_id_by_name(employer_name):
    url = 'https://api.hh.ru/employers'
    params = {'text': employer_name}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'items' in data and data['items']:
            # Предполагаем, что берем первый найденный работодатель
            employer_id = data['items'][0]['id']
            return employer_id
        else:
            print('Работодатель не найден')
    else:
        print(f'Ошибка при запросе: {response.status_code}')


def get_employer_name_by_id(employer_id):
    url = f'https://hh.ru/employer/{employer_id}'

    response = requests.get(url)


    if response.status_code == 200:
        soup = BS(response.content, 'html.parser')
        employer_name = soup.find('span', class_='employer-sidebar-header__employer-name').text.strip()
        return employer_name
    else:
        print(f'Ошибка при запросе: {response.status_code}')


def main():
    employer_name = input('Введите название работодателя: ')

    url = 'https://api.hh.ru/employers'
    params = {'text': employer_name}

    response = requests.get(url, params=params)
    pprint(response.json())

    if response.status_code == 200:
        data = response.json()
        if 'items' in data and data['items']:
            # Предполагаем, что берем первый найденный работодатель
            employer_id = data['items'][0]['id']
            print(f'ID работодателя "{employer_name}": {employer_id}')
        else:
            print('Работодатель не найден')
    else:
        print(f'Ошибка при запросе: {response.status_code}')


if __name__ == '__main__':
    create_database('hh_ru_vacancies')
