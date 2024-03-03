create table uszn.temp$_baby_3 as

select distinct
        pc.region_id,
        pc.coll_id,
        pc.people_id as id,
        pic1.people_id as mam_id,
        pic2.people_id as pap_id,
        (select distinct 1 from uszn.all_personal_doc_reqs d1
           where d1.region_id=pc.region_id and d1.pd_pc_id in (pic1.people_id, pic2.people_id)
                 and d1.pd_class_id=18899
                 and d1.class_id=20903
                 ) as karta,
        uszn.pkPCAddr.GetPCAddress(pc.region_id, pc.people_id, 1, null, SYSDATE, 0) as adr
   from uszn.v_coll_membership_periods pc
        left join uszn.v_coll_membership_periods pic1
     on pc.coll_id=pic1.coll_id and pc.region_id=pic1.region_id
         and pc.role_class_id=10
         and pic1.role_class_id=8
         and trunc(SYSDATE, 'mm') between pic1.date_start and pic1.date_end and pic1.role_class_id=8
        left join uszn.v_coll_membership_periods pic2
     on pc.coll_id=pic2.coll_id and pc.region_id=pic2.region_id
         and trunc(SYSDATE, 'mm') between pic2.date_start and pic2.date_end and pic2.role_class_id=9
         and pic2.role_class_id=9
   where pc.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
         and Floor(Months_Between(trunc(to_date('01.01.2024'), 'mm'), uszn.pkPerson.GetBirthDate(pc.region_id, pc.people_id))/12) between 0 and 2
         and trunc(SYSDATE, 'mm') between pc.date_start and pc.date_end
         and pc.coll_class_id=6