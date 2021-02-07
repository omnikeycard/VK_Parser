# Функциональная часть бота #

from bs4 import BeautifulSoup
import requests
import time

with open('log.txt', 'w') as f:
    f.write('')

forms_list = []
authors_list = []
hrefs_list = []
current_web = 0
quantity_sites = -20

def get_web(): # получение кол-ва страниц у обсуждения 
    content = requests.get('https://vk.com/topic-201145305_46761521').text
    soup = BeautifulSoup(content, "html.parser")
    result = soup.findAll('a', class_="pg_link")
    result = result[-1].get('href')
    return int(result[result.index('offset=')+7:]) // 20 # получение параметра offset из URL последней страницы и деление его на 20 => возвращение количества страниц

webs = get_web()

def parser(quantity_sites):

    content = requests.get(f'https://vk.com/topic-201145305_46761521?offset={quantity_sites}').text
    soup = BeautifulSoup(content, "lxml")
    first_forms = soup.findAll('div', class_="pi_text") # Содержание анкеты
    first_authors = soup.findAll('a', class_="pi_author") # Имя-фамилия автора
    forms_list.clear()
    authors_list.clear()
    hrefs_list.clear()
    for x in first_forms:
        forms_list.append(x.text)

    for x in first_authors:
        authors_list.append(x.text)
        hrefs_list.append(x.get('href')) # получение ссылки на страницу игрока
    
    for z in range(len(authors_list)): # Основной цикл вывода данных на экран
        output = f'(vk.com{hrefs_list[z]}) {authors_list[z]} - {forms_list[z]}\n'
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(f'{output}\n')
        print(output)
    first_forms.clear()
    first_authors.clear()
    
    global current_web
    current_web = current_web + 1
    if current_web > webs:
        pass
    else:
        print(f'Страница: {current_web}/{webs}')

# Основная часть бота #
input('''Бот, сканирующий обсуждение с анкетами и выводящий их в окно терминала. Вся работа с текстом осуществляется в файле log.txt посредством сочетания клавиш Ctrl+F

Нажмите Enter для запуска программы
''')
print('\nЗапуск...')

time_start = time.time()
for x in range(webs):
    quantity_sites = quantity_sites + 20
    parser(quantity_sites)
time_end = time.time()

print(f'Времени затрачено: {int(time_end - time_start)} секунд(ы)')
input('\nСканирование закончено. Для поиска повторяющихся выражений используйте горячую клавишу Ctrl+F. Нажмите Enter чтобы закрыть терминал')
