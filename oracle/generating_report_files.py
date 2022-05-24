from smtp import *
from writing_to_log_file import *
import shutil, zipfile
import pandas as pd
from datetime import datetime
import datetime as dt


def generating_report_files(df, name_log, name_def, test, mail):
	data = pd.DataFrame(df)
	files = ''
	mo = set(data['name'])
	if len(mo) > 0:
		for row in mo:
		    file = row + '.xlsx'
		    data[data['name'].isin([row])].to_excel(file, index=False)
		    if test == 1:
		        path = 'c:/VipoNet_out1/'
		    else:
		        path = 'c:/VipoNet_out/'
		    try:
		      shutil.move(file, path)
		    except:
		      send_email('IVAbdulganiev@yanao.ru', f'{name_def} - ошибка переноса файла', msg_text=file)
		      text = f'{name_def} - ошибка переноса файла {file} в папку {path}'
		      writing_to_log_file(name_log, text)      
		    files += file + '\n'

		writing_to_log_file(name_log, '\n'+files)
		send_email(mail, f'{name_def} в МО отправлены', msg_text=files)
	else:
		text = 'файлов нет'
		writing_to_log_file(name_log, text)
		send_email(mail, f'{name_def} - {text}', msg_text='')

# *****************************************************************

def generating_report_files_PFR(df, name_log, name_def, test, mail):
    data = pd.DataFrame(df)
    dt = datetime.now().strftime('%m-%Y')
    file = f'{name_def}{dt}.xlsx'
    data.to_excel(file, index=False)
    writing_to_log_file(name_log, f'создали файл {file}')

    if test == 1:
        path = 'c:/VipoNet_out1/'
        writing_to_log_file(name_log, f'path {path}')
    else:
        path = 'c:/VipoNet_out/'
        writing_to_log_file(name_log, f'path {path}')
    try:
	    path_backup = 'd:/python/schedule/backup/'
	    writing_to_log_file(name_log, f'path_backup {path_backup}')
	    
	    try:
	    	new_file = file + '.zip'
	    	writing_to_log_file(name_log, f'архирование файла {new_file}')
	    	zipFile = zipfile.ZipFile(new_file, 'w', zipfile.ZIP_DEFLATED)
	    	zipFile.write(file)
	    	zipFile.close()
	    except:
	    	writing_to_log_file(name_log, 'ошибка архивирования файла {file} в {new_file}')
	    
	    try:
	    	shutil.move(new_file, path)
	    	writing_to_log_file(name_log, f'перенесли {new_file} в {path}')
	    except:
	    	writing_to_log_file(name_log, f'ошибка переноса {new_file} в {path}')

	    try:
	    	shutil.move(file, path_backup)
	    	writing_to_log_file(name_log, f'перенесли {file} в {path_backup}')
	    except:
	    	writing_to_log_file(name_log, f'ошибка переноса {file} в {path_backup}')

	    writing_to_log_file(name_log, new_file)

	    send_email(mail, f'{name_def} в ПФР отправлен', msg_text=new_file)
	    writing_to_log_file(name_log, f'{name_def} в ПФР отправлен')
    except Exception as e:
      	text = f'{name_def} - ошибка'
      	send_email(mail, f'{name_def} - ошибка ', msg_text=text)
      	writing_to_log_file(name_log, text)      

# *****************************************************************

def generating_report_files_PFR_2(name_log, name_def, test, mail, text):
	dt = datetime.now().strftime('%m-%Y')
	new_file = name_def
	path_backup = 'd:/python/schedule/backup/'

	if test == 1:
		path = 'c:/VipoNet_out1/'
	else:
		path = 'c:/VipoNet_out/'

	writing_to_log_file(name_log, f'выбран режим {test} - {path}')

	try:
		os.remove(f'{path}{new_file}')
		writing_to_log_file(name_log, f'{path}{new_file} удален')
	except Exception as e:
		writing_to_log_file(name_log, f'сбой при удалении {path}{new_file}, ошибка {e}')

	try:
		os.remove(f'{path_backup}{new_file}')
		writing_to_log_file(name_log, f'{path_backup}{new_file} удален')
	except Exception as e:
		writing_to_log_file(name_log, f'сбой при удалении {path_backup}{new_file}, ошибка {e}')
	
	cnt = 0 # счетчик для отправки

	try:
		shutil.copy(new_file, path)
		writing_to_log_file(name_log, f'Файл {new_file} скопирован в {path}')
		cnt += 1
	except Exception as e:
		text = f'{name_def} - ошибка копирования файла {new_file} в папку {path}, ошибка - {e}'
		send_email(mail, f'{new_file} - ошибка переноса файла', msg_text=text)
		writing_to_log_file(name_log, text)

	try:
		shutil.move(new_file, path_backup)
		writing_to_log_file(name_log, f'Файл {new_file} перемещен в {path_backup}')
		cnt += 1
	except Exception as e:
		text = f'{name_def} - ошибка переноса файла {new_file} в папку {path_backup}, ошибка - {e}'
		send_email(mail, f'{new_file} - ошибка переноса файла', msg_text=text)
		writing_to_log_file(name_log, text)

	if cnt == 2:
		send_email(mail, f'{name_def} в ПФР отправлен', msg_text=text)
		writing_to_log_file(name_log, f'Письмо отправлено с текстом - {text}')
	else:
		send_email(mail, f'Alarm {name_def}', msg_text=text)
		writing_to_log_file(name_log, 'Письмо "Alarm" отправлено')