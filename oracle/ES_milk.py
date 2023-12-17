import os
from generating_report_files import *

#***************************************************************
log = 'ES_milk'
mail = 'IVAbdulganiev@yanao.ru'
path_backup = r'd:/python/schedule/backup/ES_milk/'
path = r'd:/python/schedule/zdrav_milk/'
test = 0

#***************************************************************
writing_to_log_file(log, '***************************************')
os.chdir(path)
c = os.listdir(os.getcwd())

for file in c:
    if file.endswith(".xlsx") or file.endswith(".xltx"):
        writing_to_log_file(log, f'Файл поступил - {file}')
        os.rename(file, '063 - ' + file)
        file = '063 - ' + file

        try:
            copy_vipnet(test, file, log, log)
        except Exception as e:
            text = f'произошла ошибка при вызове функции copy_vipnet() - {e}'
            alarm_log(mail, log, text)

        try:
            backup_file(test, file, log, log, path_backup)
        except Exception as e:
            text = f'произошла ошибка при вызове функции backup() - {e}'
            alarm_log(mail, log, text)
