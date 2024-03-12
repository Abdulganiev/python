from generating_report_files import *

#***************************************************************
name_log = 'check_ES_alarm_MIR_DO'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'Неверный номер карты МИР для ЭС для ДО'
check = 0
cnt = 0

#***************************************************************
def check_ES_alarm_MIR_DO(curs):
    with open('check_ES_alarm_MIR_DO.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()

#***************************************************************
goto_folder()

writing_to_log_file(name_log, f'************************start***************************************')

try:
    curs = connect_oracle()
    check = 0
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)
    check = 1

if check == 0:
    try:
        data = pd.DataFrame(check_ES_alarm_MIR_DO(curs))
        col = ('name','Тип сертификата','id получателя','Описание получателя','id субъекта','Описание субъекта','Статус сертификата','Описание ошибки','Дата ошибки')
        data.columns = col
        cnt = len(data)
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_ES_alarm_MIR_DO() - {e}'
        alarm_log(mail, name_log, text)
        check = 1
        
    if cnt > 0 and check == 0:
        writing_to_log_file(name_log, f'Количество записей - {len(data)}')
        generating_report_files(data, name_log, name_def, test, mail, recipient='do')

writing_to_log_file(name_log, f'************************end****************************************')