select 'ДО - изменилась карта МИР для ЭС - '||count(1) over() as name,
       pka_kind_name,
       region_id||'-'||pka_payee_pc_id,
       pka_payee_pc_desc,
       region_id||'-'||pka_people_coll_id,
       pka_people_coll_desc,
       EKJYA,
       card_number
from
(select t1.region_id, t1.pka_kind_name,
        t1.pka_payee_pc_id, t1.pka_payee_pc_desc,
        t1.pka_people_coll_id, t1.pka_people_coll_desc,
        uszn.pkPerson.GetDocReqValue(t1.region_id, 20162, uszn.pkPerson.GetPCReqValueInt(t1.region_id, t1.pka_payee_pc_id, 20903)) as EKJYA,
        t2.card_number
 from uszn.all_asg_amounts t1 inner join uszn.all_fk_ecerts t2
    on t1.region_id=t2.region_id and t1.pka_payee_pc_id=t2.person_id and t1.id=t2.asg_amount_id
       and (t1.pka_kind_id, t1.pka_kind_region_id) in ((357,104))
       and (t2.cert_kind_region_id, t2.cert_kind_id) in ((104, 3)) -- студенты
       and sysdate between t2.date_start and t2.date_end and t2.cert_number is not null and status_id in (1, 4)
       and uszn.pkPerson.GetDocReqValue(t1.region_id, 20162, uszn.pkPerson.GetPCReqValueInt(t1.region_id, t1.pka_payee_pc_id, 20903)) != t2.card_number)
