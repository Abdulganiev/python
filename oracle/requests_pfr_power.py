from generating_report_files import *

# ********************************************************
log = 'requests_pfr_power'
mail = 'IVAbdulganiev@yanao.ru'

# ********************************************************
def drop_table(): # удаление временной таблицы
  cnt = count_table()
  if cnt > 0:
    curs.execute('DROP TABLE uszn.temp$_pfr_power')

# ********************************************************
def creating_table(): # создание временное таблицы
  cnt = count_table()
  if cnt == 0:
    with open('requests_pfr_power_create.sql', 'r', encoding='utf8') as f:
      sql = f.read()
      curs.execute(sql)

# ********************************************************
def deleting_collection():
  sql = f'DELETE uszn.r_pc_collection_items WHERE collection_region_id=104 and collection_id in (71,72,73,74)'
  curs.execute(sql)

# ********************************************************
def loading_data_1():
    with open('requests_pfr_power_load_1.sql', 'r', encoding='utf8') as f:
      sql = f.read()
      curs.execute(sql)

# ********************************************************************
def loading_data_2():
    with open('requests_pfr_power_load_2.sql', 'r', encoding='utf8') as f:
      sql = f.read()
      curs.execute(sql)

# ********************************************************************
def loading_data_3():
    with open('requests_pfr_power_load_3.sql', 'r', encoding='utf8') as f:
      sql = f.read()
      curs.execute(sql)

# ********************************************************************
def loading_data_4():
    with open('requests_pfr_power_load_4.sql', 'r', encoding='utf8') as f:
      sql = f.read()
      curs.execute(sql)

# ********************************************************************
def count_table(): # проверка временной таблицы на наличие записей
  sql = f'SELECT count(*) FROM uszn.temp$_pfr_power'
  try:
    curs.execute(sql)
    return int(curs.fetchall()[0][0])
  except:
    return 0

# ********************************************************
goto_folder()

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
  text = f'произошла ошибка при вызове функции loading_data_1 - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  loading_data_2()
except Exception as e:
  text = f'произошла ошибка при вызове функции loading_data_2 - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  loading_data_3()
except Exception as e:
  text = f'произошла ошибка при вызове функции loading_data_3 - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  loading_data_4()
except Exception as e:
  text = f'произошла ошибка при вызове функции loading_data_4 - {e}'
  alarm_log(mail, log, text)

# ********************************************************
text = f'{cnt1} записей до загрузки, {cnt2} записей после загрузки'
try:
  writing_to_log_file(log, text)
except Exception as e:
  text = f'произошла ошибка при вызове функции writing_to_log_file - {e}'
  alarm_log(mail, log, text)

# ********************************************************
try:
  send_email(mail, 'Коллекции для ПФР работа обновлены', msg_text=text)
except Exception as e:
  text = f'произошла ошибка при вызове функции send_email - {e}'
  alarm_log(mail, log, text)