import pandas as pd
import os
from generating_report_files import *

#***************************************************************
log = 'VK_USVO'
mail = 'IVAbdulganiev@yanao.ru'
path = r'd:/python/schedule/vk_usvo/'
test = 0

#***************************************************************    
def vk_insert_temp(xl):
    table = 'uszn.temp$_vk_load_temp'
    columns = '(' + ', '.join(list(xl)) + ')'
    question = 'values(' + ', '.join(list('?' * len(list(xl)))) + ')'
    sql = f'INSERT INTO {table} {columns} {question}'
    
    writing_to_log_file(log, f'Загрузка данных в {table}')
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'В {table} перед загрузкой {cnt} записей')
    
    for data in xl.itertuples(index=False):
        curs.execute(f'{sql}', list(data))
    
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'В {table} после загрузки {cnt} записей')

#****************************************************************************************************
def zdrav_insert():
    table = 'uszn.temp$_vk_load'
    table_new = 'uszn.temp$_vk_new'
    
    writing_to_log_file(log, f'Добавление записей в таблицу {table} из таблицы {table_new}')
    
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в {table} до загрузки - {cnt}')

    curs.execute(f'''INSERT INTO {table} 
                     SELECT * FROM {table_new}''')
    
    curs.execute(f'SELECT count(*) FROM {table}')
    cnt = curs.fetchone()[0]
    writing_to_log_file(log, f'Количество записей в {table} после загрузки - {cnt}')

#***************************************************************    
def vk_new():
    table = 'uszn.temp$_vk_new'
    writing_to_log_file(log, f'Загрузка данных в {table}')
    try:
        curs.execute(f'DROP TABLE {table}')
    except:
        writing_to_log_file(log, f'Таблица {table} еще не создана')
    curs.execute(f'''CREATE TABLE {table} AS
                        SELECT t1.*
                         FROM uszn.temp$_vk_load_temp t1
                              LEFT JOIN uszn.temp$_vk_load t2
                         ON t1.SNILS = t2.SNILS
                         WHERE t2.SNILS is null order by to_number(t1.nom)''')
    try:
        curs.execute(f'SELECT count(*) FROM {table}')
        cnt = curs.fetchone()[0]
        writing_to_log_file(log, f'В {table} загружено {cnt} записей')
    except:
        cnt = 0
        writing_to_log_file(log, f'Таблица {table} еще не создана')
    
    if cnt > 0:
        uploading_data_uszn(f'''SELECT uszn.pkTSrv.GetRegionName(t.mo_id) as mo, 
                                       '0'||t.mo_id||' - Список кандидатов УСВО' as name,
                                       t.*
                                FROM {table} t order by to_number(t.nom)''')

        uploading_data_uszn(f'''SELECT uszn.pkTSrv.GetRegionName(t.mo_id) as mo, 
                                       '104 - Список кандидатов УСВО все' as name,
                                        t.*
                                FROM {table} t order by to_number(t.nom)''')

