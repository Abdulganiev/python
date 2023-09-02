from generating_report_files import *

# ********************************************************
log = 'requests_gis_gkh'
mail = 'IVAbdulganiev@yanao.ru'

# ********************************************************************
def count_table(): # проверка временной таблицы на наличие записей
  try:
    curs.execute('SELECT count(*) FROM uszn.temp$_gkv_gu')
    return int(curs.fetchall()[0][0])
  except:
    return 0

# ********************************************************
def drop_table(): # удаление временной таблицы
  cnt = count_table()
  if cnt > 0:
    curs.execute('DELETE FROM uszn.temp$_gkv_gu')

# ********************************************************
def creating_table(): # создание временное таблицы
  cnt = count_table()
  if cnt == 0:
        with open('requests_gis_gkh_create.sql', 'r', encoding='utf8') as f:
          sql = f.read()
          curs.execute(sql)

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
try:
  writing_to_log_file(log, '************************************************')
except Exception as e:
  text = f'произошла ошибка при вызове функции writing_to_log_file - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  curs = connect_oracle()
except Exception as e:
  text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  cnt1 = count_table()
except Exception as e:
  text = f'произошла ошибка при вызове функции count_table() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  drop_table()
except Exception as e:
  text = f'произошла ошибка при вызове функции drop_table() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  creating_table()
except Exception as e:
  text = f'произошла ошибка при вызове функции creating_table() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  cnt2 = count_table()
except Exception as e:
  text = f'произошла ошибка при вызове функции count_table() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  deleting_collection()
except Exception as e:
  text = f'произошла ошибка при вызове функции deleting_collection() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  loading_data_1()
except Exception as e:
  text = f'произошла ошибка при вызове функции loading_data_1() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  loading_data_2()
except Exception as e:
  text = f'произошла ошибка при вызове функции loading_data_2() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  loading_data_3()
except Exception as e:
  text = f'произошла ошибка при вызове функции loading_data_3() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  count_collection()
except Exception as e:
  text = f'произошла ошибка при вызове функции count_collection() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
text = f'{cnt1} записей до загрузки, {cnt2} записей после загрузки'

# ********************************************************
try:
  writing_to_log_file(log, text)
except Exception as e:
  text = f'произошла ошибка при вызове функции writing_to_log_file - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  send_email(mail, 'Коллекции для ГИС ЖКХ обновлены', msg_text=text)
except Exception as e:
  text = f'произошла ошибка при вызове функции send_email() - {e}'
  alarm_log(mail, log, text)