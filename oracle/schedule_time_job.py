import subprocess
from generating_report_files import *

#***************************************************************
name_log = 'schedule_time'
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
def movi_file_share():
    try:
        subprocess.call("python d:/python/schedule/movi_file_share.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции movi_file_share() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def unlock_user_iszn():
    try:
        subprocess.call("python d:/python/schedule/unlock_user_iszn.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции unlock_user_iszn() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def seetable_trud_stac():
    try:
        writing_to_log_file(name_log, f'Запуск процесса seetable_trud_stac')
        subprocess.call("python d:/python/schedule/seetable_trud_stac.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции seetable_trud_stac() - {e}'
        writing_to_log_file(name_log, text)


#***************************************************************
def category_large_family():
    try:
        writing_to_log_file(name_log, f'Запуск процесса category_large_family')
        subprocess.call("python d:/python/schedule/category_large_family.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции category_large_family() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def category_pfr_trud():
    try:
        writing_to_log_file(name_log, f'Запуск процесса category_pfr_trud')
        subprocess.call("python d:/python/schedule/category_pfr_trud.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции category_pfr_trud() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def category_svo():
    try:
        writing_to_log_file(name_log, f'Запуск процесса category_svo')
        subprocess.call("python d:/python/schedule/category_svo.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции category_svo() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def signature_error():
    try:
        writing_to_log_file(name_log, f'Запуск процесса signature_error')
        subprocess.call("python d:/python/schedule/signature_error.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции signature_error() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def lk_reconnecting():
    try:
        writing_to_log_file(name_log, f'Запуск процесса lk_reconnecting')
        subprocess.call("python d:/python/schedule/lk_reconnecting.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции lk_reconnecting() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def EKJ_find_alarms_cnt():
    try:
        writing_to_log_file(name_log, f'Запуск процесса EKJ_find_alarms_cnt')
        subprocess.call("python d:/python/schedule/EKJ_find_alarms_cnt.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции EKJ_find_alarms_cnt() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def not_correct_GU():
    try:
        writing_to_log_file(name_log, f'Запуск процесса not_correct_GU')
        subprocess.call("python d:/python/schedule/not_correct_GU_MSP.py", shell=True)
        subprocess.call("python d:/python/schedule/not_correct_GU_PGS.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции not_correct_GU() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def svo(): # временная таблица СВО
    try:
        writing_to_log_file(name_log, f'Запуск процесса svo')
        subprocess.call("python d:/python/schedule/svo.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции svo() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def ES_new_MIR(): # привязка к ЭС новой карты МИР
    try:
        writing_to_log_file(name_log, f'Запуск процесса ES_new_MIR')
        subprocess.call("python d:/python/schedule/ES_new_MIR.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции ES_new_MIR() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def ES_EKGYA(): # изменилась карта МИР относительно ЭС
    try:
        writing_to_log_file(name_log, f'Запуск процесса ES_EKGYA')
        subprocess.call("python d:/python/schedule/ES_EKGYA.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции ES_EKGYA() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def check_dul_large_family(): # поиск многодетных с кривыми ДУЛ
    try:
        writing_to_log_file(name_log, f'Запуск процесса check_dul_large_family')
        subprocess.call("python d:/python/schedule/check_dul_large_family.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_dul_large_family() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def report_ES(): # реестр по ЭС
    try:
        writing_to_log_file(name_log, f'Запуск процесса report_ES')
        subprocess.call("python d:/python/schedule/report_ES.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции report_ES() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def report_large_family(): # реестр многодетных
    try:
        writing_to_log_file(name_log, f'Запуск процесса report_large_family')        
        subprocess.call("python d:/python/schedule/report_large_family.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции report_large_family() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def check_EPB(): # проверка дубликатов ЕПБ
    try:
        writing_to_log_file(name_log, f'Запуск процесса check_EPB')        
        subprocess.call("python d:/python/schedule/check_EPB.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_EPB() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def check_large_family_duble(): # проверка дубликатов многодетных
    try:
        writing_to_log_file(name_log, f'Запуск процесса check_large_family_duble')
        subprocess.call("python d:/python/schedule/check_large_family_duble.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_large_family_duble() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
def check_doc_large_family(): # названия в удостоверении многодетных
    try:
        writing_to_log_file(name_log, f'Запуск процесса check_doc_large_family')
        subprocess.call("python d:/python/schedule/check_doc_large_family.py", shell=True)
    except Exception as e:
        text = f'произошла ошибка при вызове функции check_doc_large_family() - {e}'
        writing_to_log_file(name_log, text)

#***************************************************************
