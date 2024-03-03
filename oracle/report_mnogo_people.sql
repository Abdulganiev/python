create table uszn.temp$_mnogo_people as
select pc.region_id, pc.id, pc.pc_desc,
       pc.region_id||'-'||pc.id as people_id,
       pc.birth_date,
       Floor(Months_Between(sysdate, pc.birth_date)/12) as age,
       pc.sex,
       pc.snils_formatted as snils,
       uszn.pkPerson.GetRawPCReqValue(pc.region_id, pc.id, 4280) as INN,
       pc.identity_doc_class_id,
       uszn.pkPerson.GetPersonalReq(pc.region_id, pc.id, 23) as dul_date,
       floor(MONTHS_BETWEEN(uszn.pkPerson.GetPersonalReq(pc.region_id, pc.id, 23), pc.birth_date)/12) as delta_year,
       floor(mod(months_between(uszn.pkPerson.GetPersonalReq(pc.region_id, pc.id, 23), pc.birth_date),12)) as delta_mm,
       
       (floor(MONTHS_BETWEEN(uszn.pkPerson.GetPersonalReq(pc.region_id, pc.id, 23), pc.birth_date)/12) +
          (case when floor(mod(months_between(uszn.pkPerson.GetPersonalReq(pc.region_id, pc.id, 23), pc.birth_date),12))=0 then 0
                else floor(mod(months_between(uszn.pkPerson.GetPersonalReq(pc.region_id, pc.id, 23), pc.birth_date),12))/12 end)) as dul_date_check,
       
       c1.date_start, c1.date_end
      from uszn.r_categories_assigned c1
           join
           uszn.v_people_and_colls pc
      on c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
         and c1.pc_region_id=pc.region_id and c1.pc_id=pc.id
         and sysdate between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((1058,0))