from generating_report_files import *

# *****************************************************************
log = 'report_GKV_MO_mm_itog'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

# *****************************************************************
curs = connect_oracle()

# *****************************************************************
def GKH(region_id):
    with open('report_GKV_MO_mm_itog.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    sql = sql.replace('{region_id}', f'{region_id}')
    curs.execute(sql)
    return curs.fetchall()

# *****************************************************************
def report_GKV_name():
    curs.execute("select to_char(TRUNC(ADD_MONTHS(SYSDATE,-1),'MM'), 'mm.yyyy') from dual")
    return curs.fetchone()

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
        
# *****************************************************************
period = report_GKV_name()[0]
name = f'отчет ЖКВ за {period} в разрезе МО'

if test == 0:
    mail = 'IVAbdulganiev@yanao.ru, OVKolpakova@yanao.ru, NMShcherbinina@yanao.ru'

generating_report_GKV(data, log, name, mail)