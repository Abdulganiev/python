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

def generating_report_files_PFR(df, name_log, name_def, test, mail):
    data = pd.DataFrame(df)
    dt = datetime.now().strftime('%m-%Y')
    file = f'{name_def}{dt}.xlsx'
    data.to_excel(file, index=False)
    if test == 1:
        path = 'c:/VipoNet_out1/'
    else:
        path = 'c:/VipoNet_out/'
    try:
	    path_backup = 'd:/python/schedule/backup/'
	    
	    new_file = file + '.zip'
	    zipFile = zipfile.ZipFile(new_file, 'w', zipfile.ZIP_DEFLATED)
	    zipFile.write(file)
	    zipFile.close()
	    shutil.move(new_file, path)

	    today = dt.date.today()
	    new_file_name = f'{today} - {file}'
	    os.replace(file, f'backup/{new_file_name}')

	    writing_to_log_file(name_log, new_file)
	    send_email(mail, f'{name_def} в ПФР отправлен', msg_text=new_file)
	    writing_to_log_file(name_log, f'Файл {file} перемещен в backup и переименован в {new_file_name}')
    except:
      	send_email('IVAbdulganiev@yanao.ru', f'{name_def} - ошибка переноса файла', msg_text=file)
      	text = f'{name_def} - ошибка переноса файла {file} в папку {path}'
      	writing_to_log_file(name_log, text)      

def generating_report_files_PFR_2(name_log, name_def, test, mail, text):
	dt = datetime.now().strftime('%m-%Y')
	new_file = name_def
	path_backup = 'd:/python/schedule/backup/'

	if test == 1:
		path = 'c:/VipoNet_out1/'
	else:
		path = 'c:/VipoNet_out/'

	try:
		os.remove(f'{path}/{new_file}')
		os.remove(f'{path_backup}/{new_file}')
	except:
		pass
	
	try:
		shutil.copy(new_file, path)
		shutil.move(new_file, path_backup)
		writing_to_log_file(name_log, new_file)
		send_email(mail, f'{name_def} в ПФР отправлен', msg_text=text)
		writing_to_log_file(name_log, f'Файл {new_file} перемещен в backup')
	except:
		send_email('IVAbdulganiev@yanao.ru', f'{new_file} - ошибка переноса файла', msg_text=new_file)
		text = f'{name_def} - ошибка переноса файла {new_file} в папку {path}'
		writing_to_log_file(name_log, text)