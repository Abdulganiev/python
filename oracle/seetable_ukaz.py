from seatable_api import Base, context
from seatable_api.constants import UPDATE_DTABLE
import pandas as pd
from generating_report_files import *

#***************************************************************
name_log = 'seetable_ukaz'
name_def = 'seetable_ukaz'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
server_url = 'https://table.yanao.ru/'

see_code = {
    104 : ['Сбор информации', 'a13eaa38db91945377a02fdef7d95d9ef49a6e01', 'uszn.temp$_seetable_ukaz'],
    }

#***************************************************************
def seetable_ukaz(code, server_url, list_row, api_token):
    base = Base(api_token, server_url)
    # base.auth(with_socket_io=True)
    base.auth()
    
    data = {
        'СНИЛС' : [],
        'Сфера' : [],
        'МО' : [],
        'НП' : [],
        'Профессия ПП': [],
        'Профессия нет ПП' : [],
        'Телефон' : [],
        }

    for row in base.list_rows(list_row):
        data['СНИЛС'].append(row.get('СНИЛС в формате ХХХ-ХХХ-ХХХ ХХ'))
        data['Сфера'].append(row.get('Сфера'))
        data['МО'].append(row.get('Муниципальное образование'))
        data['НП'].append(row.get('Населенный пункт'))
        data['Профессия ПП'].append(row.get('Профессия по Постановлению № 117-П от 18-02-2016'))
        data['Профессия нет ПП'].append(row.get('Профессия, если нету в Постановлении'))
        data['Телефон'].append(row.get('Контактный телефон специалиста, который внес информацию'))
        
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

    columns = '(' + 'snils, scope_ukaz, region_name, np, profession_pp, profession_not_pp, phone, region_id' + ')'
    question = 'values(' + ', '.join(list('?' * len(columns.split(',')))) + ')'
    sql = f'INSERT INTO {table} {columns} {question}'
    
    xl['Сфера'].apply(num_to_str).apply(replace_nan)
    xl['МО'].apply(num_to_str).apply(replace_nan)
    xl['НП'].apply(num_to_str).apply(replace_nan)
    xl['Профессия ПП'].apply(num_to_str).apply(replace_nan)
    xl['Профессия нет ПП'].apply(num_to_str).apply(replace_nan)
    xl['Телефон'].apply(num_to_str).apply(replace_nan)
    xl['MO_ID'] = xl['МО'].apply(mo_id)

    xl = xl.fillna('')
    xl = xl.fillna(0)

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
        df = seetable_ukaz(code, server_url, list_row, api_token)
        flag = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции seetable_ukaz() - {e} {code}'
        alarm_log(mail, name_log, text)
        flag = 1
    if flag == 0:
        try:
            str_insert(df, table)
            flag = 0
        except Exception as e:
            text = f'произошла ошибка при вызове функции str_insert() - {e} {df}'
            alarm_log(mail, name_log, text)
            flag = 1
    if flag == 1:
        writing_to_log_file(name_log, f'Сбой загрузки {code} района')

writing_to_log_file(name_log, f'************** END ***************')