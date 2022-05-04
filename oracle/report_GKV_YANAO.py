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

with open('report_GKV_YANAO.sql', 'r', encoding='utf8') as f:
    sql = f.read()

# print(sql)

def report_GKV_YANAO(sql_cod):
    curs.execute(sql_cod)
    return curs.fetchall()

d = report_GKV_YANAO(sql)

data = {
         '№ п/п' : [],
         'Категории получателей мер социальной поддержки' : [],
         'Количество лиц, которым предоставлена социальная поддержка по оплате жилищно-коммунальных услуг (по сведениям органа государственной власти субъекта Российской Федерации), всего' : [],
         'в том числе носители льгот' : [],
         'Размер занимаемой общей площади' : [],
        }

cnt = 0
for el in range(1, len(d[0])+1):
    if el % 5 == 0 and el != 0:
        data['Размер занимаемой общей площади'].append(d[0][el-1])
        cnt = 0
    else:
        if cnt == 0:
            data['№ п/п'].append(d[0][el-1])
        elif cnt == 1:
            data['Категории получателей мер социальной поддержки'].append(d[0][el-1])
        elif cnt == 2:
            data['Количество лиц, которым предоставлена социальная поддержка по оплате жилищно-коммунальных услуг (по сведениям органа государственной власти субъекта Российской Федерации), всего'].append(d[0][el-1])
        elif cnt == 3:
            data['в том числе носители льгот'].append(d[0][el-1])
        cnt += 1
        
df = pd.DataFrame(data)

today = dt.date.today()
first = today.replace(day=1)
lastMonth = first - dt.timedelta(days=1)
date_report = lastMonth.strftime('%m.%Y')

file_name = f'отчет ЖКВ за {date_report} за ЯНАО.xlsx'

df.to_excel(file_name, index=False)

mail = 'IVAbdulganiev@yanao.ru, MSNesteruk@yanao.ru'
# mail = 'IVAbdulganiev@yanao.ru'

send_email(mail, f'{file_name} на {today}', msg_text='', files=[file_name])

new_file_name = f'{today} - {file_name}'

os.replace(file_name, f'backup/{new_file_name}') 
