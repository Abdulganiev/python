from generating_report_files import *

#***************************************************************
name_log = 'files_in_MFC'
name_def = 'files_in_MFC'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def files_in_MFC():
    with open('files_in_MFC_cnt.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    cnt = curs.fetchone()[0]
    
    if cnt > 0:
      with open('files_in_MFC_processing.sql', 'r', encoding='utf8') as f:
        sql = f.read()
      curs.execute(sql)

    return cnt

#***************************************************************
try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

cnt = str(files_in_MFC())

writing_to_log_file(name_log, cnt)
send_email(mail, name_def, msg_text=cnt)