CREATE TABLE uszn.temp$_msk_cert
as
select c.*,
       to_char(c.app_date, 'yyyy') as app_year,
	   uszn.pkPerson.GetPersonalReq(c.region_id, c.people_id, 25) as snils,
	   uszn.pkXMLUtils.GuidToStr(uszn.pkJUtil.GetGUIDRAW(c.region_id*1000000 + c.people_id)) as people_guid,
		uszn.pkPerson.GetDocReqValue(c.region_id, 7732, c.num_zayav) as application_date,
		uszn.pkPerson.GetDocReqValue(c.region_id, 7749, c.num_zayav) as law,
		(case uszn.pkPerson.GetDocReqValue(c.region_id, 7749, c.num_zayav)
         when 'Второй ребенок c 01.01.2020' then 'на второго ребенка'
         when 'Женщина, до 31.12.2019 родившая (усыновившая) третьего ребёнка' then 'на третьего и последующих детей'
         when 'Женщина, до 31.12.2019 родившая (усыновившая) четвёртого ребёнка или последующих детей' then 'на третьего и последующих детей'
         when 'Женщина, с 01.01.2020 родившая (усыновившая) второго ребенка' then 'на второго ребенка'
         when 'Женщина, с 01.01.2020 родившая (усыновившая) третьего ребёнка или последующих детей' then 'на третьего и последующих детей'
         when 'Мужчина, с 01.01.2020 являющийся единственными усыновителями второго ребенка' then 'на второго ребенка'
         when 'Мужчина, являющийся единственным усыновителем третьего и последующих детей' then 'на третьего и последующих детей'
         when 'Третий и последующий ребенок' then 'на третьего и последующих детей' end) as law2,
		 uszn.pkPerson.GetDocReqValue(c.region_id, 7742, c.num_zayav) as decision,
		 uszn.pkPerson.GetDocReqValue(c.region_id, 7741, c.num_zayav) as decision_date,
		 uszn.pkPerson.GetDocReqValue(c.region_id, 7809, c.num_zayav) as amount,
		 
		 uszn.pkPerson.GetBirthDate(c.region_id, uszn.pkPerson.GetDocReqValueInt(c.region_id, 7754, c.num_zayav)) as baby_date_birth,
		 (select uszn.StrCommaConcat(uszn.pkGen.StripRgnPrefix(c2.value))
           from uszn.all_personal_doc_reqs c1, uszn.all_personal_doc_reqs c2
           where c1.class_id=7737 and c1.region_id=c.region_id and c1.pdoc_id=c.num_zayav and 
		         c1.value=uszn.pkPerson.GetDocReqValueInt(c.region_id, 7754, c.num_zayav) and
                 c2.class_id=7746 and c1.region_id=c2.region_id and c1.pdoc_id=c2.pdoc_id and c1.order_num=c2.order_num) as baby_account,
		 uszn.pkPerson.GetDocReqValue(c.region_id, 7754, c.num_zayav) as baby,
		 uszn.pkPerson.GetDocReqValue(c.region_id, 7757, c.iDIID) as certificate_date,
		 uszn.pkPerson.GetDocReqValue(c.region_id, 7755, c.iDIID)||'-'||uszn.pkPerson.GetDocReqValue(c.region_id, 7756, c.iDIID)||' от '||uszn.pkPerson.GetDocReqValue(c.region_id, 7757, c.iDIID) as SV
 from
(select
      c.region_id,
      (case uszn.pkPerson.GetDocReqValueInt(c.region_id, 7755, c.doc_instance_id)
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
       end) as MO,
      c.people_coll_id as people_id,
      c.doc_instance_id as iDIID,
      c.date_created  as iDate,
      uszn.ToDateDef(value) as app_date,
      uszn.pkPerson.GetDocReqValueInt(c.region_id, 7765, c.doc_instance_id) as num_zayav,
      uszn.pkTSrv.GetRegionName(c.region_id) as mo_name  
	  
    from uszn.r_personal_doc_instances c
        where c.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and c.class_id=7757 and
          uszn.ToDateDef(value) is not null and
          uszn.pkPerson.GetDocReqValue(c.region_id, 7767, c.doc_instance_id) is null) c
where c.region_id=c.mo