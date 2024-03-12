from generating_report_files import *

#***************************************************************
name_log = 'check_CSO_IPPSO_utv'
test = 0
mail = 'IVAbdulganiev@yanao.ru'
name_def = 'ЦСО - прооверка утв. ИППСУ'
check = 0
cnt = 0

#***************************************************************
def check_CSO_IPPSO_utv(curs):
    with open('check_CSO_IPPSO_utv.sql', 'r', encoding='utf8') as f:
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
        data = pd.DataFrame(check_CSO_IPPSO_utv(curs))
        col = ('name', 'ПСУ', 'ИД человека', 'Описание человека', 'ИД ИППСУ', 'Дата решения')
        data.columns = col
        cnt = len(data)
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_CSO_IPPSO_utv() - {e}'
        alarm_log(mail, name_log, text)
        check = 1
        
    if cnt > 0 and check == 0:
        writing_to_log_file(name_log, f'Количество записей - {len(data)}')
    
        for mo in sorted(set(data['name'])):
            cnt = data[data['name'].isin([mo])].count()[0]
            text = f'{mo} - {cnt} строк'
            writing_to_log_file(name_log, text)
            
        generating_report_files(data, name_log, name_def, test, mail, recipient='cso')

writing_to_log_file(name_log, f'************************end****************************************')