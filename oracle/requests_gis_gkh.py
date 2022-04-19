import jaydebeapi
import json
from datetime import datetime
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

def drop_table():
  cnt = count_table()
  if cnt > 0:
    curs.execute('DROP TABLE uszn.temp$_gkv_gu')

def creating_table():
  cnt = count_table()
  if cnt == 0:
    curs.execute(
    '''
CREATE TABLE uszn.temp$_gkv_gu
as
SELECT row_number() over(partition by t2.region_id ORDER BY t2.pc_id) as num,
       t2.region_id,
       t2.pc_id,
       max(t2.id) as id
             FROM uszn.all_po_amounts t1
                  INNER JOIN uszn.all_ssvc_requests t2
             ON t1.region_id not in (71, 72, 104)
                and t1.region_id=t2.region_id and t1.amount_payee_pc_id=t2.pc_id and
                   (t1.pka_kind_id, t1.pka_kind_region_id) in ((29,104)) and
                   t1.status_id in (103,107,104,101,102) and
                   t1.pka_is_enabled = 1 and t1.pka_status_num = 0 and
                   t1.poi_payout_date>=TRUNC(ADD_MONTHS(SYSDATE, -1), 'MM')
                   and (state_svc_id,state_svc_region_id) in ((20,104)) and
                   t2.status_id in (20, 30, 40) and
                   uszn.pkPerson.GetDeathDate(t2.region_id, t2.pc_id) is null and
                   uszn.pkPerson.GetCloseDate(t2.region_id, t2.pc_id) is null
GROUP BY t2.region_id, t2.pc_id''')  

def deleting_collection():
  curs.execute('''
DELETE uszn.r_ssvc_rq_collection_items
WHERE collection_id in (SELECT id 
                         FROM uszn.r_ssvc_request_collections 
                         WHERE name like 'ЖКВ-_')
    ''')

def loading_data():
  for region_id in range(58,71):
    for row in range(1,4):
      name_collection = f"'ЖКВ-{row}'"

      curs.execute(f'''
INSERT INTO uszn.r_ssvc_rq_collection_items(collection_id, collection_region_id, request_id, request_region_id)
    SELECT 
    distinct (SELECT v2.id 
        FROM uszn.r_ssvc_request_collections v2 
        WHERE v2.name={name_collection} and 
              v2.region_id=t1.region_id),
        t1.region_id, 
        t1.id, 
        t1.region_id
    FROM uszn.temp$_gkv_gu t1
    WHERE t1.region_id={region_id} and
          t1.num between 1 and (SELECT ceil(max(t2.num)/3) 
                                 FROM uszn.temp$_gkv_gu t2 
                                 WHERE t2.region_id=t1.region_id)''')

def count_table():
  try:
    curs.execute('SELECT count(*) from uszn.temp$_gkv_gu')
    return int(curs.fetchall()[0][0])
  except:
    return 0

def count_collection(conn):
  for region_id in range(58,71):
    for row in range(1,4):
      name_collection = f"'ЖКВ-{row}'"
      curs.execute(f'''
SELECT t1.id, 
       t1.name, 
       count(t2.request_id) as id
        FROM uszn.r_ssvc_request_collections t1
             inner join
             uszn.r_ssvc_rq_collection_items t2
        on t1.name = {name_collection} and
           t1.region_id = {region_id} and
           t1.id=t2.collection_id and
           t1.region_id=t2.collection_region_id
group by t1.id, name''')
      col_id, col_name, col_cnt = curs.fetchall()[0]
      with open(f'log/{log}', 'a') as f:
        f.write(f'id-{col_id}, {col_name} - {col_cnt} количество записей\n')

log = "requests_gis_gkh.log"
day = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

cnt1 = count_table()
drop_table()
creating_table()
cnt2 = count_table()
deleting_collection()
loading_data()

with open(f'log/{log}', 'a') as f:
    f.write('**************************************\n')
    f.write(f'{day} - {cnt1} записей до загрузки\n')
    f.write(f'{day} - {cnt2} записей после загрузки\n')

count_collection(conn)

send_email('IVAbdulganiev@yanao.ru', 'Коллекции для ГИС ЖКХ обновлены', msg_text=f'{day} - {cnt2} записей после загрузки\n')