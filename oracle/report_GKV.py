import pandas as pd
import jaydebeapi
import json
import datetime as dt
import os
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

def GKH(region_id):
    with open('report_GKV_MO.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{region_id}', f'{region_id}')
    curs.execute(sql)
    return curs.fetchall()

data = {
         'Название МО' : [] ,
         'Всего' : [] ,
         'в том числе льготники' : [] ,
         'площадь' : []             
        }

for region_id in range(58, 71):
    d = GKH(region_id)
    for row in d:
        data['Название МО'].append(row[1])
        data['Всего'].append(row[2])
        data['в том числе льготники'].append(row[3])
        data['площадь'].append(row[4])
        
df = pd.DataFrame(data)
    
today = dt.date.today()
first = today.replace(day=1)
lastMonth = first - dt.timedelta(days=1)
date_report = lastMonth.strftime('%m.%Y')
    
file_name = f'отчет ЖКВ за {date_report} в разрезе МО'+ '.xlsx'
df.to_excel(file_name, index=False)

mail = 'IVAbdulganiev@yanao.ru, MSNesteruk@yanao.ru'
# mail = 'IVAbdulganiev@yanao.ru'


send_email(mail, f'{file_name} на {today}', msg_text='', files=[file_name])

new_file_name = f'{today} - {file_name}'

os.replace(file_name, f'backup/{new_file_name}') 