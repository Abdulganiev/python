from generating_report_files import *

# ********************************************************
log = 'requests_200_GGS'
mail = 'IVAbdulganiev@yanao.ru'

# ********************************************************
def drop_table(): # удаление временной таблицы
  writing_to_log_file(log, f'drop_table')
  cnt = count_table()
  writing_to_log_file(log, f'drop_table - {cnt}')
  if cnt > 0:
    curs.execute('DROP TABLE uszn.temp$_200_GGS')
    writing_to_log_file(log, f'DROP TABLE uszn.temp$_200_GGS')

# ********************************************************
def creating_table(): # создание временное таблицы
  writing_to_log_file(log, f'creating_table')
  cnt = count_table()
  if cnt == 0:
    with open('requests_200_GGS_create.sql', 'r', encoding='utf8') as f:
      sql = f.read()
    curs.execute(sql)
    writing_to_log_file(log, f'CREATE TABLE uszn.temp$_200_GGS')
  cnt = count_table()

# ********************************************************
def deleting_collection():
  writing_to_log_file(log, f'deleting_collection')
  curs.execute('''
DELETE uszn.r_ssvc_rq_collection_items
WHERE collection_id=1 and collection_region_id=71''')

# ********************************************************
def loading_data():
  writing_to_log_file(log, f'loading_data')
  curs.execute('''
INSERT INTO uszn.r_ssvc_rq_collection_items(collection_id, collection_region_id, request_id, request_region_id)
    SELECT 1, t1.region_id, t1.id, t1.region_id
    FROM uszn.temp$_200_GGS t1''')

# ********************************************************************
def count_table(): # проверка временной таблицы на наличие записей
  writing_to_log_file(log, f'count_table')
  try:
    curs.execute('SELECT count(*) FROM uszn.temp$_200_GGS')
    cnt = int(curs.fetchall()[0][0])
    writing_to_log_file(log, f'SELECT count(*) FROM uszn.temp$_200_GGS - {cnt}')
    return cnt
  except:
    writing_to_log_file(log, f'SELECT count(*) FROM uszn.temp$_200_GGS - 0')
    return 0

# ********************************************************************
def count_collection():
  try:
    curs.execute('''SELECT count(*) FROM uszn.temp$_200_GGS''')
    col_cnt = curs.fetchall()[0][0]
    writing_to_log_file(log, f'{col_cnt} количество записей во временной таблице')
  except Exception as e:
    ext = f'произошла ошибка при внутри функции count_collection() - {e}'
    alarm_log(mail, log, text)

# ********************************************************
def count_collection_200():
  try:
    curs.execute('''select count(*) from uszn.r_ssvc_rq_collection_items WHERE collection_id=1 and collection_region_id=71''')
    col_cnt = curs.fetchall()[0][0]
    writing_to_log_file(log, f'{col_cnt} количество записей в коллекции')
  except Exception as e:
    text = f'произошла ошибка при внутри функции count_collection_200() - {e}'
    alarm_log(mail, log, text)
  return col_cnt

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
  cnt1 = count_collection_200()
except Exception as e:
  text = f'произошла ошибка при вызове функции count_collection_200() - {e}'
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
  text = count_collection_200()
except Exception as e:
  text = f'произошла ошибка при вызове функции count_collection_200() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  deleting_collection()
except Exception as e:
  text = f'произошла ошибка при вызове функции deleting_collection() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  text = count_collection_200()
except Exception as e:
  text = f'произошла ошибка при вызове функции count_collection_200() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  loading_data()
except Exception as e:
  text = f'произошла ошибка при вызове функции loading_data() - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  cnt2 = count_collection_200()
except Exception as e:
  text = f'произошла ошибка при вызове функции count_collection_200() - {e}'
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