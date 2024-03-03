from generating_report_files import *

# *****************************************************************
name_log = 'report_RSD_children'
mail = 'IVAbdulganiev@yanao.ru, ISZaguzin@yanao.ru'

# *****************************************************************
def report_RSD_children():
    with open('report_RSD_children.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    data, rsd_all, rsd_tr = curs.fetchall()[0]

    text = f'''Информация о реализации Федерального закона от 16.04.2022 № 113-ФЗ «О внесении изменений в статью 12.1 Федерального закона «О государственной социальной помощи»\n
    по состоянию на {data}\n
    {rsd_all}\n
    {rsd_tr}'''

    writing_to_log_file(name_log, text)

    send_email(mail, name_log, msg_text=text)


# *****************************************************************
goto_folder()

try:
    curs = connect_oracle()
except Exception as e:    
    text = f'произошла ошибка при вызове функции connect_oracle() - {e}'
    alarm_log(mail, name_log, text)

# *****************************************************************
writing_to_log_file(name_log, '********start**********************')

try:
    name_file = report_RSD_children()
except Exception as e:
    text = f'произошла ошибка при вызове функции report_RSD_children() - {e}'
    alarm_log(mail, name_log, text)

writing_to_log_file(name_log, 'end')