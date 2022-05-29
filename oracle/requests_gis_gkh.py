from generating_report_files import *

# ********************************************************
def drop_table(): # удаление временной таблицы
  cnt = count_table()
  if cnt > 0:
    curs.execute('DROP TABLE uszn.temp$_gkv_gu')

# ********************************************************
def creating_table(): # создание временное таблицы
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

# ********************************************************
def deleting_collection():
  curs.execute('''
DELETE uszn.r_ssvc_rq_collection_items
WHERE collection_id in (SELECT id 
                         FROM uszn.r_ssvc_request_collections 
                         WHERE name like 'ЖКВ-_')''')

# ********************************************************
def loading_data_1():
  for region_id in range(58,71):
    name_collection = f"'ЖКВ-1'"

    curs.execute(f'''
INSERT INTO uszn.r_ssvc_rq_collection_items(collection_id, collection_region_id, request_id, request_region_id)
    SELECT 
    DISTINCT (SELECT v2.id 
        FROM uszn.r_ssvc_request_collections v2 
        WHERE v2.name={name_collection} and 
              v2.region_id=t1.region_id),
        t1.region_id, 
        t1.id, 
        t1.region_id
    FROM uszn.temp$_gkv_gu t1
    WHERE t1.region_id={region_id} and
    t1.num BETWEEN 1 and 
                   (SELECT ceil(max(t2.num)/3) FROM uszn.temp$_gkv_gu t2 WHERE t2.region_id=t1.region_id)''')

# ********************************************************************
def loading_data_2():
  for region_id in range(58,71):
    name_collection = f"'ЖКВ-2'"

    curs.execute(f'''
INSERT INTO uszn.r_ssvc_rq_collection_items(collection_id, collection_region_id, request_id, request_region_id)
    SELECT 
    DISTINCT (SELECT v2.id 
        FROM uszn.r_ssvc_request_collections v2 
        WHERE v2.name={name_collection} and 
              v2.region_id=t1.region_id),
        t1.region_id, 
        t1.id, 
        t1.region_id
    FROM uszn.temp$_gkv_gu t1
    WHERE t1.region_id={region_id} and
    t1.num BETWEEN (SELECT ceil(max(t2.num)/3)   FROM uszn.temp$_gkv_gu t2 WHERE t2.region_id=t1.region_id) + 1 and
                   (SELECT ceil(max(t2.num)/3)*2 FROM uszn.temp$_gkv_gu t2 WHERE t2.region_id=t1.region_id)''')

# ********************************************************************
def loading_data_3():
  for region_id in range(58,71):
    name_collection = f"'ЖКВ-3'"

    curs.execute(f'''
INSERT INTO uszn.r_ssvc_rq_collection_items(collection_id, collection_region_id, request_id, request_region_id)
    SELECT 
    DISTINCT (SELECT v2.id 
        FROM uszn.r_ssvc_request_collections v2 
        WHERE v2.name={name_collection} and 
              v2.region_id=t1.region_id),
        t1.region_id, 
        t1.id, 
        t1.region_id
    FROM uszn.temp$_gkv_gu t1
    WHERE t1.region_id={region_id} and
    t1.num between (SELECT ceil(max(t2.num)/3)*2 FROM uszn.temp$_gkv_gu t2 WHERE t2.region_id=t1.region_id) + 1 and
                   (SELECT max(t2.num)           FROM uszn.temp$_gkv_gu t2 WHERE t2.region_id=t1.region_id)''')

# ********************************************************************
def count_table(): # проверка временной таблицы на наличие записей
  try:
    curs.execute('SELECT count(*) FROM uszn.temp$_gkv_gu')
    return int(curs.fetchall()[0][0])
  except:
    return 0

# ********************************************************************
def count_collection():
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
      writing_to_log_file(log, f'{region_id}-{col_id}, {col_name} - {col_cnt} количество записей')

# ********************************************************

writing_to_log_file(log, '************************************************')
curs = connect_oracle()
cnt1 = count_table()
drop_table()
creating_table()
cnt2 = count_table()
deleting_collection()
loading_data_1()
loading_data_2()
loading_data_3()

log = 'requests_gis_gkh'
text = f'{cnt1} записей до загрузки, {cnt2} записей после загрузки'
mail = 'IVAbdulganiev@yanao.ru'

count_collection()

writing_to_log_file(log, text)
send_email(mail, 'Коллекции для ГИС ЖКХ обновлены', msg_text=text)