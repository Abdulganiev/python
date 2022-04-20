import jaydebeapi
import json
from datetime import datetime
from smtp import *
import shutil
import pandas as pd

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
def log(file):
  log = "egr_zagz.log"
  day = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

  with open(f'log/{log}', 'a') as f:
      f.write('**********************************************\n')
      f.write(f'{day}\n')
      f.write(f'{file}\n')

#***************************************************************
def zags_sm():
    curs.execute('''begin
  uszn.pkXMLImp.ClearParsedXMLData(0);
  for msg in (
      select id, uszn.pkEgrZags.DirectiveDeathToRiurXML(id) as data
        from uszn.r_smev3_inc_messages
        where
          message_kind_id=1 and /* запрос */
          data_kind_region_id=0 and data_kind_id in (16, 28) and /* Регистрация смерти */
          Trunc(date_created, 'dd') between ADD_MONTHS(TRUNC(sysdate,'mm'),-1) and sysdate)
  loop
    uszn.pkXMLImp.ParseXMLData(msg.data, 0, 0, 0, 30, msg.id);
  end loop;
  uszn.pkXMLImp.AnalyzeParsedXMLData;
end;''')
        
    curs.execute('''
select 
  '0'||pc.region_id||'-'||uszn.pkTSrv.GetRegionName(pc.region_id)||' - список умерших',
  pc.region_id||'-'||pc.id,
  pc.id,
  uszn.pkPerson.DescribeManColl(pc.region_id, pc.id, 0),
  pc.death_date,
  pc.close_date,
  z.F||' '||z.I||' '||z.O||' '||z.DR,
  z.ds,
  z.ds2,
  z.d_akt,
  z.n_akt
from
 uszn.v_people_and_colls pc,
(select distinct last_name as f, first_name as i, middle_name as o,
         uszn.pkXML.StrToDate(birth_date) as dr,
         uszn.pkXML.StrToDate(death_date) as ds, death_date as ds2, record_date as d_akt, record_num as n_akt
from
  (select fn.value as first_name, mn.value as middle_name, ln.value as last_name,
          bd.value as birth_date, dd.value as death_date, uszn.pkXML.StrToDate(dz.value) as record_date, nz.value as record_num
     from uszn.r$_parsed_xml_data rec, uszn.r$_parsed_xml_data dz, uszn.r$_parsed_xml_data nz, uszn.r$_parsed_xml_data st,
          uszn.r$_parsed_xml_data fn, uszn.r$_parsed_xml_data mn, uszn.r$_parsed_xml_data ln, uszn.r$_parsed_xml_data bd, uszn.r$_parsed_xml_data dd
     where rec.name='regDeath' and  st.value!='03' and -- исключаем записи "Аннулирование записи"
           dz.owner_id=rec.id and dz.name='recDate' and nz.owner_id=rec.id and nz.name='recNum' and st.owner_id=rec.id and st.name='recStatus' and
           fn.owner_id(+)=rec.id and fn.name(+)='firstName' and mn.name(+)='middleName' and mn.owner_id(+)=rec.id and ln.name(+)='lastName' and ln.owner_id(+)=rec.id and
           bd.name(+)='birthDate' and bd.owner_id(+)=rec.id and dd.name(+)='deathDate' and dd.owner_id(+)=rec.id)) z
where
    Translate(Upper(pc.last_name), 'Ё', 'Е')=Translate(Upper(z.F), 'Ё', 'Е') and
    Translate(Upper(pc.first_name), 'Ё', 'Е')=Translate(Upper(z.I), 'Ё', 'Е') and
    Translate(Upper(pc.middle_name), 'Ё', 'Е')=Translate(Upper(z.O), 'Ё', 'Е') and
    pc.birth_date=z.DR and pc.death_date is null''')
    
    data = {
         'район' : [],
         'id+МО' : [] ,
         'id человека' : [] ,
         'ФИО и д.р' : [] ,
         'Дата смерти' : [] ,
         'Дата снятия с учёта' : [],
         'ФИО и д.р из свидетельства' : [],
         'Дата смерти из свидетельства' : [],
         'Дата смерти 2 из свидетельства' : [],
         'Дата акта свидетельства' : [],
         'Номер акта свидетельства' : [],
        }
    
    for row in curs.fetchall():
        data['район'].append(row[0])
        data['id+МО'].append(row[1])
        data['id человека'].append(row[2])
        data['ФИО и д.р'].append(row[3])
        data['Дата смерти'].append(row[4])
        data['Дата снятия с учёта'].append(row[5])
        data['ФИО и д.р из свидетельства'].append(row[6])
        data['Дата смерти из свидетельства'].append(row[7])
        data['Дата смерти 2 из свидетельства'].append(row[8])
        data['Дата акта свидетельства'].append(row[9])
        data['Номер акта свидетельства'].append(row[10])
    
    df = pd.DataFrame(data)
    return df

#***************************************************************

data = zags_sm()

files = ''

mo = set(data['район'])
for row in mo:
    file = row + '.xlsx'
    data[data['район'].isin([row])].to_excel(file, index=False)
    path = 'c:/VipoNet_out/'
    shutil.move(file, path)
    files += file + '\n'

log(files)

send_email('IVAbdulganiev@yanao.ru', 'Данные ЕГР ЗАГС в МО отправлены', msg_text=files)