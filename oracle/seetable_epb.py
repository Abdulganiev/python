from seatable_api import Base, context
from seatable_api.constants import UPDATE_DTABLE
import pandas as pd
from generating_report_files import *

#***************************************************************
name_log = 'seetable_epb'
name_def = 'seetable_epb'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
server_url = 'https://table.yanao.ru/'

see_code = {
    104 : ['Table1', '1b70f02f2f4736b509968dc96a9b859d09e8226b', 'uszn.temp$_EPB_see'],
        }

#***************************************************************
def seetable_epb(server_url, list_row, api_token):
    base = Base(api_token, server_url)
    # base.auth(with_socket_io=True)
    base.auth()
    
    data = {
        'nom' : [],
        'Муниципальное образование' : [],
        'СНИЛС в формате ХХХ-ХХХ-ХХХ ХХ' : [],
        }

    for row in base.list_rows(list_row):
        data['nom'].append(row.get('номер'))
        data['Муниципальное образование'].append(row.get('Муниципальное образование'))
        data['СНИЛС в формате ХХХ-ХХХ-ХХХ ХХ'].append(row.get('СНИЛС в формате ХХХ-ХХХ-ХХХ ХХ'))
        
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

    col = ['nom', 'mo', 'snils']
    xl.columns = col

    xl['nom'] = xl['nom'].apply(replace_nan)
    xl['snils'] = xl['snils'].apply(replace_nan)
    xl['mo'] = xl['mo'].apply(num_int_to_str)
    xl['mo'] = xl['mo'].apply(staples)
    xl['mo'] = xl['mo'].apply(replace_nan)


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

    columns = '(' + 'nom, mo, snils' + ')'
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
goto_folder()

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
        df = seetable_epb(server_url, list_row, api_token)
        flag = 0
    except Exception as e:
        text = f'произошла ошибка при вызове функции seetable_epb() - {e}'
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