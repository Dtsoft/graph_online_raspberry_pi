import time
import requests
import matplotlib.pyplot as plt

url_temp = 'http://192.168.22.220/sensors'  # Адрес страницы с сенсорами
url_pressure = 'http://192.168.22.123/sensors'  # Адрес страницы с сенсорами
temp = []  # Массив для хранения данных температуры
pressure = []  # Массив для записи данных о давлении
time_get = []
data_col = 60  # Количество данных для отображения графика
interval = 10  # Интервал обновления данных в секундах


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
        pressure.append(float(zapros_sensor(url_pressure, 4)))  # Добавляем время в массив
        check_len_data(temp)  # Проверяем длину массива и удаляем первый элемент если он больше нужного количества
        check_len_data(pressure)  # Проверяем длину массива и удаляем первый элемент если он больше нужного количества
        check_len_data(time_get)  # Проверяем длину массива и удаляем первый элемент если он больше нужного количества
        print(temp)
        print(pressure)
        plt.figure()
        fig, ax = plt.subplots(2, 1, figsize=(20, 15))
        plt.subplots_adjust(wspace=1, hspace=0.5)
        ax[0].set_title('Температура на улице')
        ax[0].plot(time_get, temp, 'r')
        ax[0].set_xlabel('Время')
        ax[0].tick_params(axis='x', labelrotation=90)
        ax[0].set_ylabel('Температура')
        ax[0].grid(True)


        ax[1].set_title('Атмосферное давление')
        ax[1].plot(time_get, pressure, 'b')
        ax[1].set_xlabel('Время')
        ax[1].tick_params(axis='x', labelrotation=90)
        ax[1].set_ylabel('Атмосферное давление')
        ax[1].grid(True)
        fig.savefig('static/image.png')  # Сохраняем график в файл
        plt.close(fig)  # Закрываем график

        # with open("temp.json", "w") as json_file:
        #     json.dump(temp, json_file)
        # with open("pressure.json", "w") as json_file:
        #     json.dump(pressure, json_file)
        time.sleep(interval)  # Приостанавливаем выполнение функции на интервал времени


if __name__ == '__main__':
    update_data()

