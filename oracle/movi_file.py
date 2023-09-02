from generating_report_files import *
import subprocess

#***************************************************************
name_log = 'movi_file'
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************    
path_in = 'z:/! Обмен с организациями/УСЗН/к ним/'
path_to = 'c:/VipoNet_out/'
os.chdir(path_in)

c = os.listdir(os.getcwd())
for file in c:
    movi_file(file, name_log, name_log, path_in, path_to)

#***************************************************************    
path_in = 'z:/! Обмен с организациями/от ВК/'
path_to = 'd:/python/schedule/vk_usvo/'
os.chdir(path_in)

cnt = 0
c = os.listdir(os.getcwd())
for file in c:
    movi_file(file, name_log, name_log, path_in, path_to)
    cnt += 1
    if cnt > 0:
        subprocess.call("python d:/python/schedule/VK_USVO.py", shell=True)