import pandas as pd
import os, sys
from datetime import datetime
import datetime as dt
import jaydebeapi
import json
from samohod_v1 import *
from samohod_v2 import *
from smtp import *

path = "access_report.txt"
with open(path) as f:
    access = json.load(f)
    
driver = 'ojdbc14.jar'
path_base = access['path_base']
password = access['password']
login = access['login']
port = access['port']
sid = access['sid']

conn = jaydebeapi.connect(
    'oracle.jdbc.driver.OracleDriver',
    f'jdbc:oracle:thin:{login}/{password}@{path_base}:{port}/{sid}',
    [login, password],
    driver)

curs = conn.cursor()

c = os.listdir(os.getcwd())
for fil in c:
    if fil.endswith(".xlsx") or fil.endswith(".xltx"):
        file = fil
        writing_to_log_file(f'Файл поступил - {file}')
    else:
        file = '0'

if len(file) > 1:

    xl = pd.read_excel(file)

    cnt = 0
    x = 0
    for data in xl.itertuples(index=False):
        if cnt == 2:
            if data[0] == 'Гос. рег. знак' and data[1] == 'Марка' and data[2] == 'Наименование' and data[3] == 'Дата регистрации' and data[4] == 'Год вып.' and data[5] == 'Владелец' and data[6] == 'Адрес владельца' and data[7] == 'Документ, удост. личность' and data[8] == 'Кем выдан док. удост. личность' and data[9] == 'Дата выдачи док. удост. личность' and data[10] == 'Дата рождения':
                v2_drop(conn)
                v2_insert(conn, xl)
                v2_table_all(conn)
                v2_table_del(conn)
                v2_table_new(conn)
                v2_table_chahge(conn)
                v2_table_update(conn)
                v2_table_insert(conn)
            elif data[0] == 'Гос. рег. знак' and data[1] == 'Марка' and data[2] == 'Наименование' and data[3] == 'Год вып.' and data[4] == 'Владелец' and data[5] == 'Адрес владельца' and data[6] == 'Документ, удост. личность' and data[7] == 'Кем выдан док. удост. личность' and data[8] == 'Дата выдачи док. удост. личность' and data[9] == 'Дата рождения' and data[10] == 'Дата регистрации':
                v1_drop(conn)
                v1_insert(conn, xl)
                v1_table_all(conn)
                v1_table_del(conn)
                v1_table_new(conn)
                v1_table_chahge(conn)
                v1_table_update(conn)
                v1_table_insert(conn)
            else:    
                writing_to_log_file('ВНИМАНИЕ!!! Ошибки в полях')
                text = f'Файл от службы на {file} содержит ошибки в полях'
                send_email('IVAbdulganiev@yanao.ru', 'ВНИМАНИЕ!!! Файл от службы - ошибки в полях', msg_text=text, files=[])
                
                today = dt.date.today()
                new_file_name = f'{today} - {file}'
                os.replace(file, f'backup/{new_file_name}')
                writing_to_log_file(f'Файл {file} перемещен в backup и переименован в {new_file_name}')
                exit()
        cnt += 1

    today = dt.date.today()
    new_file_name = f'{today} - {file}'

    os.replace(file, f'backup/{new_file_name}')

    writing_to_log_file(f'Файл {file} перемещен в backup и переименован в {new_file_name}')

    send_email('IVAbdulganiev@yanao.ru', f'Файл от службы на {today} обработан', msg_text=file, files=[])
else:
    writing_to_log_file('Файла нет')
    send_email('IVAbdulganiev@yanao.ru', f'Файл от службы на {today} не пришел', msg_text='', files=[])