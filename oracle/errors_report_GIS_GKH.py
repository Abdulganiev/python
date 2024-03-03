from generating_report_files import *

#***************************************************************
name_log = 'errors_report__GIS_GKH'
name_def = 'Ошибки при отправке в ГИС ЖКХ'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def errors_report_GIS_GKH():
    with open('errors_report_GIS_GKH.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    
    data = {
         'name' : [],
         'id человека' : [] ,
         'ФИО и д.р' : [] ,
         'Адрес' : [] ,
         'Ошибка' : [],
        }
    
    for row in curs.fetchall():
        data['name'].append(row[0])
        data['id человека'].append(row[1])
        data['ФИО и д.р'].append(row[2])
        data['Адрес'].append(row[3])
        data['Ошибка'].append(row[4])
    
    return data

#***************************************************************
goto_folder()

try:
  curs = connect_oracle()
except Exception as e:
  text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
  alarm_log(mail, name_log, text)

try:
  data = errors_report_GIS_GKH()
except Exception as e:
  text = f'произошла ошибка при вызове функции errors_report_GIS_GKH() - {e}'
  alarm_log(mail, name_log, text)

generating_report_files(data, name_log, name_def, test, mail)