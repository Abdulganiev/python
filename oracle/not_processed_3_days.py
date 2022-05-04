import jaydebeapi
import json
from generating_report_files import *

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


#***************************************************************
def not_processed_3_days():
    curs.execute('''
    select
  '0'||t1.region_id||'-'||uszn.pkTSrv.GetRegionName(t1.region_id)||'-'||to_char(SysDate,'yyyy-mm-dd')||' - '||'не обработанные гос_услуги' as name,
  t1.region_id||'-'||t1.pc_id as pc_id, -- ID человека
  t1.pc_desc, -- Описание заявителя
  t1.id, -- ID заявления
  ' '||to_char(t1.date_created,'dd.mm.yyyy'), -- Дата подачи
  t1.state_service_name, -- Гос_услуга
  t1.status_name, -- Статус
  t1.sender_display_name -- Откуда пришло заявление
from
  uszn.all_ssvc_requests t1
  inner join
  uszn.all_state_services t2
on
  t1.region_id in (select id from uszn.tsrv_regions where owner_id=104 and id not in (71, 72) )
  and t1.state_svc_region_id=t2.region_id and t1.state_svc_id=t2.id
  and (sysdate-t1.date_created)>3 and t1.status_id in (1,2,10)
  and t1.date_created>to_date('01.01.2020')
  and t2.folder_region_id=104 and t2.folder_id=2''')
    
    data = {
         'name' : [],
         'ID человека' : [],
         'Описание человека' : [],
         'ID заявления' : [],
         'Дата подачи' : [],
         'Гос_услуга' : [],
         'Статус' : [],
         'Откуда пришло заявление' : [],
        }
    
    for row in curs.fetchall():
        data['name'].append(row[0])
        data['ID человека'].append(row[1])
        data['Описание человека'].append(row[2])
        data['ID заявления'].append(row[3])
        data['Дата подачи'].append(row[4])
        data['Гос_услуга'].append(row[5])
        data['Статус'].append(row[6])
        data['Откуда пришло заявление'].append(row[7])

    return data

#***************************************************************

data = not_processed_3_days()
name_log = 'not_processed_3_days'
name_def = 'Гос_услуги необработанные более 3 дней'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

generating_report_files(data, name_log, name_def, test, mail)
