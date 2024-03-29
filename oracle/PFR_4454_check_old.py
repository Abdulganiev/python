import pandas as pd
import re, os
from datetime import datetime
import datetime as dt
from generating_report_files import *

pd.options.mode.chained_assignment = None

# *************************************************
log = 'prf_4454'
mail = 'IVAbdulganiev@yanao.ru'
path = 'd:\\python\\schedule\\prf_4454\\'
name_def = 'prf_4454'
test = 0
today = datetime.now().strftime('%d.%m.%Y')

# *************************************************
def load_files():
    a = 0

    c = os.listdir(path)
    for file in c:
        writing_to_log_file(log, '***************************************')
        writing_to_log_file(log, f'Файл поступил - {file}')
        if file.endswith('.zip'):
            with zipfile.ZipFile(path + '\\' + file) as zf:
                zf.extractall(path)
            os.remove(path + '\\' + file)
    
    c = os.listdir(path)
    for file in c:
        writing_to_log_file(log, f'Файл поступил - {file}')
        if file.endswith('.xlsx'):
            xl = pd.read_excel(path + '\\' + file)
            writing_to_log_file(log, f'Файл {file} записан в dataframe')
            
            try:
                a = load_base(xl)
            except Exception as e:
                text = f'произошла ошибка при вызове функции load_base() - {e}'
                alarm_log(mail, log, text)
            
            try:
                movi_file(file)
            except Exception as e:
                text = f'произошла ошибка при вызове функции movi_file() - {e}'
                alarm_log(mail, log, text)
        
        elif file.endswith('.csv'):
            xl = pd.read_csv(path + '\\' + file, sep=';' , encoding='cp1251')
            writing_to_log_file(log, f'Файл {file} записан в dataframe')
            
            try:
                a = load_base(xl)
            except Exception as e:
                text = f'произошла ошибка при вызове функции load_base() - {e}'
                alarm_log(mail, log, text)
            
            try:
                movi_file(file)
            except Exception as e:
                text = f'произошла ошибка при вызове функции movi_file() - {e}'
                alarm_log(mail, log, text)

    return a

# *************************************************            
def load_base(xl):
    table = 'uszn.temp$_pfr_check'
    nabor = ['СНИЛС получателя ЕП', 'Фамилия получателя ЕП', 'Имя получателя ЕП', 'Отчество получателя ЕП',
             'Дата рождения получателя ЕП', 
             'СНИЛС лица основания ЕП', 'Фамилия лица основания ЕП', 'Имя лица основания ЕП',
             'Отчество лица основания ЕП', 'Дата рождения лица основания ЕП',
             'Дата решения о назначении',
             'Период,на который установено ЕП С', 'Период,на который установено ЕП ПО', 'Размер назначения ЕП']
    xl = xl[nabor]
    xl['Дата решения о назначении'] = xl['Дата решения о назначении'].apply(dat)
    xl['Дата рождения получателя ЕП'] = xl['Дата рождения получателя ЕП'].apply(dat)
    xl['Дата рождения лица основания ЕП'] = xl['Дата рождения лица основания ЕП'].apply(dat)
    xl['Дата рождения лица основания ЕП'] = xl['Дата рождения лица основания ЕП'].apply(replace_nat)
    xl['СНИЛС получателя ЕП'] = xl['СНИЛС получателя ЕП'].apply(snils)
    xl['СНИЛС лица основания ЕП'] = xl['СНИЛС лица основания ЕП'].apply(snils)
    xl['DT'] = today
    xl['DT'] = xl['DT'].apply(dat)
    xl['Период,на который установено ЕП С'] = xl['Период,на который установено ЕП С'].apply(dat)
    xl['Период,на который установено ЕП ПО'] = xl['Период,на который установено ЕП ПО'].apply(dat)

    xl.fillna('', inplace=True)

    writing_to_log_file(log, '*******************************************')    
    writing_to_log_file(log, f'Загрузка данных в {table}')
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в {table} перед загрузкой - {cnt}')
    a = 0

    curs.execute('delete from uszn.temp$_pfr_check')

    for data in xl.itertuples(index=False):
        try:
            curs.execute(f'''INSERT INTO {table} (app_date, app_snils, app_F, app_I, app_O, app_DR, baby_snils, baby_F, baby_I, baby_O, baby_DR, decision_date, decision, decision_status, date_from, date_to, amount, date_upload) 
                values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', 
                #          [data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], 
                #           data[11], data[12], data[13], data[14], data[15], data[16], data[17]])
                            ['', data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], 'Назначить', 'Назначить', 
                             data[10], data[11], data[12], data[13], data[14]])
            a += 1
        except Exception as e:
            text = f'произошла ошибка - {e}'
            alarm_log(mail, log, text)

    curs.execute('''insert into uszn.temp$_pfr_check_temp
                        select * from uszn.temp$_pfr_check''')
    return a

# *************************************************
def pfr_check():
    with open('PFR_4454_check.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

# *************************************************
def movi_file(file):
    new_file_name = f'{today} - {file}'
    os.replace(path + '\\' + file, f'd:\\python\\schedule\\backup\\{new_file_name}')
    writing_to_log_file(log, f'Файл {file} перемещен в backup и переименован в {new_file_name}')    

# *************************************************
# a = 0

try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, log, text)

a = load_files()

if a > 0:
    try:
        d = pfr_check()
    except Exception as e:
        text = f'произошла ошибка при вызове функции pfr_check() - {e}'
        alarm_log(mail, log, text)


    data = {
        'Дата решения о назначении ЕП' : [],
        'СНИЛС получателя ЕП' : [],
        'Фамилия получателя ЕП' : [],
        'Имя получателя ЕП' : [],
        'Отчество получателя ЕП' : [],
        'Дата рождения получателя ЕП' : [],
        'СНИЛС (лица - основания) ЕП' : [],
        'Фамилия (лица - основания) ЕП' : [],
        'Имя (лица - основания) ЕП' : [],
        'Отчество (лица - основания) ЕП' : [],
        'Дата рождения (лица - основания) ЕП' : [],
        'Период, на который установлено ЕП С' : [],
        'Период, на который установлена ЕП По' : [],
        'Размер назначения ЕП' : [],
        'Вид выплаты в УСЗН' : [],
        'name' : []
        }

    for row in d:
        data['Дата решения о назначении ЕП'].append(row[0])
        data['СНИЛС получателя ЕП'].append(row[1])
        data['Фамилия получателя ЕП'].append(row[2])
        data['Имя получателя ЕП'].append(row[3])
        data['Отчество получателя ЕП'].append(row[4])
        data['Дата рождения получателя ЕП'].append(row[5])
        data['СНИЛС (лица - основания) ЕП'].append(row[6])
        data['Фамилия (лица - основания) ЕП'].append(row[7])
        data['Имя (лица - основания) ЕП'].append(row[8])
        data['Отчество (лица - основания) ЕП'].append(row[9])
        data['Дата рождения (лица - основания) ЕП'].append(row[10])
        data['Период, на который установлено ЕП С'].append(row[11])
        data['Период, на который установлена ЕП По'].append(row[12])
        data['Размер назначения ЕП'].append(row[13])
        data['Вид выплаты в УСЗН'].append(row[14])
        data['name'].append(row[15])

    generating_report_files(data, log, name_def, test, mail)
else:
    text = f'файла нет'
    alarm_log(mail, log, text)
