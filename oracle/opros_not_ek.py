from generating_report_files import *
import pandas as pd
from datetime import datetime
import datetime as dt

#***************************************************************
today = dt.date.today()
sec = time.strftime("%S", time.localtime())
path = r'd:/python/schedule/opros/'

name_log = 'opros_not_ek'
name_def = 'opros_not_ek'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
data_len = 0

#***************************************************************
def opros_not_ek():
    with open('opros_not_ek.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return pd.DataFrame(curs.fetchall())

#***************************************************************
def file_survey(data):
    file_name = f'{path}{today}_{sec}_opros_ek.csv'
    data.columns = ['applicant','department','kppogv','serviceCode','targetCode','processingMethod','orderIdEpgu','orderIdIs','oktmo','dateStart','dateEnd','result','channel','snils','firstName','patronymic','phone','email','gender','age','representative','specialistId','specialistName','nameUl','innUl','kppUl']
    data.to_csv(file_name, sep=';', index=False, encoding="utf-8")    

#***************************************************************
try:
    curs = connect_oracle()
except Exception as e:
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

#***************************************************************
writing_to_log_file(name_log, '***********start****************************')
try:
    data = opros_not_ek()
    data_len = len(data)
except Exception as e:
    text = f'произошла ошибка при вызове функции opros_not_ek() - {e}'
    alarm_log(mail, name_log, text)

if data_len > 0:
    file_survey(data)

writing_to_log_file(name_log, f'Количество строк - {data_len}')
writing_to_log_file(name_log, '***********end*****************************')    