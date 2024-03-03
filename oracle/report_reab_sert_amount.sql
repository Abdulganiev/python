create table uszn.temp$_r_reab_cert_inv_amount as

select t3.mo, t3.region_id, t3.people_id, t3.cert_date, t3.stop_time, t3.cert_nom, t3.cert_id,
       uszn.StrCommaConcat(distinct pka.pka_region_id||'-'||pka.pka_people_coll_id) as people_amount_id,
       uszn.StrCommaConcat(distinct pka.pka_people_coll_desc) as people_amount_desc,
       sum(poa.amount) as amount
    from uszn.r_personal_doc_reqs t2
         join
         uszn.v_pka_pk_assigned pka
     on pka.PKA_PEOPLE_COLL_ID=uszn.pkPerson.GetDocInstancePC(t2.pdoc_id, t2.region_id) and pka.pka_region_id=t2.region_id
        and t2.class_id=14741 and uszn.pkPerson.GetDocReqValue(t2.region_id, 14742, t2.pdoc_id) not like '%дубликат%'
         join
         uszn.v_po_amounts poa
     on poa.poi_region_id=pka.pka_region_id and poa.poi_assigned_id=pka.pka_id
        and pka.pka_kind_id=206 and pka.pka_kind_region_id=104 and poa.status_id in (103,107,104,101,102)
        join
         uszn.temp$_v_reab_cert_inv t3
  on uszn.pkPerson.GetBirthDate(t2.region_id, uszn.pkPerson.GetDocInstancePC(t2.pdoc_id, t2.region_id))||'-'||uszn.ToDateDef(t2.value)||'-'||uszn.pkPerson.GetDocReqValue(t2.region_id, 14740, t2.pdoc_id)=t3.cert_id
group by t3.mo, t3.region_id, t3.people_id, t3.cert_date, t3.stop_time, t3.cert_nom, t3.cert_id
