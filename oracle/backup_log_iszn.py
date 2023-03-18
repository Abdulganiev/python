import shutil, os, re
import datetime as dt
import zipfile
from generating_report_files import *

# ******************************************************
log_backups = 'log/'
path_y = r'Y:/'
os.chdir(path_y)
name_log = 'backup_log_iszn'
mail = 'IVAbdulganiev@yanao.ru'

# ******************************************************
def file_list(file_start, file_end, path_log):
    c = os.listdir()
    file_extension = '.' + file_end
    file_find = r'^' + file_start
    not_file = file_start + str(dt.date.today()) + file_extension
    for file in c:
        if re.findall(file_find, file) and file.endswith(file_extension) and file != not_file:
            text = f'**** {file}'
            writing_to_log_file(name_log, text)
            archive = file + '.zip'
            try:
                with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                    zf.write(file)
                    text = f'{file} to {archive}'
                    writing_to_log_file(name_log, text)
            except Exception as e:    
                text = f'произошла ошибка при архивировании файла {file} - {e}'
                alarm_log(mail, name_log, text)
                writing_to_log_file(name_log, text)

            try:
                shutil.move(archive, path_log)
                text = f'move {archive} to {path_log}'
                writing_to_log_file(name_log, text)
            except Exception as e:    
                text = f'произошла ошибка при переносе файла {archive} - {e}'
                alarm_log(mail, name_log, text)
            
            try:
                os.remove(file)
                text = f'delete {file}'
                writing_to_log_file(name_log, text)
            except Exception as e:    
                text = f'произошла ошибка при удалении файла {file} - {e}'
                alarm_log(mail, name_log, text)
                

# ******************************************************            
dict_logs = {
    'DOLG_REPORT_' : 'DOLG', 
    'EGISSO_processing_facts_' : 'EGISSO', 
    'EGISSO_sending_facts_' : 'EGISSO', 
    'file_' : 'file', 
    'GIS_GKH_DOLG_' : 'GIS_GKH',
    'GIS_GKH_request_dolg_' : 'GIS_GKH',
    'LK_MSP_bind_people_' : 'LK_MSP', 
    'LK_MSP_delete_' : 'LK_MSP', 
    'service_' : 'service', 
    'smev_to_file_' : 'file', 
    'smev2_in_' : 'smev', 
    'smev2_out_' : 'smev', 
    # 'smev3_in_' : 'smev', 
    # 'smev3_out_' : 'smev', 
    'Statistics_' : 'Statistics',
    'ZAGS_GGS_' : 'ZAGZ', 
    'ZAGZ_' : 'ZAGZ', 
    'EKJ_faсt_' : 'EKJ_faсt',
    'EKJ_messages_' : 'EKJ_messages',
    'EKJ_new_card_' : 'EKJ_new_card',
    'EKJ_new_change_contract_GU_' : 'EKJ_new_change_contract_GU',
    'EKJ_new_change_contract_NKO_' : 'EKJ_new_change_contract_NKO',
    'EKJ_new_contract_GU_' : 'EKJ_new_contract_GU',
    'EKJ_new_contract_NKO_' : 'EKJ_new_contract_NKO',
    'EKJ_new_employee_' : 'EKJ_new_employee',
    'EKJ_new_IPSU_' : 'EKJ_new_IPSU',
    'EKJ_new_urgent_' : 'EKJ_new_urgent',
    'EKJ_processing_responses_' : 'EKJ_processing_responses',
    'EKJ_register_' : 'EKJ_register',
    'EKJ_YD_out_' : 'EKJ_YD_out',
    'EKJ_YD_wants_to_participate_' : 'EKJ_YD_wants_to_participate',
    'EKJ_Recipient_' : 'EKJ_Recipient',
    'EKJ_EPB_' : 'EKJ_EPB',
}

text = '****************start****************'
writing_to_log_file(name_log, text)

for file, log_backup in dict_logs.items():
    path_log = path_y + log_backups + log_backup+'/'
    file_list(file, 'txt', path_log)

text = '****************end******************'
writing_to_log_file(name_log, text)