import os
from datetime import datetime


def writing_to_log_file(file, text):
    # '''функция создания лог файла и записи в него информации'''
    dt = datetime.now().strftime('%Y-%m-%d %X')
    log_file = file + '.log'
    path = 'log/' + log_file
    # print(text)
    with open(path, 'a+') as file_log:
        file_log.write(dt + ' : ' + text + '\n')