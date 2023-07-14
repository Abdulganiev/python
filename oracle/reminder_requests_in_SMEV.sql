select 
    '0'||region_id||' - '||'не сделаны запросы в СМЭВ для переходников на 3-7' as name,
    region_id||'-'||people_id,
    uszn.pkPerson.DescribeManColl(region_id, people_id, 0),
    region_id||'-'||coll_id,
    region_id||'-'||baby,
    region_id||'-'||payee,
    (case requesting when 1 then '' else 'Не создано обращение за ГУ, ' end)||
    (case EGISSO when 1 then '' else 'Запрос в ЕГИСО, ' end)||
    (case  AVTO when 1 then '' else 'Запрос в МВД об авто, ' end)||
    (case  FNS_vznos when 1 then '' else 'Запрос в ФНС о страховых взносах, ' end)||
    (case  FNS_3_ndfl when 1 then '' else 'Запрос в ФНС о справке 3-НДФЛ, ' end)||
    (case  FNS_agent when 1 then '' else 'Запрос в ФНС о начислениях агента' end)
        
from
(select c.region_id, c.people_id, c.role_class_id,  p.kind_name, p.pkaf_name, c.coll_id, p.people_id as baby, p.pka_payee_pc_id as payee,

(case when
  (select count(*) from uszn.r_personal_doc_instances d
    where d.doc_class_id=17368 and d.region_id=c.region_id and d.people_coll_id=c.people_id
          and d.date_created between trunc(ADD_MONTHS(sysdate, -1), 'mm') and trunc(ADD_MONTHS(sysdate, 1), 'mm'))>0
    then 1 else 0 end) as EGISSO, -- ïðîâåðêà ÅÃÈÑÑÎ,

(case when
  (select count(*) from uszn.r_personal_doc_instances d
    where d.doc_class_id=18277 and d.region_id=c.region_id and d.people_coll_id=c.people_id
          and d.date_created between trunc(ADD_MONTHS(sysdate, -1), 'mm') and trunc(ADD_MONTHS(sysdate, 1), 'mm'))>0
          or c.role_class_id=10
    then 1 else 0 end) as zak_brak,

(case when
  (select count(*) from uszn.r_personal_doc_instances d
    where d.doc_class_id=18331 and d.region_id=c.region_id and d.people_coll_id=c.people_id
          and d.date_created between trunc(ADD_MONTHS(sysdate, -1), 'mm') and trunc(ADD_MONTHS(sysdate, 1), 'mm'))>0
   or
  (select count(*) from uszn.r_personal_doc_instances d
    where d.doc_class_id=15213 and d.region_id=c.region_id and d.people_coll_id=c.people_id
          and d.date_created between trunc(ADD_MONTHS(sysdate, -1), 'mm') and trunc(ADD_MONTHS(sysdate, 1), 'mm'))>0
    then 1 else 0 end) as sm,

(case when
  (select count(*) from uszn.r_personal_doc_instances d
    where d.doc_class_id=18218 and d.region_id=c.region_id and d.people_coll_id=c.people_id
          and d.date_created between trunc(ADD_MONTHS(sysdate, -1), 'mm') and trunc(ADD_MONTHS(sysdate, 1), 'mm'))>0
          or Floor(Months_Between(sysdate, uszn.pkPerson.GetBirthDate(c.region_id, c.people_id))/12)<6
    then 1 else 0 end) as AVTO,

(case when
  (select count(*) from uszn.r_personal_doc_instances d
    where d.doc_class_id=17466 and d.region_id=c.region_id and d.people_coll_id=c.people_id
          and d.date_created between trunc(ADD_MONTHS(sysdate, -1), 'mm') and trunc(ADD_MONTHS(sysdate, 1), 'mm'))>0
    then 1 else 0 end) as FNS_vznos,

(case when
  (select count(*) from uszn.r_personal_doc_instances d
    where d.doc_class_id=17482 and d.region_id=c.region_id and d.people_coll_id=c.people_id
          and d.date_created between trunc(ADD_MONTHS(sysdate, -1), 'mm') and trunc(ADD_MONTHS(sysdate, 1), 'mm'))>0
    then 1 else 0 end) as FNS_3_ndfl,

(case when
  (select count(*) from uszn.r_personal_doc_instances d
    where d.doc_class_id=1766 and d.region_id=c.region_id and d.people_coll_id=c.people_id
          and d.date_created between trunc(ADD_MONTHS(sysdate, -1), 'mm') and trunc(ADD_MONTHS(sysdate, 1), 'mm'))>0
    then 1 else 0 end) as FNS_agent,

(case when
   (select count(*) from uszn.all_ssvc_requests d
     where d.region_id=c.region_id and d.pc_id=p.pka_payee_pc_id and
     d.request_date between trunc(ADD_MONTHS(sysdate, -1), 'mm') and trunc(ADD_MONTHS(sysdate, 1), 'mm') and
     d.is_test_request=0 and (d.state_svc_variant_id, d.state_svc_region_id) in ((106,104)))>0
     or p.pka_payee_pc_id!=c.people_id
    then 1 else 0 end) as requesting

from uszn.v_coll_membership_periods c,

(select pk.region_id,
        pk.pka_people_coll_id as people_id,
        pk.pka_kind_name as kind_name,
        pk.pkaf_name,
        Floor(Months_Between(sysdate, uszn.pkPerson.GetBirthDate(pk.region_id, pk.pka_people_coll_id))/12) as age,
        uszn.pkPerson.GetBirthDate(pk.region_id, pk.pka_people_coll_id) as dr,
        pk.pka_payee_pc_id,
        (select c.coll_id from uszn.v_coll_membership_periods c
              where c.people_id=pk.pka_people_coll_id and c.region_id=pk.region_id and c.role_class_id=10 and sysdate between date_start and date_end) as coll_id

    from uszn.all_asg_items pk
    where --pk.region_id=61 and
          (pk.pka_kind_id, pk.pka_kind_region_id) in ((211,104)) and (pk.pkaf_region_id, pk.pkaf_id) not in ((104,982),(104,1006))
          and pk.pka_is_enabled=1 and pk.pka_status_num=0 and sysdate between pk.rap_date_start and pk.rap_date_end+1

          and 3 between Floor(Months_Between(last_day(ADD_MONTHS(sysdate, 1)), uszn.pkPerson.GetBirthDate(pk.region_id,pk.pka_people_coll_id))/12)  /*ïðîâåðêà âîçðàñòà 3 ãîäà â ñëåäóþùåì ìåñÿöå*/
                    and Floor(Months_Between(trunc(ADD_MONTHS(sysdate, 1), 'mm'), uszn.pkPerson.GetBirthDate(pk.region_id, pk.pka_people_coll_id))/12)

          and Floor(Months_Between(sysdate, uszn.pkPerson.GetBirthDate(pk.region_id,pk.pka_people_coll_id))/12)<3 /*ñåé÷àñ äîëæåí áûòü ìëàäøå 3 ëåò*/ ) p

where c.coll_id=p.coll_id and c.region_id=p.region_id and sysdate between c.date_start and c.date_end)

where EGISSO!=1 or /*zak_brak!=1 or sm!=1 or*/ AVTO!=1 or FNS_vznos!=1 or FNS_3_ndfl!=1 or FNS_agent!=1 or requesting!=1