def uploading_data_uszn(sql):
    data = {
        'УСЗН' : [],
        'name' : [],
        'Номер' : [],
        'Фамилия' : [],
        'Имя' : [],
        'Отчество' : [],
        'Дата рождения' : [],
        'Наименование ДУЛ' : [],
        'Серия и номер' : [],
        'Кем выдан' : [],
        'Когда выдан' : [],
        'Код подразделения' : [],
        'Место рождения' : [],
        'Регион' : [],
        'Муниципальное образование' : [],
        'Полный адрес' : [],
        'СНИЛС' : [],
        'ИНН' : [],
        'Дата заключения контракта' : [],
        'Срок заключения контракта' : [],
        'ВК ЯНАО - Дата постановки' : [],
        'ВК ЯНАО - Дата снятия' : [],
        'ВК ЯНАО - Место (муниципальное образование) постановки на воинский учет' : [],
        'Единовременная выплата в размере' : [],
        'Единовременная выплата на приобретение вещевого имущества' : [],
        'Возмещение расходов стоимости проезда от места жительства (пребывания) на территории ЯНАО' : [],
        'Наименование банка' : [],
        'БИК банк' : [],
        'Номер счета' : [],
        'Контактные данные' : [],
        'ID района' : [],
            }
    curs.execute(sql)
    for row in curs.fetchall():
        data['УСЗН'].append(row[0]),
        data['name'].append(row[1]),
        data['Номер'].append(row[2]),
        data['Фамилия'].append(row[3]),
        data['Имя'].append(row[4]),
        data['Отчество'].append(row[5]),
        data['Дата рождения'].append(row[6]),
        data['Наименование ДУЛ'].append(row[7]),
        data['Серия и номер'].append(row[8]),
        data['Кем выдан'].append(row[9]),
        data['Когда выдан'].append(row[10]),
        data['Код подразделения'].append(row[11]),
        data['Место рождения'].append(row[12]),
        data['Регион'].append(row[13]),
        data['Муниципальное образование'].append(row[14]),
        data['Полный адрес'].append(row[15]),
        data['СНИЛС'].append(row[16]),
        data['ИНН'].append(row[17]),
        data['Дата заключения контракта'].append(row[18]),
        data['Срок заключения контракта'].append(row[19]),
        data['ВК ЯНАО - Дата постановки'].append(row[20]),
        data['ВК ЯНАО - Дата снятия'].append(row[21]),
        data['ВК ЯНАО - Место (муниципальное образование) постановки на воинский учет'].append(row[22]),
        data['Единовременная выплата в размере'].append(row[23]),
        data['Единовременная выплата на приобретение вещевого имущества'].append(row[24]),
        data['Возмещение расходов стоимости проезда от места жительства (пребывания) на территории ЯНАО'].append(row[25]),
        data['Наименование банка'].append(row[26]),
        data['БИК банк'].append(row[27]),
        data['Номер счета'].append(row[28]),
        data['Контактные данные'].append(row[29]),
        data['ID района'].append(row[30])
    
    generating_report_files(data, log, log, test, mail)

#****************************************************************************************************
try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, log, text)

#****************************************************************************************************
writing_to_log_file(log, '***************************************')
cnt_file = 0
os.chdir(path)
c = os.listdir(os.getcwd())
for file in c:
    if file.endswith(".xlsx") or file.endswith(".xltx"):
        writing_to_log_file(log, f'Файл поступил - {file}')
        xl = write_file(file, log)
        try:
            backup_file(test, file, log, log)
        except Exception as e:
            text = f'произошла ошибка при вызове функции backup_file() - {e}'
            alarm_log(mail, log, text)
        cnt_file += 1

if cnt_file > 0:
    col = ['NOM', 'F', 'I', 'O', 'DR', 
           'DUL_TYPE', 'DUL_SER_NOM', 'DUL_KEM', 'DUL_DATE', 'DUL_PLACE', 'DUL_CODE',
           'ADR_REGION', 'ADR_MO', 'ADR_FULL',
           'SNILS', 'INN', 'CONTRACT_DATE', 'CONTRACT_PERIOD', 'VK_DATE_START', 'VK_DATE_END', 'VK_MO',
           'MSP_SINGLE', 'MSP_GOODS', 'MSP_TRAVEL', 'BANK_NAME', 'BANK_BIC', 'BANK_ACCOUNT', 'CONTACTS']
    xl.columns = col
    xl['DR'] = xl['DR'].apply(dat)
    xl['DUL_DATE'] = xl['DUL_DATE'].apply(dat)
    xl['VK_DATE_START'] = xl['VK_DATE_START'].apply(dat)
    xl['VK_DATE_END'] = xl['VK_DATE_END'].apply(dat)
    xl['VK_DATE_END'] = xl['VK_DATE_END'].apply(replace_nan)
    xl['MO_ID'] = xl['ADR_MO'].apply(mo_id)
    xl['INN'] = xl['INN'].apply(num_to_str)
    xl['BANK_BIC'] = xl['BANK_BIC'].apply(num_to_str)
    xl['BANK_ACCOUNT'] = xl['BANK_ACCOUNT'].apply(num_to_str)
    
    xl = xl.fillna('')
    
    if xl.iloc[0][0] != 1:
        xl.drop(index=list(range(0, xl['NOM'][xl['NOM'] == 1].index.tolist()[0])), inplace = True)
    
    vk_insert_temp(xl)
    vk_new()
    zdrav_insert()