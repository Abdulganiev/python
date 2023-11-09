from seatable_api import Base, context
from seatable_api.constants import UPDATE_DTABLE
import pandas as pd
from generating_report_files import *

#***************************************************************
name_log = 'seetable_trud_stac'
name_def = 'seetable_trud_stac'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
server_url = 'https://table.yanao.ru/'

see_code = {
    58 : ['2023 год', 'c2955de42fc849512d88be0ffb52c3f734f5ffe7', 'uszn.temp$_trud_stac_58'],
    61 : ['2023 год', '41133f0005592075769dea9f4a74d7ed825d444d', 'uszn.temp$_trud_stac_61'],
    63 : ['2023 год', 'ab33db03623587635c9f61bb062d73c9458381d0', 'uszn.temp$_trud_stac_63'],
    66 : ['2023 год', '590bdb01d145c028d94f7790d28399af3f661135', 'uszn.temp$_trud_stac_66'],
    67 : ['2023 год', 'f0436340b58c154a204da1edae611b62703ddb25', 'uszn.temp$_trud_stac_67'],
    70 : ['2023 год', 'cf89ab7105a18cd383e681087d12135b674bd4a6', 'uszn.temp$_trud_stac_70'],
    72 : ['2023 год', 'd9f30b77293c68d6295106dd64425d69933f1c2d', 'uszn.temp$_trud_stac_72'],
    73 : ['2023 год', 'c5d0b04d6bfb76e564225e3d3e9b6b15857967e2', 'uszn.temp$_trud_stac_73'],        
    }

#***************************************************************
def seetable_trud_stac(code, server_url, list_row, api_token):
    base = Base(api_token, server_url)
    # base.auth(with_socket_io=True)
    base.auth()
    
    data = {
        'МО' : [],
        'Дата' : [],
        'Количество проживающих, чел' : [],
        'в отпуске, чел' : [],
        'на лечении, чел': [],
        'в том числе детей, чел' : [],
        }

    for row in base.list_rows(list_row):
        data['МО'].append(code)
        data['Дата'].append(row.get('Дата'))
        data['Количество проживающих, чел'].append(row.get('Количество проживающих, чел'))
        data['в отпуске, чел'].append(row.get('в отпуске, чел'))
        data['на лечении, чел'].append(row.get('на лечении, чел'))
        data['в том числе детей, чел'].append(row.get('в том числе детей, чел'))
        
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

    columns = '(' + 'region_id, date_info, count_resident, count_vacation, count_medicine, count_children' + ')'
    question = 'values(' + ', '.join(list('?' * len(columns.split(',')))) + ')'
    sql = f'INSERT INTO {table} {columns} {question}'
    
    xl['Дата'] = xl['Дата'].apply(dat)
    # xl['Дата'] = xl['Дата'].apply(num_to_str).apply(replace_nan)
    xl['Количество проживающих, чел'] = xl['Количество проживающих, чел'].apply(num_to_str).apply(replace_nan)
    xl['в отпуске, чел'] = xl['в отпуске, чел'].apply(num_to_str).apply(replace_nan)
    xl['на лечении, чел'] = xl['на лечении, чел'].apply(num_to_str).apply(replace_nan)
    xl['в том числе детей, чел'] = xl['в том числе детей, чел'].apply(num_to_str).apply(replace_nan)

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
        df = seetable_trud_stac(code, server_url, list_row, api_token)
        flag = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции seetable_trud_stac() - {e} {code}'
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