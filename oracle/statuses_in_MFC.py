from generating_report_files import *

#***************************************************************
mail = 'IVAbdulganiev@yanao.ru'
name_log = 'statuses_in_MFC'

#***************************************************************
def statuses_in_MFC():
    with open('statuses_in_MFC_cnt.sql', 'r', encoding='utf8') as f:
      sql = f.read()
    curs.execute(sql)

    cnt = curs.fetchone()[0]
    
    if cnt > 0:
      with open('statuses_in_MFC.sql', 'r', encoding='utf8') as f:
        sql = f.read()
      curs.execute(sql)

    return cnt

#***************************************************************
try:
  curs = connect_oracle()
except Exception as e:
  text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
  alarm_log(mail, name_log, text)

try:
  cnt = str(statuses_in_MFC())
  writing_to_log_file(name_log, cnt)
  send_email(mail, 'Статусы в МФЦ отработаны', msg_text=cnt)
except Exception as e:
  text = f'произошла ошибка при вызове функции statuses_in_MFC() - {e}'
  alarm_log(mail, name_log, text)
