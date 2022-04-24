from smtp import *
from writing_to_log_file import *
import shutil
import pandas as pd


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
	
	text = 'файлов нет'
	writing_to_log_file(name_log, text)		
	send_email(mail, f'{name_def} - {text}', msg_text='')