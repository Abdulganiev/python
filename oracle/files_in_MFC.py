import jaydebeapi
import json
from datetime import datetime
from smtp import *
from writing_to_log_file import *

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


#***************************************************************
def files_in_MFC():
    curs.execute('''
select 
    count(*)    
from
 (select r.message_id
  from uszn.all_smev2_inc_msg_processing r
         where r.error_count>0 and r.log_data like '%Operation timed out with%' and r.id in
          (select max(r.id) as id from uszn.all_smev2_inc_msg_processing r
             where r.message_id in
              (select id from uszn.all_smev2_inc_messages where date_created>=(sysdate-7))
       group by r.message_id))''')

    cnt = curs.fetchone()[0]
    
    if cnt > 0:
        curs.execute('''
    declare 
      iiIDs        uszn.pkGen.TIntegers; 
      i$ Pls_Integer; 
    begin 
    select r.message_id bulk collect into iiIDs 
       from uszn.all_smev2_inc_msg_processing r 
         where r.error_count>0 and r.log_data like '%Operation timed out with%' 
           and r.id in 
          (select max(r.id) as id from uszn.all_smev2_inc_msg_processing r 
            where r.message_id in 
               (select id from uszn.all_smev2_inc_messages 
                  where date_created>=(sysdate-7) ) 
         group by r.message_id); 
      for i in 1..iiIDs.count loop 
        begin 
          i$ :=uszn.pkSMEVProv.AsyncProcessMessage(iiIDs(i),1,1,'Принудительная асинхронная обработка входящего сообщения СМЭВ-2'); 
          commit; 
        exception 
          when Others then 
            rollback; 
            raise; 
        end; 
      end loop; 
    end;''')

        cnt = str(cnt)

        writing_to_log_file('files_in_MFC', cnt)
        send_email('IVAbdulganiev@yanao.ru', 'Файлы МФЦ отработаны', msg_text=cnt)

#***************************************************************

files_in_MFC()