select '0'||region_id||' - '||uszn.pkTSrv.GetRegionName(region_id)||' - изменилась карта МИР для ЭС - '||count(1) over(partition BY region_id) as name,
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
       and (t1.pka_kind_id, t1.pka_kind_region_id, t1.rai_item_id, t1.rai_item_region_id) in ((261,104,719,104))
       and (t2.cert_kind_region_id, t2.cert_kind_id) in ((104, 1)) -- новорожденные
       and sysdate between t2.date_start and t2.date_end and t2.cert_number is not null and t2.status_id in (1, 4)
       and uszn.pkPerson.GetDocReqValue(t1.region_id, 20162, uszn.pkPerson.GetPCReqValueInt(t1.region_id, t1.pka_payee_pc_id, 20903)) != t2.card_number
  union all
 select t1.region_id, t1.pka_kind_name,
        t1.pka_payee_pc_id, t1.pka_payee_pc_desc,
        t1.pka_people_coll_id, t1.pka_people_coll_desc,
        uszn.pkPerson.GetDocReqValue(t1.region_id, 20162, uszn.pkPerson.GetPCReqValueInt(t1.region_id, t1.pka_payee_pc_id, 20903)) as EKJYA,
        t2.card_number
 from uszn.all_asg_amounts t1 inner join uszn.all_fk_ecerts t2
    on t1.region_id=t2.region_id and t1.pka_payee_pc_id=t2.person_id and t1.id=t2.asg_amount_id
       and (t1.pka_kind_id, t1.pka_kind_region_id) in ((325,104))
       and (t2.cert_kind_region_id, t2.cert_kind_id) in ((104, 2)) -- молочка
       and sysdate between t2.date_start and t2.date_end and t2.cert_number is not null and status_id in (1, 4)
       and uszn.pkPerson.GetDocReqValue(t1.region_id, 20162, uszn.pkPerson.GetPCReqValueInt(t1.region_id, t1.pka_payee_pc_id, 20903)) != t2.card_number)
