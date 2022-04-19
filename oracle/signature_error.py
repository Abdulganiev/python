import jaydebeapi
import json
from datetime import datetime
from smtp import *


path = "access_report.txt"
with open(path) as f:
    access = json.load(f)
    
driver = 'ojdbc14.jar'
path_base = access['path_base']
password = access['password']
login = access['login']
port = access['port']
sid = access['sid']

conn = jaydebeapi.connect(
    'oracle.jdbc.driver.OracleDriver',
    f'jdbc:oracle:thin:{login}/{password}@{path_base}:{port}/{sid}',
    [login, password],
    driver)

curs = conn.cursor()

def alarm_ep():
    curs.execute(
    '''select count(*) from
     (select id
       from uszn.all_smev3_inc_messages
       where date_created>=To_Date('01.01.2021') and proc_status_id in (3))'''
    )
    cnt = int(curs.fetchall()[0][0])

    if cnt > 0:
        curs.execute(
        '''
        declare
          iiIDs        uszn.pkGen.TIntegers;
          i$ Pls_Integer;
        begin
        select id bulk collect into iiIDs
          from uszn.all_smev3_inc_messages
          where date_created>=To_Date('01.01.2021') and proc_status_id in (3);
          for i in 1..iiIDs.count loop
            begin
              i$ := uszn.pkSMEV3.ProcessInMessage(iiIDs(i), 1, 1,'Принудительная обработка входящего сообщения СМЭВ-3');
            commit;
            exception
              when Others then
                rollback;
                raise;
            end;
          end loop;
        end;
        '''
        )
        return cnt

cnt = alarm_ep()

log = "signature_error.log"
day = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

with open(f'log/{log}', 'a') as f:
    f.write('**************************************\n')
    f.write(f'{day} - {cnt}\n')

send_email('IVAbdulganiev@yanao.ru', 'Проверка ЭП сделана', msg_text=f'{day} - {cnt}\n')