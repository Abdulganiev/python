import pandas as pd
from generating_report_files import *

#***************************************************************
log = 'not_correct_GU_MSP'
mail = 'IVAbdulganiev@yanao.ru'

#***************************************************************
try:
    curs = connect_oracle()
except Exception as e:
  text = f'произошла ошибка при вызове функции connect_oracle - {e}'
  alarm_log(mail, log, text)

#***************************************************************
def not_correct_GU_MSP():
    # writing_to_log_file(log, 'Вызов функции not_correct_GU_MSP')
    with open('not_correct_GU_MSP.sql', 'r', encoding='utf8') as f:
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
def ararm_sql(sql1, sql2, sql3, log, mail):
    try:
        curs.execute(sql1)
        cnt_e1 = 1
        alarm1 = ''
    except Exception as e1:
        alarm1 = str(e1)
        cnt_e1 = 0
    
    try:
        curs.execute(sql2)
        cnt_e2 = 1
        alarm2 = ''
    except Exception as e2:
        alarm2 = str(e2)
        cnt_e2 = 0
    
    try:
        curs.execute(sql3)
        cnt_e3 = 1
        alarm3 = ''
    except Exception as e3:
        alarm3 = str(e3)
        cnt_e3 = 0
        
    if (cnt_e1 + cnt_e2 + cnt_e3) == 3:
        return 1
    else:
        text = f'''ошибка 
*********** {cnt_e1} \n {sql1} \n *********** \n {alarm1} \n 
*********** {cnt_e2} \n {sql2} \n *********** \n {alarm2} \n 
*********** {cnt_e3} \n {sql3} \n *********** \n {alarm3}'''
        
        writing_to_log_file(log, text)
        send_email(mail, log, msg_text=text)
        return 0

#***************************************************************    
def not_correct_GU_MSP_transfer(df):
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
            sql1 = f'''begin -- заявитель {pc_id} МСП {state_service_name}
    delete from uszn.r_ssvc_requests where region_id={region_id} and id={id};
    update uszn.all_smev2_inc_messages set region_id={mo_out}
        where message_guid=uszn.pkXMLUtils.StrToGuid('{message_guid}');
    declare
        rMessageGUID Raw(16) := uszn.pkXMLUtils.StrToGuid('{message_guid}');
        bMessageData BLOB;
        iSOAPBodyTagID Pls_Integer;
        iOperationTagID Pls_Integer;
    begin
        begin
            select request_data into bMessageData from uszn.r_smev_messages where message_guid=rMessageGUID;
        exception
            when No_Data_Found then Raise_Application_Error(-20000, 'Сообщение СМЭВ-2 не найдено');
        end;
        uszn.pkXMLImp.ParseXMLData(bMessageData, 1, 1, 1);
        uszn.pkXMLImp.ComputeNSAttribs(1, 1);
        uszn.pkSMEVProv.SetSvcSMEVNamespace(104, 8);
        iSOAPBodyTagID := uszn.pkXML_SOAP.GetBodyTagID(1);
        iOperationTagID := uszn.pkXMLImp.GetChildTagID(iSOAPBodyTagID, 1, 0);
        uszn.pkWSStateSvc.ProcessCreateApplication(rMessageGUID, iOperationTagID, 1);
    end;
end;'''    
            sql2 = f'''begin
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
end;'''
            sql3 = f'''begin    
    delete from uszn.r_personal_docs where region_id={region_id} and id={request_pdoc_id};
    begin
      uszn.pkSMEVProv.ScheduleAsyncProcessing(uszn.pkSMEVProv.GetMessageGUID({smev_message_id},1));
    end;
end;'''
            
            try:
                resume = ararm_sql(sql1, sql2, sql3, log, mail)
            except Exception as e:
                text = f'произошла ошибка при вызове функции ararm_sql - {e}'
                alarm_log(mail, log, text)

            if resume == 1:
                text = f'Заявитель {pc_id} c МСП {state_service_name} перенесен в {mo_out}, его адрес {adr}'

                writing_to_log_file(log, text)
                send_email(mail, log, msg_text=text)
        else:
            text = f'Заявитель {pc_id} c МСП {state_service_name} - проблема с адресом - {adr}'
            writing_to_log_file(log, text)
            send_email(mail, log+' проблема с адресом', msg_text=text)

#***************************************************************
writing_to_log_file(log, '**********start**************')

try:
    data = not_correct_GU_MSP()
except Exception as e:
    text = f'произошла ошибка при вызове функции not_correct_GU_MSP - {e}'
    alarm_log(mail, log, text)

try:
    df = pd.DataFrame(data)
except Exception as e:
    text = f'произошла ошибка при вызове функции pd.DataFrame(data) - {e}' #' \n {data}'
    alarm_log(mail, log, text)


if len(set(data['pc_id'])) > 0:
    try:
        not_correct_GU_MSP_transfer(df)
    except Exception as e:
        text = f'произошла ошибка при вызове функции not_correct_GU_MSP_transfer - {e}'
        alarm_log(mail, log, text)
else:
    text = 'Некорретных заявлений МСП нет'

    writing_to_log_file(log, text)
    send_email(mail, log, msg_text=text)

writing_to_log_file(log, 'end')