import jaydebeapi
import json
from generating_report_files import *


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
def not_correct_to_assign():
    curs.execute('''
select
    '0'||per.region_id||'-'||uszn.pkTSrv.GetRegionName(per.region_id)||' - МСП с не правильным сроком назначения - дата ПО' as name,
    per.pka_region_id as mo, -- МО
    per.pka_region_id||'-'||per.pka_people_coll_id, -- ID человека
    per.pka_people_coll_desc, -- Описание субъекта назначения
    per.pka_kind_name, -- Вид выплаты
    per.date_end -- Дата ПО
from uszn.all_asg_periods per, uszn.all_asg_amounts pk
where pk.rai_region_id=per.region_id and pk.rai_period_id=per.assigned_id  and per.pka_is_external=0 and
(per.pka_kind_id, per.pka_kind_region_id) in
                             ((133,0),(22,0),(134,0),(147,0),(132,0),(104,0),(241,104),(76,104),(21,104),(80,104),(23,104),(78,104),
                              (81,104),(14,104),(141,0),(140,0),(139,0),(99,0),(103,0),(98,0),(102,0),(138,0),(175,0),(150,0),(202,104),
                              (203,104),(204,104),(205,104),(160,0),(142,0),(137,0),(29,104),(53,104),(268,104),(75,104),(58,104),(57,104),
                              (51,0),(165,0),(201,0),(164,0),(170,0),(58,0),(161,0),(48,0),(122,0),(112,104),(213,104),(63,104),(61,104),
                              (56,104),(206,104),(66,104),(88,104),(89,104),(11,104),(51,104),(50,104),(136,0),(110,0),(149,0),(151,0),(179,0),
                              (37,0),(24,0),(224,0),(119,0),(46,0),(178,0),(40,0),(38,0),(207,0),(2,0),(67,104),(47,104),(261,104),(211,104),
                              (153,0),(112,0),(152,0),(101,0),(210,104),(9,104),(18,104),(24,104),(25,104),(20,104),(19,104),(84,104),(5,104),
                              (16,104),(83,104),(15,104),(70,104),(69,104),(49,104),(17,104),(60,104),(212,104),(55,104),(54,104),(28,104),
                              (27,104),(13,104),(52,104),(10,104),(4,104),(2,104),(7,104),(48,104),(272,104),(224,104),(225,104),(271,104),(223,104),
                              (222,104),(243,104),(244,104),(249,104),(248,104),(247,104),(245,104),(246,104),(260,104),(234,104),(230,104),(231,104),
                              (232,104),(227,104),(233,104),(236,104),(235,104),(237,104),(257,104),(254,104),(256,104),(255,104),(251,104),(252,104),
                              (259,104),(253,104),(258,104),(166,0),(155,0),(135,0),(172,0),(173,0),(176,0),(205,0),(167,0),(177,0),(148,0),(157,0),
                              (129,0),(168,0),(77,104),(12,104),(32,104),(31,104),(30,104),(62,104),(266,104),(26,104),(207,104),(6,104))
and per.date_end between To_Date('01.12.2090') and To_Date('30.12.9999')
group by '0'||per.region_id||'-'||uszn.pkTSrv.GetRegionName(per.region_id)||' - МСП с не правильным сроком назначения - дата ПО',
         per.pka_region_id,per.pka_region_id||'-'||per.pka_people_coll_id, per.pka_people_coll_desc,per.pka_kind_name,date_end,'0'||per.region_id||'-'||uszn.pkTSrv.GetRegionName(per.region_id)||' - ÌÑÏ ñ íå ïðàâèëüíûì ñðîêîì íàçíà÷åíèÿ - äàòà ÏÎ'
order by 1,4,5''')
    
    data = {
         'name' : [],
         'МО' : [],
         'ID человека' : [],
         'Описание субъекта назначения' : [],
         'Вид выплаты' : [],
         'Дата ПО' : [],
        }
    
    for row in curs.fetchall():
        data['name'].append(row[0])
        data['МО'].append(row[1])
        data['ID человека'].append(row[2])
        data['Описание субъекта назначения'].append(row[3])
        data['Вид выплаты'].append(row[4])
        data['Дата ПО'].append(row[5])
        
    return data

#***************************************************************

data = not_correct_to_assign()

name_log = 'not_correct_to_assign'
name_def = 'МСП с неправильным сроком назначения'
test = 0
mail = 'IVAbdulganiev@yanao.ru'

generating_report_files(data, name_log, name_def, test, mail)

