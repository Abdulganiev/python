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
def statuses_in_MFC():
    curs.execute('''
select 
    count(*)    
 from uszn.r_smev2_calls b1
 inner join
 (select c1.region_id, max(c1.id) as id -- находим у этих сообщений макс ИД отправлений
   from uszn.r_smev2_calls c1
    inner join
 (select t1.region_id, t1.id -- находим для этих отправлений сообщения СМЭВ2
   from uszn.r_smev2_requests t1
     inner join
    (select id, region_id, request_id -- находим все отправления с ошибками
      from uszn.r_smev2_calls
       where error_message is not null and date_created > to_date('01.12.2021')) t2
     on t1.region_id=t2.region_id and t1.id=t2.request_id) c2
  on c1.region_id=c2.region_id and c1.request_id=c2.id
 group by c1.region_id) b2
 on b1.region_id=b2.region_id and b1.id=b2.id
 where b1.error_message is not null''')

    cnt = curs.fetchone()[0]
    
    if cnt > 0:
        curs.execute('''
update uszn.all_smev2_out_messages
  set next_send_time=sysdate
where (region_id, id) in

(select b1.region_id, b1.request_id
 from uszn.r_smev2_calls b1
 inner join
 (select c1.region_id, max(c1.id) as id -- находим у этих сообщений макс ИД отправлений
   from uszn.r_smev2_calls c1
    inner join
 (select t1.region_id, t1.id -- находим для этих отправлений сообщения СМЭВ2
   from uszn.r_smev2_requests t1
     inner join
    (select id, region_id, request_id -- находим все отправления с ошибками
      from uszn.r_smev2_calls
       where error_message is not null and date_created > to_date('01.12.2021')) t2
     on t1.region_id=t2.region_id and t1.id=t2.request_id) c2
  on c1.region_id=c2.region_id and c1.request_id=c2.id
 group by c1.region_id, c1.request_id) b2
 on b1.region_id=b2.region_id and b1.id=b2.id
 where b1.error_message is not null)''')

        cnt = str(cnt)

        writing_to_log_file('statuses_in_MFC', cnt)
        send_email('IVAbdulganiev@yanao.ru', 'Статусы в МФЦ отработаны', msg_text=cnt)

#***************************************************************

statuses_in_MFC()