import pandas as pd
from generating_report_files import *

#***************************************************************
curs = connect_oracle()

#***************************************************************
def not_correct_GU_MSP():
    curs.execute('''
select t.pc_id, t.region_id, t.id, t.message_guid, t.adr, t.request_pdoc_id, t.smev_message_id, t.state_service_name,
 (case when upper(t.adr) like '%НОВЫЙ У%' then 58
       when upper(t.adr) like '%КРАСНОСЕЛЬКУП%' then 59
       when upper(t.adr) like '%САЛЕХАРД%' then 60
       when upper(t.adr) like '%ЛАБЫТНАНГ%' then 62
       when upper(t.adr) like '%ХАРП%' then 62
       when upper(t.adr) like '%ПРИУРАЛ%' then 61
       when upper(t.adr) like '%НАДЫМ%' then 63
       when upper(t.adr) like '%ГУБК%' then 64
       when upper(t.adr) like '%ПУРПЕ%' then 64
       when upper(t.adr) like '%МУРАВ%' then 65
       when upper(t.adr) like '%НОЯБ%' then 66
       when upper(t.adr) like '%ПУРОВСК%' then 67
       when upper(t.adr) like '%ЯМАЛЬ%' then 68
       when upper(t.adr) like '%ШУРЫШ%' then 69
       when upper(t.adr) like '%МУЖИ%' then 69
       when upper(t.adr) like '%ТАЗ%' then 70
   else 0 end) as mo_out
from
(select
  r.region_id||'-'||r.pc_id as pc_id,
  r.region_id,
  r.id,
  uszn.pkXMLUtils.GUIDToStr(r.message_guid) as message_guid,
  
  (select
 NVL(uszn.pkPerson.GetPersonalReq(region_id, id, 15),
    (select value from uszn.all_personal_doc_reqs
      where region_id=pc.region_id and pdoc_id=uszn.pkPerson.GetMainPersonIdentity(pc.region_id, pc.id, 0) and class_id=8434))
 from uszn.v_people_and_colls pc
 where pc.region_id=r.region_id and pc.id=r.pc_id) as adr,
 
 r.request_pdoc_id,
 r.smev_message_id,
 r.state_service_name

from
  uszn.all_ssvc_requests r
where
  r.region_id=71 and r.date_created>=To_Date('01.01.2022') and
  (r.state_svc_region_id,r.state_svc_id) in ((104, 3),(104, 5),(104, 6),(104, 7),(104, 8),(104,10),(104,11),(104,25),(104,16),
                                             (104,12),(104,20),(104,21),(104,24),(104,26),(104,28),
                                             (104,29),(104,34),(104,35),(104,37),(104,38),(104,39),(104,40),
                                             (104,13),(104,14))
  and r.request_origin_id in (2,5,1,4) and r.status_id not in (40,50)
  and r.smev3_inc_message_id is null
  and r.is_test_request=0
  and r.data_kind_id is null
  and upper(r.case_number) not like ('%TEST%')) t''')
    
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
        

        name_log = f'Alarm sql - {log}'
        writing_to_log_file(name_log, text)
        send_email(mail, name_log, msg_text=text)
        return 0

#***************************************************************    
def not_correct_GU_MSP_transfer(df):
    for row in df.itertuples(index=False):
        if row[8] != 0:
            pc_id = row[0]
            region_id = row[1]
            id = row[2]
            message_guid = row[3]
            adr = row[4]
            request_pdoc_id = row[5]
            smev_message_id = row[6]
            state_service_name = row[7]
            mo_out = row[8]
            
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
            
            name_log = 'not_correct_GU_MSP'
            mail = 'IVAbdulganiev@yanao.ru'

            resume = ararm_sql(sql1, sql2, sql3, name_log, mail)

            if resume == 1:
                text = f'Заявитель {pc_id} c МСП {state_service_name} перенесен в {mo_out}, его адрес {adr}'

                writing_to_log_file(name_log, text)
                send_email(mail, name_log, msg_text=text)
        else:
            text = f'Заявитель {pc_id} c МСП {state_service_name} - проблема с адресом - {adr}'
            name_log = '!!! not_correct_GU_MSP'
            mail = 'IVAbdulganiev@yanao.ru'
            
            writing_to_log_file(name_log, text)
            send_email(mail, name_log, msg_text=text)

#***************************************************************

data = not_correct_GU_MSP()
df = pd.DataFrame(data)

if len(set(data['pc_id'])) > 0:
    not_correct_GU_MSP_transfer(df)
else:
    text = 'Некорретных заявлений МСП нет'
    name_log = 'not_correct_GU_MSP'
    mail = 'IVAbdulganiev@yanao.ru'

    writing_to_log_file(name_log, text)
    send_email(mail, name_log, msg_text=text)
