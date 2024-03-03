select
  pc.region_id,
  '0'||pc.region_id||' - '||uszn.pkTSrv.GetRegionName(pc.region_id)||' - неправильная дата выдачи ДУЛ - '||count(1) over(partition BY pc.region_id) as name,
  '0'||pc.region_id||' - '||uszn.pkTSrv.GetRegionName(pc.region_id) as MO,
   pc.people_id,
   pc.pc_desc,
   pc.birth_date,
   pc.dul_date,
   case when pc.identity_doc_class_id=4 and pc.dul_date_check<(13+(10/12)) then 'меньше 13 лет и 10 месяцев'
        when pc.dul_date_check<0 then 'Дата выдачи ДУЛ раньше даты рождения' end as chk
 from uszn.temp$_mnogo_people pc
 where (pc.identity_doc_class_id=4 and pc.dul_date_check<(13+(10/12))) or pc.dul_date_check<0
