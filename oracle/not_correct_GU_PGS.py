import pandas as pd
from generating_report_files import *

#***************************************************************
name_log = 'not_correct_GU_PGS'
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
goto_folder()

try:
    curs = connect_oracle()
    writing_to_log_file(name_log, f'Подключение к базе')
except Exception as e:
  text = f'произошла ошибка при вызове функции connect_oracle - {e}'
  alarm_log(mail, name_log, text)

#***************************************************************
def not_correct_GU_PGS(name_log):
    # writing_to_log_file(name_log, 'Вызов функции not_correct_GU_PGS')
    
    with open('not_correct_GU_PGS.sql', 'r', encoding='utf8') as f:
        sql = f.read()
    curs.execute(sql)
    
    data = {
         'pc_id' : [],
         'region_id' : [],
         'id' : [],
         'message_guid' : [],
         'adr' : [],
         'request_pdoc_id' : [],
         'smev_message_id' : [],
         'state_service_name' : [],
         'mo_out' : [],
        }
    
    for row in curs.fetchall():
        data['pc_id'].append(row[0])
        data['region_id'].append(row[1])
        data['id'].append(row[2])
        data['message_guid'].append(row[3])
        data['adr'].append(row[4])
        data['request_pdoc_id'].append(row[5])
        data['smev_message_id'].append(row[6])
        data['state_service_name'].append(row[7])
        data['mo_out'].append(row[8])
        
    return data

#***************************************************************
def ararm_sql(sql, log, mail):
    # writing_to_log_file(log, 'Вызов функции ararm_sql')
    try:
        curs.execute(sql)
        return 1
    except Exception as e:
        text = f'ошибка \n {sql} \n {e}'
        alarm_log(mail, name_log, text)
        return 0    

#***************************************************************
def not_correct_GU_PGS_transfer(df, name_log, mail):
    writing_to_log_file(name_log, 'Вызов функции not_correct_GU_PGS_transfer')
    for row in df.itertuples(index=False):
        pc_id = row[0]
        region_id = row[1]
        id = row[2]
        message_guid = row[3]
        adr = row[4]
        request_pdoc_id = row[5]
        smev_message_id = row[6]
        state_service_name = row[7]
        mo_out = row[8]

        if row[8] != 0:
            sql = f'''begin -- заявитель {region_id}-{pc_id}
    delete from uszn.r_ssvc_requests where region_id={region_id} and id={id};
    update uszn.r_smev3_inc_messages set region_id={mo_out} -- {adr}
        where message_guid=uszn.pkXMLUtils.StrToGuid('{message_guid}');
    begin
        uszn.pkSMEV3.ScheduleInMsgProcessing('{smev_message_id}');
    end;
    declare
      iiIDs uszn.pkGen.TIntegers;
      i$ Pls_Integer;
    begin
      select id bulk collect into iiIDs
        from uszn.all_personal_doc_files
        where region_id={region_id} and pdoc_id={request_pdoc_id}
      order by id;
      for i in 1..iiIDs.count loop
        begin
          uszn.pkPerson.DeletePDocFile({region_id},iiIDs(i),1);
        end;
      end loop;
    end;
    delete from uszn.r_personal_docs where region_id={region_id} and id={request_pdoc_id};
end;'''
            try:
                resume = ararm_sql(sql, name_log, mail)
            except Exception as e:
                text = f'произошла ошибка при вызове функции resume - {e}'
                alarm_log(mail, name_log, text)

            if resume == 1:
                text = f'Заявитель {pc_id} c ПГС {state_service_name} перенесен в {mo_out}, его адрес {adr}'
                writing_to_log_file(name_log, text)
                send_email(mail, name_log, msg_text=text)
        else:
            text = f'Заявитель {pc_id} c ПГС {state_service_name} - проблема с адресом - {adr}'
            writing_to_log_file(name_log, text)
            send_email(mail, name_log + ' - проблема с адресом', msg_text=text)

#***************************************************************
writing_to_log_file(name_log, '**********start**************')

try:
    data = not_correct_GU_PGS(name_log)
except Exception as e:
  text = f'произошла ошибка при вызове функции not_correct_GU_PGS - {e}'
  alarm_log(mail, name_log, text)

df = pd.DataFrame(data)

if len(set(data['pc_id'])) > 0:
    try:
        not_correct_GU_PGS_transfer(df, name_log, mail)
    except Exception as e:
        text = f'произошла ошибка при вызове функции not_correct_GU_PGS_transfer - {e}'
        alarm_log(mail, name_log, text)

else:
    text = 'Некорретных заявлений ПГС нет'
    writing_to_log_file(name_log, text)
    send_email(mail, name_log, msg_text=text)

writing_to_log_file(name_log, 'end')