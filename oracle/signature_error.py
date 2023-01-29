from generating_report_files import *

# ********************************************
def alarm_ep():
    curs.execute(
    '''select count(*) 
       from uszn.all_smev3_inc_messages
       where date_created>=trunc(sysdate-30, 'dd') and proc_status_id in (3)''')
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
          where date_created>=trunc(sysdate-30, 'dd') and proc_status_id in (3);
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

def alarm_aurora():
    curs.execute(
    '''select count(*) 
       from uszn.all_smev2_inc_messages
       where error_message like 'ORA-29516: Aurora%' and date_created>=trunc(sysdate-30, 'dd')''')
    cnt = int(curs.fetchall()[0][0])

    if cnt > 0:
        curs.execute(
        '''
        declare
          iiIDs        uszn.pkGen.TIntegers;
          i$ Pls_Integer;
        begin
            select id as id bulk collect into iiIDs
              from  uszn.all_smev2_inc_messages
              where error_message like 'ORA-29516: Aurora%' and date_created>=trunc(sysdate-30, 'dd');
          for i in 1..iiIDs.count loop
            begin
              i$ := uszn.pkSMEVProv.AsyncProcessMessage(iiIDs(i),1,1,'Принудительная обработка входящего сообщения СМЭВ-2');
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





# ********************************************

curs = connect_oracle()

cnt_ep = alarm_ep()
cnt_aurora = alarm_aurora()

log = 'signature_error'
text = f'ep - {cnt_ep}, aurora - {cnt_aurora}'

writing_to_log_file(log, text)
send_email('IVAbdulganiev@yanao.ru', 'Проверка ЭП сделана', msg_text=text)