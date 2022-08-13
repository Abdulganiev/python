from generating_report_files import *

# ********************************************************
log = 'requests_200_GGS'
mail = 'IVAbdulganiev@yanao.ru'

# ********************************************************
def drop_table(): # удаление временной таблицы
  cnt = count_table()
  if cnt > 0:
    curs.execute('DROP TABLE uszn.temp$_200_GGS')

# ********************************************************
def creating_table(): # создание временное таблицы
  cnt = count_table()
  if cnt == 0:
    curs.execute(
    '''
CREATE TABLE uszn.temp$_200_GGS
as
SELECT row_number() over(partition by t2.region_id ORDER BY t2.pc_id) as num,
       t2.region_id,
       t2.pc_id,
       max(t2.id) as id
             FROM uszn.all_po_amounts t1
                  INNER JOIN uszn.all_ssvc_requests t2
             ON t1.region_id = 71
                and t1.region_id=t2.region_id and t1.amount_payee_pc_id=t2.pc_id and
                   (t1.pka_kind_id, t1.pka_kind_region_id) in ((89,104),(11,104),(51,104),(50,104),(80,104),(78,104),(81,104)) and
                   t1.status_id in (103,107,104,101,102) and
                   t1.pka_is_enabled = 1 and t1.pka_status_num = 0 and
                   t1.poi_payout_date>=TRUNC(ADD_MONTHS(SYSDATE, -1), 'MM')
                   and (state_svc_id,state_svc_region_id) in ((1,104),(9,104)) and
                   t2.status_id in (20, 30, 40)
GROUP BY t2.region_id, t2.pc_id''')  

# ********************************************************
def deleting_collection():
  curs.execute('''
DELETE uszn.r_ssvc_rq_collection_items
WHERE collection_id=1 and collection_region_id=71''')

# ********************************************************
def loading_data():
  curs.execute('''
INSERT INTO uszn.r_ssvc_rq_collection_items(collection_id, collection_region_id, request_id, request_region_id)
    SELECT 1, t1.region_id, t1.id, t1.region_id
    FROM uszn.temp$_200_GGS t1''')

# ********************************************************************
def count_table(): # проверка временной таблицы на наличие записей
  try:
    curs.execute('SELECT count(*) FROM uszn.temp$_200_GGS')
    return int(curs.fetchall()[0][0])
  except:
    return 0

# ********************************************************************
def count_collection():
  try:
    curs.execute('''SELECT count(*) FROM uszn.temp$_200_GGS''')
    col_cnt = curs.fetchall()[0]
    writing_to_log_file(log, f'{col_cnt} количество записей')
  except Exception as e:
    ext = f'произошла ошибка при внутри функции count_collection() - {e}'
    alarm_log(mail, log, text)

# ********************************************************
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
  loading_data()
except Exception as e:
  text = f'произошла ошибка при вызове функции loading_data() - {e}'
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
  send_email(mail, 'Коллекция 200 ГГС обновлена', msg_text=text)
except Exception as e:
  text = f'произошла ошибка при вызове функции send_email() - {e}'
  alarm_log(mail, log, text)