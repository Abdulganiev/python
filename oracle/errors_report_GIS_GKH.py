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
def errors_report__GIS_GKH():
        
    curs.execute('''
select
  '0'||r.region_id||' - '||uszn.pkTSrv.GetRegionName(r.region_id)||' ошибки при отправке в ГИС ЖКХ в '||to_char(sysdate, 'yyyy-mm') as name,
  r.region_id||'-'||r.request_subject_id as pc_id,
  trim(
  uszn.pkPerson.GetDocReqValue(r.region_id, 18410, r.request_pdoc_id)||' '||
  uszn.pkPerson.GetDocReqValue(r.region_id, 18411, r.request_pdoc_id)||' '||
  uszn.pkPerson.GetDocReqValue(r.region_id, 18412, r.request_pdoc_id)) as FIO,
  uszn.pkPerson.GetDocReqValue(r.region_id, 18415, r.request_pdoc_id) as adr,
  r.status_message
from
  uszn.all_interdept_requests r
where
  r.region_id in (select id from uszn.v_filter_regions_down where filter_region_id=104) and
  r.date_created between trunc(sysdate, 'mm') and trunc(sysdate, 'dd')-10 and
  (r.data_kind_region_id,r.data_kind_id) in ((0,71)) and
  r.status_id in (7,5)''')
    
    data = {
         'name' : [],
         'id человека' : [] ,
         'ФИО и д.р' : [] ,
         'Адрес' : [] ,
         'Ошибка' : [],
        }
    
    for row in curs.fetchall():
        data['name'].append(row[0])
        data['id человека'].append(row[1])
        data['ФИО и д.р'].append(row[2])
        data['Адрес'].append(row[3])
        data['Ошибка'].append(row[4])
    
    return data

#***************************************************************

data = errors_report__GIS_GKH()

name_log = 'errors_report__GIS_GKH'
name_def = 'Ошибки при отправке в ГИС ЖКХ'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

generating_report_files(data, name_log, name_def, test, mail)