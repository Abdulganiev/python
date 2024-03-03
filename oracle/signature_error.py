from generating_report_files import *

#***************************************************************
mail = 'IVAbdulganiev@yanao.ru'
name_log = 'signature_error'
cnt_ep = 0
cnt_aurora = 0

# ********************************************
def alarm_ep():
  with open('signature_error_cnt.sql', 'r', encoding='utf8') as f:
    sql = f.read()
  curs.execute(sql)
  cnt = int(curs.fetchall()[0][0])

  if cnt > 0:
    with open('signature_error_alarm.sql', 'r', encoding='utf8') as f:
      sql = f.read()
    curs.execute(sql)
  return cnt

# ********************************************
def alarm_aurora():
  with open('signature_error_cnt_aurora.sql', 'r', encoding='utf8') as f:
    sql = f.read()
  curs.execute(sql)
  cnt = int(curs.fetchall()[0][0])

  if cnt > 0:
    with open('signature_error_alarm.sql', 'r', encoding='utf8') as f:
      sql = f.read()
    curs.execute(sql)
  return cnt

# ********************************************
goto_folder()

try:
  curs = connect_oracle()
except Exception as e:
  text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
  alarm_log(mail, name_log, text)

try:
  cnt_ep = alarm_ep()
except Exception as e:
  text = f'произошла ошибка при вызове функции alarm_ep() - {e}'
  alarm_log(mail, name_log, text)

try:
  cnt_aurora = alarm_aurora()
except Exception as e:
  text = f'произошла ошибка при вызове функции alarm_aurora() - {e}'
  alarm_log(mail, name_log, text)  

text = f'ep - {cnt_ep}, aurora - {cnt_aurora}'

writing_to_log_file(name_log, text)
send_email(mail, 'Проверка ЭП сделана', msg_text=text)
