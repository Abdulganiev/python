select 'begin'||chr(10)||kod||chr(10)||'end;'
from
(
select 'uszn.pkFkEcert.ECert_Edit('||t2.region_id||','||t2.id||');' as kod
 from uszn.all_asg_amounts t1 inner join uszn.all_fk_ecerts t2
    on t1.region_id=t2.region_id and t1.pka_payee_pc_id=t2.person_id and t1.id=t2.asg_amount_id
       and uszn.pkPerson.GetDocReqValue(t1.region_id, 20162, t1.pka_pw_doc_id) != t2.card_number
       and (t1.pka_kind_id, t1.pka_kind_region_id, t1.rai_item_id, t1.rai_item_region_id) in ((261,104,719,104))
       and (t2.cert_kind_region_id, t2.cert_kind_id) in ((104, 1))
       and sysdate between t2.date_start and t2.date_end and t2.cert_number is not null and status_id in (1, 4)
  union all
select 'uszn.pkFkEcert.ECert_Edit('||t2.region_id||','||t2.id||');' as kod
 from uszn.all_asg_amounts t1 inner join uszn.all_fk_ecerts t2
    on t1.region_id=t2.region_id and t1.pka_payee_pc_id=t2.person_id and t1.id=t2.asg_amount_id
       and uszn.pkPerson.GetDocReqValue(t1.region_id, 20162, t1.pka_pw_doc_id) != t2.card_number
       and (t1.pka_kind_id, t1.pka_kind_region_id) in ((325,104))
       and (t2.cert_kind_region_id, t2.cert_kind_id) in ((104, 2))
       and sysdate between t2.date_start and t2.date_end and t2.cert_number is not null and status_id in (1, 4)
)