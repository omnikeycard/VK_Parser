# Парсер обсуждений для ВК, готовая версия

from bs4 import BeautifulSoup
import requests

forms_list = []
authors_list = []

def parser(quantity_sites):
    site = f'https://vk.com/topic-201145305_46761521?offset={quantity_sites}'
    content = requests.get(site).text
    soup = BeautifulSoup(content, "lxml")
    client_forms = soup.findAll('div', class_="pi_text") # Содержание анкеты
    author = soup.findAll('a', class_="pi_author") # Имя-фамилия автора
    for x in client_forms:
        forms_list.append(x.text)

    for x in author:
        authors_list.append(x.text)

    for z in range(len(authors_list)):
        output = f'{authors_list[z]} - {forms_list[z]} \n'
        print(output)

def get_web():
    content = requests.get('https://vk.com/topic-201145305_46761521').text
    soup = BeautifulSoup(content, "html.parser")
    result = soup.findAll('a', class_="pg_link")
    result = result[-1].get('href')
    result = int(result[result.index('offset=')+7:]) // 20
    return result

def search(quantity_sites):
    for x in range(get_web()):
        quantity_sites = quantity_sites + 20
        parser(quantity_sites)

input('''Бот, сканирующий обсуждение с анкетами и выводящий их в окно терминала. Вся работа с текстом осуществляется посредством горячего сочетания клавиш Ctrl+F (поиск регулярных выражений)
Нажмите Enter для запуска программы
''')
print('Запуск...')
search(0)
input('\nСканирование закончено. Для поиска повторяющихся выражений используйте горячую клавишу Ctrl+F. Нажмите Enter чтобы закрыть терминал')
