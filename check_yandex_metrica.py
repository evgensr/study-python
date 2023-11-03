import re
import os
import requests

# Путь к директории с вашими файлами, нужно будет указать корректный путь
directory_path = './1/'

# Регулярное выражение для поиска номера Yandex.Metrika
pattern = re.compile(r'ym\((\d+), "init", {')

def check_metrika_on_site(domain):
    """Функция для проверки наличия счетчика Yandex.Metrika на сайте."""
    try:
        response = requests.get(f'http://{domain}', timeout=10)
        if response.status_code == 200:
            # Ищем счетчик в содержимом страницы
            if pattern.search(response.text):
                return True
    except requests.RequestException as e:
        print(f"Ошибка при запросе к {domain}: {e}")
    return False

# Проходим по всем файлам в директории
for file_name in os.listdir(directory_path):
    # Проверяем, что файл имеет расширение .txt
    if file_name.endswith('.txt'):
        # Формируем полный путь к файлу
        file_path = os.path.join(directory_path, file_name)
        # Получаем домен (имя файла без расширения)
        domain = file_name.replace('.txt', '')
        
        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            file_contents = file.read()
            
            # Ищем номер счетчика в содержимом файла
            match = pattern.search(file_contents)
            if match:
                metrika_number = match.group(1)
                # Проверяем наличие счетчика на сайте
                if not check_metrika_on_site(domain):
                    # Если счетчик на сайте не найден, выводим домен
                    print(domain)
            else:
                # Если номер счетчика не найден в файле, сообщаем об этом
                print(f"Счетчик Yandex.Metrika не найден в файле {file_name}")
