from seatable_api import Base, context
from seatable_api.constants import UPDATE_DTABLE
import pandas as pd
from generating_report_files import *

#***************************************************************
name_log = 'seatable_noz'
name_def = 'seatable_noz'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
server_url = 'https://table.yanao.ru/'

see_code = {
    58 : ['058', '4a5a13b6814a409e084bb3ef26de55431ef910f0', 'uszn.temp$_inv_noz_058'],
    59 : ['059', '909b6d2004ea0a0384663984b1c0de025727772c', 'uszn.temp$_inv_noz_059'],
    60 : ['060', 'e07e8c7da93c577a2107bb09290dee46c191faf4', 'uszn.temp$_inv_noz_060'],
    61 : ['061', '66a1298f9cc8aefbc9d1ff472acf7876032f31cb', 'uszn.temp$_inv_noz_061'],
    62 : ['062', '4c9327883a77ff13a3167d1b6e89eadcbdc1eab0', 'uszn.temp$_inv_noz_062'],
    63 : ['063', '4f7c689821b2df446681734698af13b7ad42325c', 'uszn.temp$_inv_noz_063'],
    64 : ['064', 'b97caf4b50e3ea7a95cda52139adefd7b918363b', 'uszn.temp$_inv_noz_064'],
    65 : ['065', '2a2f63c5d5ed6c15ea8b67e50260c37a20ef9b80', 'uszn.temp$_inv_noz_065'],
    66 : ['066', '1fa4d09d12ea999760658bfef7534532070ca0e8', 'uszn.temp$_inv_noz_066'],
    67 : ['067', '9d62e0c2bf90a6ddd64e588661bb147a280f251a', 'uszn.temp$_inv_noz_067'],
    68 : ['068', '124764ab97200f2076f8f66896a7675fa9a885d7', 'uszn.temp$_inv_noz_068'],
    69 : ['069', '4992ad7f56f7952e22548647a105574e29eb99ba', 'uszn.temp$_inv_noz_069'],
    70 : ['070', '3786d7ccb561ad33290fb1931af6306218a439e8', 'uszn.temp$_inv_noz_070']
        }

#***************************************************************
def seetable_noz(server_url, list_row, api_token):
    base = Base(api_token, server_url)
    # base.auth(with_socket_io=True)
    base.auth()
    
    data = {
        'СНИЛС' : [],
        'id в исзн' : [],
        'ФИО и д.р.' : [],
        'Нозология' : [],
        'Обследована квартира' : [],
        'Приспособлена квартира' : [],
        'Предоставлена квартира' : [],
        'Обследовано общее имущ-во МКД' : [],
        'Приспособлено общее имущ-во МКД' : [],
        'Примечание' : [],
        }

    for row in base.list_rows(list_row):
        data['СНИЛС'].append(row.get('СНИЛС'))
        data['id в исзн'].append(row.get('id в исзн'))
        data['ФИО и д.р.'].append(row.get('ФИО и д.р.'))
        data['Нозология'].append(row.get('Нозология'))
        data['Обследована квартира'].append(row.get('Обследована квартира'))
        data['Приспособлена квартира'].append(row.get('Приспособлена квартира'))
        data['Предоставлена квартира'].append(row.get('Предоставлена квартира'))
        data['Обследовано общее имущ-во МКД'].append(row.get('Обследовано общее имущ-во МКД'))
        data['Приспособлено общее имущ-во МКД'].append(row.get('Приспособлено общее имущ-во МКД'))
        data['Примечание'].append(row.get('Примечание'))
        
    return pd.DataFrame(data)

#***************************************************************
def str_delete(table):
    writing_to_log_file(name_log, f'Удаление данных из {table}')
    curs.execute(f'delete from {table}')

#***************************************************************
def cnt_table(table):
    curs.execute(f'SELECT count(*) FROM {table}')
    return curs.fetchone()[0]

#***************************************************************
def str_insert(xl, table):
    writing_to_log_file(name_log, f'Начало загрузки данных в {table}')
    
    try:
        cnt = cnt_table(table)
    except Exception as e:
        text = f'произошла ошибка при вызове функции cnt_table() - {e}'
        alarm_log(mail, name_log, text)
    
    writing_to_log_file(name_log, f'В {table} перед загрузкой {cnt} записей')
    
    try:
        str_delete(table)
    except Exception as e:
        text = f'произошла ошибка при вызове функции str_delete() - {e}'
        alarm_log(mail, name_log, text)

    columns = '(' + 'snils, id, fio, noz, obsl_kv, prisp_kv, predst_kv, obsl_mkd, prisp_mkd, comments' + ')'
    question = 'values(' + ', '.join(list('?' * len(columns.split(',')))) + ')'
    sql = f'INSERT INTO {table} {columns} {question}'
    
    writing_to_log_file(name_log, f'Загрузка данных в {table}')
    
    for data in xl.itertuples(index=False):
        curs.execute(f'{sql}', list(data))
    
    try:
        cnt = cnt_table(table)
    except Exception as e:
        text = f'произошла ошибка при вызове функции cnt_table() - {e}'
        alarm_log(mail, name_log, text)

    writing_to_log_file(name_log, f'В {table} после загрузки {cnt} записей')

#***************************************************************
try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

#***************************************************************
writing_to_log_file(name_log, f'************** START **************')

for code, value in see_code.items():
    flag = 0
    list_row = value[0]
    api_token = value[1]
    table = value[2]
    
    writing_to_log_file(name_log, '-' * 10)
    writing_to_log_file(name_log, f'Загрузка {code} района')
    try:
        df = seetable_noz(server_url, list_row, api_token)
        flag = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции seetable_noz() - {e}'
        alarm_log(mail, name_log, text)
        flag = 1
    if flag == 0:
        try:
            str_insert(df, table)
            flag = 0
        except Exception as e:
            text = f'произошла ошибка при вызове функции str_insert() - {e}'
            alarm_log(mail, name_log, text)
            flag = 1
    if flag == 1:
        writing_to_log_file(name_log, f'Сбой загрузки {code} района')

writing_to_log_file(name_log, f'************** END ***************')