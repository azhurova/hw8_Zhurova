#1задача
import requests

super_heroes = requests.get('https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json')
HEROES_NAMES = ['Hulk', 'Captain America', 'Thanos']
# print(super_heroes.text)
super_heroes_json = super_heroes.json()

three_heroes = {}

for hero in super_heroes_json:
    hero_name = hero.get('name')
    if hero_name in HEROES_NAMES:
        three_heroes[hero_name] = (hero.get('powerstats').get('intelligence'))

# print(three_heroes)
max_intelligence_hero_name = max(three_heroes, key=three_heroes.get)
# print(max_intelligence_hero_name)
print(
    f'Самый умный(intelligence)это: {max_intelligence_hero_name} с уровнем intelligence, равным: {three_heroes.get(max_intelligence_hero_name)}')



#2 задача

from os import path
from urllib import parse

import requests

# Константы
API_URL = 'https://cloud-api.yandex.net'
API_PATH = '/v1/disk/resources'

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):

        # метода upload в API Яндекс.Диска
        API_METHOD = 'upload'

        print('Используя токен, создаем HTTP-заголовок для авторизации в API Яндекс.Диска:')
        authorization_header = {"Authorization": self.token}
        print('authorization_header ==', authorization_header, '\n')

        print('Кодируем в формат URLencoded имя загружаемого файла на Яндекс.Диск и добавляем его к параметру "path":')
        urlencoded_path = parse.urlencode({"path": "/" + path.basename(file_path)})
        print('urlencoded_path ==', urlencoded_path, '\n')

        print('Создаем полный URL для получения ссылки для загрузки файла:')
        full_url = f'{API_URL}{API_PATH}/{API_METHOD}?{urlencoded_path}'
        print('full_url ==', full_url, '\n')

        print(
            'Получаем с помощью HTTP-запроса GET к API Яндекс.Диска json-словарь, в котором ссылку для загрузки файла получаем (get) по ключу "href":')
        get_response = requests.get(url=full_url, headers=authorization_header)

        if not get_response.ok:
            return get_response
        else:
            upload_url = get_response.json().get('href')
            print('upload_url ==', upload_url, '\n')

        with open(file_path, mode='rb') as upload_file:

            print(
                'Загружаем файл на Яндекс.Диск с помощью HTTP-запроса PUT и сохраняем результат запроса в переменную put_response:')
            put_response = requests.request('PUT', upload_url, data=upload_file)
            print('put_response ==', put_response, '\n')

        return put_response

if __name__ == '__main__':

    path_to_file = input('Введите путь к файлу: ')
    print('Введенный путь к файлу:\npath_to_file ==', path_to_file, '\n')
    token = input('Введите токен: ')
    print('Введенный токен:\ntoken ==', token, '\n')

    uploader = YaUploader(token)
    print('Созданный объект класса YaUploader:\nuploader ==', uploader, '\n')
    print('Переданный при создании объекта токен:\nuploader.token ==', uploader.token, '\n')

    result = uploader.upload(file_path=path_to_file)

    print(f'Файл {path_to_file} успешно загружен, код HTTP-ответа: {result.status_code}' if result.ok else f'Ошибка при загрузке файла {path_to_file}, код HTTP-ответа: {result.status_code}, текст ошибки:\n{result.text}')