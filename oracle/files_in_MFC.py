from generating_report_files import *

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

    return cnt

#***************************************************************

curs = connect_oracle()

cnt = str(files_in_MFC())

writing_to_log_file('files_in_MFC', cnt)
send_email('IVAbdulganiev@yanao.ru', 'Файлы МФЦ отработаны', msg_text=cnt)
