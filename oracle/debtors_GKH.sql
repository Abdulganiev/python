select 
    pc.region_id,
    '0'||pc.region_id||' - '||uszn.pkTSrv.GetRegionName(pc.region_id)||' наличие задолженности в ГИС ЖКХ в '||to_char(sysdate, 'yyyy-mm') as region_id_desc,
	--'0'||pc.region_id||' - '||uszn.pkTSrv.GetRegionName(pc.region_id)||' наличие задолженности в ГИС ЖКХ в 2023-01' as region_id_desc,
    pc.id,
    c.pdoc_id,
    pc.snils_formatted as snils,
    c.adr,
    TRIM(c.request_F||' '||c.request_I||' '||c.request_O) as request,
    TRIM(c.response_F||' '||c.response_I||' '||c.response_O) as response,
    c.org,
    c.org_tel
from
(select t1.region_id,
        t1.pd_pc_id as id,
        t1.pdoc_id,
        uszn.pkPerson.GetDocReqValue(t1.region_id, 18415, t1.pdoc_id) as adr,
        t2.decoded_value as org,
        t3.decoded_value as org_tel,
        uszn.pkPerson.GetDocReqValue(t1.region_id, 18410, t1.pdoc_id) as request_F,
        t4.value as response_F,
        uszn.pkPerson.GetDocReqValue(t1.region_id, 18411, t1.pdoc_id) as request_I,
        t5.value as response_I,
        uszn.pkPerson.GetDocReqValue(t1.region_id, 18412, t1.pdoc_id) as request_O,
        t6.value  as response_O
    from  uszn.all_personal_doc_reqs t1
          inner join
          uszn.all_personal_doc_reqs t2
    on    t1.class_id=18436 and t1.pd_class_id=18404
          and t1.pd_date_created between trunc(sysdate, 'mm')-10 and trunc(sysdate, 'dd')
          and t1.value = 1 and
          t1.region_id=t2.region_id and t1.pdoc_id=t2.pdoc_id and t1.order_num=t2.order_num and t1.owner_id=t2.owner_id and t2.class_id=18434
          inner join
          uszn.all_personal_doc_reqs t3
    on    t1.region_id=t3.region_id and t1.pdoc_id=t3.pdoc_id and t1.order_num=t3.order_num and t1.owner_id=t3.owner_id and t3.class_id=18448
          left join
          uszn.r_personal_doc_reqs t4
    on    t2.region_id=t4.region_id and t2.pdoc_id=t4.pdoc_id and t2.id=t4.owner_id and t4.class_id=18441
          left join
          uszn.r_personal_doc_reqs t5
    on    t2.region_id=t5.region_id and t2.pdoc_id=t5.pdoc_id and t2.id=t5.owner_id and t4.order_num=t5.order_num and t5.class_id=18442
          left join
          uszn.r_personal_doc_reqs t6
    on    t2.region_id=t6.region_id and t2.pdoc_id=t6.pdoc_id and t2.id=t6.owner_id and t4.order_num=t6.order_num and t6.class_id=18443) c,
 uszn.v_people_and_colls pc
where pc.region_id=c.region_id and pc.id=c.id