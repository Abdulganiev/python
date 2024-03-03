from generating_report_files import *

# *****************************************************************
name_log = 'report_GSP'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

# *****************************************************************
def report_GSP_data():
    with open('report_GSP.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    
    data = {
             'Код МО' : [],
             'Наименование МО' : [],
             'Категория' : [],
             'Количество получателей' : [],
             'Количество членов' : [],
            }

    for row in curs.fetchall():
        data['Код МО'].append(row[0])
        data['Наименование МО'].append(row[1])
        data['Категория'].append(row[2])
        data['Количество получателей'].append(row[3])
        data['Количество членов'].append(row[4])

    return data

# *****************************************************************
def report_GSP_name():
    with open('report_GSP_name.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    return curs.fetchall()[0][0]

# *****************************************************************
goto_folder()

writing_to_log_file(name_log, '********start**********************')

try:
    curs = connect_oracle()
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

try:
    name_file = report_GSP_name()
except Exception as e:
    text = f'произошла ошибка при вызове функции report_GSP_name() - {e}'
    alarm_log(mail, name_log, text)

try:
    data = report_GSP_data()
except Exception as e:
    text = f'произошла ошибка при вызове функции report_GSP_data() - {e}'
    alarm_log(mail, name_log, text)

try:
    if test == 0:
        mail = 'IVAbdulganiev@yanao.ru, OVKolpakova@yanao.ru, NMShcherbinina@yanao.ru'
    generating_report_GSP(data, name_log, name_file, mail)
except Exception as e:
    text = f'произошла ошибка при вызове функции generating_report_GSP() - {e}'
    alarm_log(mail, name_log, text)

writing_to_log_file(name_log, 'end')