create table uszn.temp$_msk_resh as
(select
  region_id,
  region_id||'-'||people_id as id,
  uszn.pkPerson.GetDocReqValue(region_id, 7749, uszn.pkPerson.GetDocReqValueInt(region_id, 7765, svid)) as  law,
  (case uszn.pkPerson.GetDocReqValue(region_id, 7749, uszn.pkPerson.GetDocReqValueInt(region_id, 7765, svid))
     when 'Второй ребенок c 01.01.2020' then 'на второго ребенка'
     when 'Женщина, до 31.12.2019 родившая (усыновившая) третьего ребёнка' then 'на третьего и последующих детей'
     when 'Женщина, до 31.12.2019 родившая (усыновившая) четвёртого ребёнка или последующих детей' then 'на третьего и последующих детей'
     when 'Женщина, с 01.01.2020 родившая (усыновившая) второго ребенка' then 'на второго ребенка'
     when 'Женщина, с 01.01.2020 родившая (усыновившая) третьего ребёнка или последующих детей' then 'на третьего и последующих детей'
     when 'Мужчина, с 01.01.2020 являющийся единственными усыновителями второго ребенка' then 'на второго ребенка'
     when 'Мужчина, являющийся единственным усыновителем третьего и последующих детей' then 'на третьего и последующих детей'
     when 'Третий и последующий ребенок'then 'на третьего и последующих детей'end) as law2,
  to_date(data_obr) as data_obr,
  resh,
  to_date(data_resh) as data_resh,
  vid_resh,
  summa_resh,
  uszn.pkPerson.GetDocReqValue(region_id, 7755, svid)||'-'||uszn.pkPerson.GetDocReqValue(region_id, 7756, svid)||' от '||uszn.pkPerson.GetDocReqValue(region_id, 7757, svid) as SV,
  to_date(uszn.pkPerson.GetDocReqValue(region_id, 7757, svid)) as SV_data,
  uszn.pkPerson.GetDocReqValue(region_id, 7755, svid) as SV_ser,
  (case uszn.pkPerson.GetDocReqValueInt(region_id, 7755, svid)
        when 104000443 then 58
        when 104000446 then 59
        when 104000447 then 60
        when 104000448 then 61
        when 104000449 then 62
        when 104000450 then 63
        when 104000451 then 64
        when 104000452 then 65
        when 104000453 then 66
        when 104000454 then 67
        when 104000455 then 68
        when 104000456 then 69
        when 104000457 then 70
       end) as id_MO_sert,
  (case uszn.pkPerson.GetDocReqValueInt(region_id, 7755, svid)
        when 104000443 then 'г. Новый Уренгой'
        when 104000446 then 'Красноселькупский район'
        when 104000447 then 'г. Салехард'
        when 104000448 then 'Приуральский район'
        when 104000449 then 'г. Лабытнанги'
        when 104000450 then 'Надымский район'
        when 104000451 then 'г. Губкинский'
        when 104000452 then 'г. Муравленко'
        when 104000453 then 'г. Ноябрьск'
        when 104000454 then 'Пуровский район'
        when 104000455 then 'Ямальский район'
        when 104000456 then 'Шурышкарский район'
        when 104000457 then 'Тазовский район'
       end) as MO_sert,	   
  uszn.pkPerson.GetDocReqValue(region_id, 7756, svid) as SV_num,
  uszn.pkPerson.GetDocReqValue(region_id, 7754, uszn.pkPerson.GetDocReqValueInt(c.region_id, 7765, svid)) as baby,
  region_id||'-'||svid as sv_id,
  region_id||'-'||uszn.pkPerson.GetDocReqValueInt(region_id, 7765, svid) as zayav_id,
  directed,
  to_char(to_date(data_resh), 'yyyy') as year_resh
from
  (select region_id,
             people_coll_id as people_id,
             doc_instance_id as iDIID,
             date_created as iDate,
             uszn.ToDateDef(value) as app_date,
             uszn.pkPerson.GetDocReqValue(region_id, 7800, doc_instance_id) as resh,
             uszn.pkPerson.GetDocReqValueDate(region_id, 7793, doc_instance_id) as data_obr,
             uszn.pkPerson.GetDocReqValueDate(region_id, 7799, doc_instance_id) as data_resh,
             uszn.pkPerson.GetDocReqValue(region_id, 7795, doc_instance_id) as vid_resh,
             uszn.pkPerson.GetDocReqValueNumber(region_id, 7796, doc_instance_id) as summa_resh,
             uszn.pkPerson.GetDocReqValueInt(region_id, 7794, doc_instance_id) as svid,
             uszn.pkPerson.GetDocReqValueInt(region_id, 7749, uszn.pkPerson.GetDocReqValueInt(region_id, 7794, doc_instance_id)) as zayav,
             'Медицина' as directed
         from uszn.r_personal_doc_instances
         where region_id not in (104,72) and class_id=7799 and doc_class_id=7787 and uszn.ToDateDef(value) between To_Date('01.01.2000') and sysdate
       union
   select region_id,
             people_coll_id as people_id,
             doc_instance_id as iDIID,
             date_created as iDate,
             uszn.ToDateDef(value) as app_date,
             uszn.pkPerson.GetDocReqValue(region_id, 7778, doc_instance_id) as resh,
             uszn.pkPerson.GetDocReqValueDate(region_id, 7773, doc_instance_id) as data_obr,
             uszn.pkPerson.GetDocReqValueDate(region_id, 7777, doc_instance_id) as data_resh,
             uszn.pkPerson.GetDocReqValue(region_id, 7782, doc_instance_id) as vid_resh,
             uszn.pkPerson.GetDocReqValueNumber(region_id, 7783, doc_instance_id) as summa_resh,
             uszn.pkPerson.GetDocReqValueInt(region_id, 7774, doc_instance_id) as svid,
             uszn.pkPerson.GetDocReqValueInt(region_id, 7749, uszn.pkPerson.GetDocReqValueInt(region_id, 7774, doc_instance_id)) as zayav,
             'Улучшение жилищных условий' as directed
          from uszn.r_personal_doc_instances
          where region_id not in (104,72) and class_id=7777 and doc_class_id=7753 and uszn.ToDateDef(value) between To_Date('01.01.2000') and sysdate
       union
   select region_id,
            people_coll_id as people_id,
            doc_instance_id as iDIID,
            date_created as iDate,
            uszn.ToDateDef(value) as app_date,
            uszn.pkPerson.GetDocReqValue(region_id, 9078, doc_instance_id) as resh,
            uszn.pkPerson.GetDocReqValueDate(region_id, 9066, doc_instance_id) as data_obr,
            uszn.pkPerson.GetDocReqValueDate(region_id, 9077, doc_instance_id) as data_resh,
            uszn.pkPerson.GetDocReqValue(region_id, 9069, doc_instance_id) as vid_resh,
            uszn.pkPerson.GetDocReqValueNumber(region_id, 9070, doc_instance_id) as summa_resh,
            uszn.pkPerson.GetDocReqValueInt(region_id, 9068, doc_instance_id) as svid,
            uszn.pkPerson.GetDocReqValueInt(region_id, 7749, uszn.pkPerson.GetDocReqValueInt(region_id, 9068, doc_instance_id)) as zayav,
           'Единовременное 55-ЗАО от 26.05.2015' as directed
          from uszn.r_personal_doc_instances where region_id not in (104,72) and class_id=9077 and doc_class_id=8966 and uszn.ToDateDef(value) between To_Date('01.01.2000') and sysdate
        union
   select region_id,
             people_coll_id as people_id,
             doc_instance_id as iDIID,
             date_created as iDate,
             uszn.ToDateDef(value) as app_date,
             uszn.pkPerson.GetDocReqValue(region_id, 17418, doc_instance_id) as resh,
             uszn.pkPerson.GetDocReqValueDate(region_id, 17404, doc_instance_id) as data_obr,
             uszn.pkPerson.GetDocReqValueDate(region_id, 17417, doc_instance_id) as data_resh,
             uszn.pkPerson.GetDocReqValue(region_id, 17409, doc_instance_id) as vid_resh,
             uszn.pkPerson.GetDocReqValueNumber(region_id, 17410, doc_instance_id) as summa_resh,
             uszn.pkPerson.GetDocReqValueInt(region_id, 17407, doc_instance_id) as svid,
             uszn.pkPerson.GetDocReqValueInt(region_id, 7749, uszn.pkPerson.GetDocReqValueInt(region_id, 17407, doc_instance_id)) as zayav,
             'Единовременное 35-ЗАО от 15.04.2020' as directed
           from uszn.r_personal_doc_instances where region_id not in (104,72) and class_id=17404 and doc_class_id=17402 and uszn.ToDateDef(value) between To_Date('01.01.2000') and sysdate
        )c
      where (data_obr >= to_date('01.01.2021') and region_id != 71) or (data_obr < to_date('01.01.2021') and region_id = 71) )