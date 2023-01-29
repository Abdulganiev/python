import pandas as pd
import os, re, openpyxl
import datetime as dt
from samohod_v1 import *
from samohod_v2 import *
from generating_report_files import *

#***************************************************************
log = 'samohod'
mail = 'IVAbdulganiev@yanao.ru'
today = dt.date.today()

#***************************************************************
def movi_file(file):
    new_file_name = f'{today} - {file}'
    os.replace(file, f'backup/{new_file_name}')
    writing_to_log_file(log, f'Файл {file} перемещен в backup и переименован в {new_file_name}')

#***************************************************************
def write_file(file):
    try:
        xl = pd.read_excel(file)
        writing_to_log_file(log, f'Файл {file} записан в dataframe')
        return xl
    except Exception as e:
        text = f'Alarm: \n {e}'
        alarm_log(mail, log, text)
    
#***************************************************************
def write_df(xl):
    cnt = 0
    for data in xl.itertuples(index=False):
        if cnt == 2:
            if data[0] == 'Гос. рег. знак' and data[1] == 'Марка' and data[2] == 'Наименование' and data[3] == 'Дата регистрации' and data[4] == 'Год вып.' and data[5] == 'Владелец' and data[6] == 'Адрес владельца' and data[7] == 'Документ, удост. личность' and data[8] == 'Кем выдан док. удост. личность' and data[9] == 'Дата выдачи док. удост. личность' and data[10] == 'Дата рождения':
                writing_to_log_file(log, 'Запуск вариант 2')
                # print('Запуск вариант 2')
                v2(xl)
            elif data[0] == 'Гос. рег. знак' and data[1] == 'Марка' and data[2] == 'Наименование' and data[3] == 'Год вып.' and data[4] == 'Владелец' and data[5] == 'Адрес владельца' and data[6] == 'Документ, удост. личность' and data[7] == 'Кем выдан док. удост. личность' and data[8] == 'Дата выдачи док. удост. личность' and data[9] == 'Дата рождения' and data[10] == 'Дата регистрации':
                writing_to_log_file(log, 'Запуск вариант 1')
                # print('Запуск вариант 1')
                v1(xl)
            elif data[0] == 'Гос. рег. знак' and data[1] == 'Марка' and data[2] == 'Наименование' and data[3] == 'Дата регистрации' and data[4] == 'Год вып.' and data[5] == 'Владелец' and data[6] == 'Адрес владельца' and data[7] == 'Документ, удост. личность' and data[8] == 'Кем выдан док. удост. личность' and data[9] == 'Дата выдачи док. удост. личность' and data[10] == 'СНИЛС' and data[11] == 'Дата рождения':
                writing_to_log_file(log, 'Запуск вариант 3')
                # print('Запуск вариант 3')
                xl.drop('Unnamed: 10', axis=1, inplace=True)
                xl.rename(columns={'Unnamed: 11': 'Unnamed: 10'}, inplace=True)
                v2(xl)
            else:    
                writing_to_log_file(log, 'ВНИМАНИЕ!!! Ошибки в полях')
                text = f'Файл от службы на {file} содержит ошибки в полях'
                send_email(mail, 'ВНИМАНИЕ!!! Файл от службы - ошибки в полях', msg_text=text, files=[])
                movi_file(file)
                exit()
            break
        cnt += 1

#***************************************************************
writing_to_log_file(log, '***************************************')

c = os.listdir(os.getcwd())
for file in c:
    if file.endswith(".xlsx") or file.endswith(".xltx"):
        writing_to_log_file(log, '***************************************')
        writing_to_log_file(log, f'Файл поступил - {file}')
        wb = openpyxl.load_workbook(file)
        wb.save(file)
        # print(file)
        xl = write_file(file)
        write_df(xl)
        movi_file(file)
        send_email(mail, f'Файл от службы на {today} обработан', msg_text=file, files=[])