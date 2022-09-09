import time
import requests
import matplotlib.pyplot as plt
import subprocess

url_temp = 'http://192.168.22.220/sensors'  # Адрес страницы с сенсорами
url_pressure = 'http://192.168.22.123/sensors'  # Адрес страницы с сенсорами
temp = []  # Массив для хранения данных температуры
temp_k = []
pressure = []  # Массив для записи данных о давлении
time_get = []
data_col = 60  # Количество данных для отображения графика
interval = 600  # Интервал обновления данных в секундах


def zapros_sensor(url_link, num):  # Функция для запроса данных с сенсора
    zapros = requests.get(url_link)  # Делаем запрос на адрес url
    out = zapros.text.split(';')[num].split(':')[1]  # Полученный текст запроса разбиваем на массив по ; и
    # берем нужны параметр. Параметр разбиваем на имя поля и значение по точке с запятой
    return out  # Возвращаем значение полученного параметра


def check_len_data(spisok):
    if len(spisok) > data_col:
        spisok.pop(0)
    return spisok


def update_data():  # Функция для обновления данных
    global temp, pressure  # Объявляем глобальные переменные
    while True:
        time_get.append(time.strftime('%H:%M:%S'))  # Получаем время
        temp.append(float(zapros_sensor(url_temp, 1)))  # Добавляем значение полученное из сенсора в массив
        temp_k.append(float(zapros_sensor(url_pressure, 6)))
        pressure.append(float(zapros_sensor(url_pressure, 4)))  # Добавляем время в массив
        check_len_data(temp)  # Проверяем длину массива и удаляем первый элемент если он больше нужного количества
        check_len_data(temp_k)  # Проверяем длину массива и удаляем первый элемент если он больше нужного количества
        check_len_data(pressure)  # Проверяем длину массива и удаляем первый элемент если он больше нужного количества
        check_len_data(time_get)  # Проверяем длину массива и удаляем первый элемент если он больше нужного количества
        print(temp)
        print(pressure)
        plt.figure(1, figsize=(20, 15), dpi=80)  # Создаем график и задаем размеры его по ширине и высоте
        # График температуры на улице
        plt.subplot(221)
        plt.subplots_adjust(hspace=0.3, left=0.05, right=0.95, top=0.95, bottom=0.05)
        plt.plot(time_get, temp, 'r-')  # Рисуем график и задаем цвет линии и тип линии
        plt.title('Температура на улице', fontsize=20)  # Задаем заголовок графика
        plt.xlabel('Время')  # Задаем название оси Х
        plt.ylabel('°C')  # Задаем название оси Y
        plt.grid(True)  # Включаем сетку
        plt.xticks(rotation=90)  # Поворачиваем ось Х
        # График температуры в комнате
        plt.subplot(222)
        plt.plot(time_get, temp_k, 'b-')
        plt.title('Температура в комнате', fontsize=20)  # Задаем заголовок графика
        plt.xlabel('Время')  # Задаем название оси Х
        plt.ylabel('°C')  # Задаем название оси Y
        plt.grid(True)  # Включаем сетку
        plt.xticks(rotation=90)  # Поворачиваем ось Х
        # График давления
        plt.subplot(212)
        plt.plot(time_get, pressure, 'g-')  # Рисуем график и задаем цвет линии и тип линии
        plt.title('Атмосферное давление', fontsize=20)  # Задаем заголовок графика
        plt.xlabel('Время')  # Задаем название оси Х
        plt.ylabel('мм.рт.ст')  # Задаем название оси Y
        plt.grid(True)  # Включаем сетку
        plt.xticks(rotation=90)  # Поворачиваем ось Х
        # plt.show()  # Показываем график
        plt.savefig('static/image.png')  # Сохраняем график в файл
	plt.clf()
        plt.close('all')  # Закрываем график
        time.sleep(interval)  # Приостанавливаем выполнение функции на интервал времени


if __name__ == '__main__':
    subprocess.Popen('python server1.py', shell=True)
    update_data()
