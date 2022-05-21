import jaydebeapi
import json
import pandas as pd
from writing_to_log_file import *
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


#***************************************************************
def not_correct_GU_PGS():
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
 r.smev3_inc_message_id as smev_message_id,
 r.state_service_name

from
  uszn.all_ssvc_requests r
  inner join
  uszn.all_smev3_data_kinds t2
on
  r.region_id=71 and r.date_created>=To_Date('01.01.2022') and
  r.data_kind_region_id=t2.region_id and r.data_kind_id=t2.id
  and r.status_id in (1, 2, 3, 4, 10, 20, 30, 40)
  and (r.region_id, r.id) not in
      ((104, 1), (104, 2), (104, 18), (104, 27), (104, 30), (104, 9),
       (104, 31), (104, 13), (104, 14), (104, 15), (104, 19), (104, 17), (104, 32))
  and pc_id != 140264 ) t''')
    
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
    try:
        curs.execute(sql)
        return 1
    except:
        text = f'ошибка \n {sql}'
        name_log = f'Alarm sql - {log}'
        writing_to_log_file(name_log, text)
        send_email(mail, name_log, msg_text=text)
        return 0    

#***************************************************************
def not_correct_GU_PGS_transfer(df):
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
            name_log = 'not_correct_GU_PGS'
            mail = 'IVAbdulganiev@yanao.ru'

            resume = ararm_sql(sql, name_log, mail)
            if resume == 1:
                text = f'Заявитель {pc_id} c ПГС {state_service_name} перенесен в {mo_out}, его адрес {adr}'
                writing_to_log_file(name_log, text)
                send_email(mail, name_log, msg_text=text)
        else:
            text = f'Заявитель {pc_id} c ПГС {state_service_name} - проблема с адресом - {adr}'
            name_log = '!!! not_correct_GU_PGS'
            mail = 'IVAbdulganiev@yanao.ru'
            
            writing_to_log_file(name_log, text)
            send_email(mail, name_log, msg_text=text)

#***************************************************************

data = not_correct_GU_PGS()
df = pd.DataFrame(data)

if len(set(data['pc_id'])) > 0:
    not_correct_GU_PGS_transfer(df)
else:
    text = 'Некорретных заявлений ПГС нет'
    name_log = 'not_correct_GU_PGS'
    mail = 'IVAbdulganiev@yanao.ru'

    writing_to_log_file(name_log, text)
    send_email(mail, name_log, msg_text=text)
