import time
import requests
import matplotlib.pyplot as plt
import subprocess
import pandas as pd
import logging
import json

url_1 = 'http://192.168.22.220/sensors'  # Адрес страницы с сенсорами
url_2 = 'http://192.168.22.123/sensors'  # Адрес страницы с сенсорами
temp = []  # Массив для хранения данных температуры
temp_k = []
temp_hot = []  # Массив для хранения данных температуры
pressure = []  # Массив для записи данных о давлении
time_get = []
interval = 60 * 10  # Интервал обновления данных в секундах
graph_delta = 48  # Количество часов для отображения на графике
data_col = (3600 * graph_delta) / interval  # Количество записей для отображения на графике


def zapros_sensor(url_link, num):  # Функция для запроса данных с сенсора
    try:
        zapros = requests.get(url_link)  # Делаем запрос на адрес url
        out = zapros.text.split(';')[num].split(':')[1]  # Полученный текст запроса разбиваем на массив по ; и
        # берем нужны параметр. Параметр разбиваем на имя поля и значение по точке с запятой
        return out  # Возвращаем значение полученного параметра
    except Exception as e:  # Если запрос не удался, то возвращаем 0
        logging.error(f'Ошибка запроса данных с сенсора {e}')
        print(e)
        return 888888  # Признак ошибки получения данных


def check_len_data(spisok):  # Функция для проверки длины массива
    if len(spisok) > data_col:
        spisok.pop(0)
    return spisok


def plus(tem):  # Добавляем плюс к положительным значениям
    return round(tem, 1) if tem <= 0 else '+' + str(round(tem, 1))


def save_to_json(data, name):  # Функция для сохранения данных в json файл
    try:
        with open(name, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        logging.error(f'Ошибка сохранения данных в json файл {e}')
        print(e)


def read_from_json(data, name):  # Функция для чтения данных из json файла
    try:
        with open(name, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        logging.error(f'Ошибка чтения данных из json файла {e}')
        print(e)


def update_data():  # Функция для обновления данных
    global temp, pressure, temp_hot, temp_k, time_get  # Объявляем глобальные переменные
    try:
        temp = read_from_json(temp, 'temp.json')  # Читаем данные из json файла
        pressure = read_from_json(pressure, 'pressure.json')
        temp_hot = read_from_json(temp_hot, 'temp_hot.json')
        temp_k = read_from_json(temp_k, 'temp_k.json')
        time_get = read_from_json(time_get, 'time_get.json')
        while True:
            mont = int(time.strftime('%m'))  # Получаем месяц
            print(type(mont))
            time_get.append(time.strftime('%H:%M'))  # Получаем время
            sens_t_ul = float(zapros_sensor(url_1, 1))  # Получаем данные с сенсора во временную переменную
            print(type(sens_t_ul))
            sens_t_kv = float(zapros_sensor(url_2, 6))  # Получаем данные с сенсора во временную переменную
            sens_t_hot = float(zapros_sensor(url_2, 5))  # Получаем данные с сенсора во временную переменную
            sens_pressure = float(zapros_sensor(url_2, 4))  # Получаем данные с сенсора во временную переменную
            temp_hot.append(sens_t_hot if sens_t_hot != 888888 else temp_hot[-1])  # Добавляем данные в массив
            temp.append(
                sens_t_ul if sens_t_ul != 888888 else temp[-1])  # Добавляем значение полученное из сенсора в массив
            temp_k.append(
                sens_t_kv if sens_t_kv != 888888 else temp_k[-1])  # Добавляем значение полученное из сенсора в массив
            pressure.append(sens_pressure if sens_pressure != 888888 else pressure[
                -1])  # Добавляем значение полученное из сенсора в массив
            check_len_data(temp_hot)  # Проверяем длину массива
            check_len_data(temp)  # Проверяем длину массива и удаляем первый элемент если он больше нужного количества
            check_len_data(temp_k)  # Проверяем длину массива и удаляем первый элемент если он больше нужного количества
            check_len_data(
                pressure)  # Проверяем длину массива и удаляем первый элемент если он больше нужного количества
            check_len_data(
                time_get)  # Проверяем длину массива и удаляем первый элемент если он больше нужного количества
            save_to_json(temp, 'temp.json')  # Сохраняем данные в json файл
            save_to_json(pressure, 'pressure.json')
            save_to_json(temp_hot, 'temp_hot.json')
            save_to_json(temp_k, 'temp_k.json')
            save_to_json(time_get, 'time_get.json')
            print(
                f'Обновлено в {time_get[-1]}: {temp[-1]}, {temp_k[-1]}, {int((pressure[-1]))}')  # Выводим время
            # последнего обновления
            plt.figure(1, figsize=(20, 15), dpi=80)  # Создаем график и задаем размеры его по ширине и высоте
            if 3 < mont < 10:
                df = pd.DataFrame(
                    {'Время': time_get, 'Улица': temp, 'Дом': temp_k, 'Давление': pressure})  # Создаем датафрейм
                ax = df.plot(x='Время', y=['Дом', 'Улица'], figsize=(18, 10), grid=True)  # Создаем график
                ax = df.plot(x='Время', secondary_y=['Давление'], figsize=(18, 10), grid=True,
                             color=['b', 'r', 'g', 'y'], linewidth=3)  # Создаем график
                plt.title(
                    f'Атмосферное давление: {int(pressure[-1])} мм.рт.ст., Температура: улица {plus(temp[-1])}°C, дома: {plus(temp_k[-1])}°С',
                    fontsize=20)  # Задаем заголовок графика
            else:
                df = pd.DataFrame(
                    {'Время': time_get, 'Улица': temp, 'Дом': temp_k, 'Давление': pressure,
                     'Отопление': temp_hot})  # Создаем датафрейм
                ax = df.plot(x='Время', y=['Дом', 'Улица', 'Отопление'], figsize=(18, 10), grid=True)  # Создаем график
                ax = df.plot(x='Время', secondary_y=['Давление'], figsize=(18, 10), grid=True,
                             color=['b', 'r', 'g', 'y'], linewidth=3)  # Создаем график
                plt.title(
                    f'Атмосферное давление: {int(pressure[-1])} мм.рт.ст., Температура: улица {plus(temp[-1])}°C, дома: {plus(temp_k[-1])}°С, отопление: {plus(temp_hot[-1])}°С',
                    fontsize=20)  # Задаем заголовок графика
            plt.grid(True)  # Включаем сетку
            plt.savefig('static/image.png')  # Сохраняем график в файл
            plt.clf()  # Очищаем график
            plt.close('all')  # Закрываем график
            time.sleep(interval)  # Приостанавливаем выполнение функции на интервал времени
    except Exception as e:
        logging.error(f'Ошибка в основном модуле программы обновления и рисования: {e}')  # Выводим ошибку в лог
        print(e)


if __name__ == '__main__':
    logging.basicConfig(filename='graph.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info('Запуск программы')  # Выводим в лог информацию о запуске программы
    try:
        subprocess.Popen('python server1.py', shell=True)  # Запускаем сервер
    except Exception as e:
        logging.error(f'Ошибка в модуле запуска сервера: {e}')  # Выводим ошибку в лог
    logging.info('Cервер запущен')  # Выводим в лог информацию о запуске сервера
    update_data()  # Запускаем функцию обновления данных
