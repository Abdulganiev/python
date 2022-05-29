from generating_report_files import *

# *****************************************************************
curs = connect_oracle()

# *****************************************************************
def GKH(region_id):
    with open('report_GKV_MO.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{region_id}', f'{region_id}')
    curs.execute(sql)
    return curs.fetchall()

# *****************************************************************
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
        
log = 'report_GKV_MO'
test = 0
name = 'в разрезе МО'

generating_report_GKV(data, log, name, test)