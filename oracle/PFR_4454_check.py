import pandas as pd
import os
from datetime import datetime
import datetime as dt
from generating_report_files import *

pd.options.mode.chained_assignment = None

# *************************************************
log = 'prf_4454'
mail = 'IVAbdulganiev@yanao.ru'
path_backup = r'd:/python/schedule/backup/PFR_4454_check/'
path = 'd:/python/schedule/prf_4454'
name_def = 'prf_4454'
today = datetime.now().strftime('%d.%m.%Y')
test = 0
a = 0

# *************************************************
def load_files():
    writing_to_log_file(log, '***********start****************************')
    a = 0
    c = os.listdir(path)
    for file in c:
        writing_to_log_file(log, f'Файл поступил - {file}')
        if file.endswith('.zip'):
            writing_to_log_file(log, f'распаковка {file}')
            with zipfile.ZipFile(path + '/' + file) as zf:
                zf.extractall(path)
            writing_to_log_file(log, f'удаление {file}')
            os.remove(path + '/' + file)        

    writing_to_log_file(log, '********обработка файлов********')
    c = os.listdir(path)
    for file in c:
        writing_to_log_file(log, f'обработка файла - {file}')
        if file.endswith('.xlsx'):
            a += 1
            xl = pd.read_excel(path + '/' + file)
            writing_to_log_file(log, f'Файл {file} записан в dataframe')
            
            try:
                load_base(xl, a)
            except Exception as e:
                text = f'произошла ошибка при вызове функции load_base() - {e} - {file} - {a}'
                alarm_log(mail, log, text)

            # try:
            backup_file(test, file, log, name_def, path_backup)
            writing_to_log_file(log, f'Файл {file} в backup')
            # except Exception as e:
            #     text = f'произошла ошибка при вызове функции backup_file_pfr_4454() - {e} - {file} - {a}'
            #     alarm_log(mail, log, text)


        elif file.endswith('.csv'):
            a += 1
            xl = pd.read_csv(path + '/' + file, sep=';' , encoding='cp1251')
            writing_to_log_file(log, f'Файл {file} записан в dataframe')
            
            try:
                load_base(xl, a)
            except Exception as e:
                text = f'произошла ошибка при вызове функции load_base() - {e} - {file} - {a}'
                alarm_log(mail, log, text)
            
            # try:
            backup_file(test, file, log, name_def, path_backup)
            writing_to_log_file(log, f'Файл {file} в backup')
            # except Exception as e:
            #     text = f'произошла ошибка при вызове функции backup_file_pfr_4454() - {e} - {file} - {a}'
            #     alarm_log(mail, log, text)

# *************************************************            
def load_base(xl, v):
    nabor = ['Код региона устан ЕП', 'Дата решения о назначении', 
             'СНИЛС получателя ЕП', 'Фамилия получателя ЕП', 'Имя получателя ЕП', 'Отчество получателя ЕП', 
             'Дата рождения получателя ЕП', 
             'СНИЛС лица основания ЕП', 'Фамилия лица основания ЕП', 'Имя лица основания ЕП', 'Отчество лица основания ЕП', 
             'Дата рождения лица основания ЕП', 
             'Период,на который установено ЕП С', 'Период,на который установено ЕП ПО', 'Размер назначения ЕП', 
             'Код региона прекращения МСЗ', 'Код ОНМСЗ', 'Код меры', 'Наименование меры']
    
    xl = xl[nabor]
    xl['Дата решения о назначении'] = xl['Дата решения о назначении'].apply(dat)
    xl['Дата рождения получателя ЕП'] = xl['Дата рождения получателя ЕП'].apply(dat)
    xl['Дата рождения лица основания ЕП'] = xl['Дата рождения лица основания ЕП'].apply(dat)
    xl['Дата рождения лица основания ЕП'] = xl['Дата рождения лица основания ЕП'].apply(replace_nat)
    xl['СНИЛС получателя ЕП'] = xl['СНИЛС получателя ЕП'].apply(snils)
    xl['СНИЛС лица основания ЕП'] = xl['СНИЛС лица основания ЕП'].apply(snils)
    xl['Период,на который установено ЕП С'] = xl['Период,на который установено ЕП С'].apply(dat)
    xl['Период,на который установено ЕП ПО'] = xl['Период,на который установено ЕП ПО'].apply(dat)
    xl['Код УСЗН'] = xl['Код ОНМСЗ'].apply(kod_sfr_uszn_id)
    xl['Наименование УСЗН'] = xl['Код ОНМСЗ'].apply(kod_sfr_uszn_name)

    xl.fillna('', inplace=True)
    current_date = dt.datetime.now().date()
    mo_range = range(58,71)
    names = set()
    
    for i in mo_range:
        name = '0' + str(i) + '_pfr_posobie_' + str(current_date) + f'_{v}.xlsx'
        xl[xl['Код УСЗН'].isin([i])].to_excel(name, index=False)
        names.add(name)
    
    for file in names:
        movi_vipnet(test, file, log, name_def)
        writing_to_log_file(log, f'файл {file} отправлен в УСЗН')
    
# *************************************************
try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, log, text)

# try:
load_files()
# except Exception as e:
#     text = f'произошла ошибка при вызове функции load_files() - {e}'
#     alarm_log(mail, log, text)