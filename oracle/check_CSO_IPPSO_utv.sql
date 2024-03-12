select
       '0'||d.region_id||'-'||uszn.pkPerson.GetDocReqValue(rq.region_id, 8731, rq.pdoc_id)||' не утв. ИППСУ на '||sysdate||' - '||count(distinct rq.pdoc_id) over(partition BY d.region_id) as name,
       uszn.pkPerson.GetDocReqValue(rq.region_id, 8731, rq.pdoc_id) as psu,
       d.region_id||'-'||d.pc_id as people_id, d.pc_desc, rq.pdoc_id, uszn.ToDateDef(rq.value) as date_decision
  from uszn.v_personal_docs d join uszn.v_personal_doc_reqs rq
   on rq.region_id=d.region_id and rq.pdoc_id=d.id
      and rq.class_id=8740 and d.class_id=8726
      and rq.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
      and uszn.ToDateDef(rq.value) between ADD_MONTHS(sysdate, -6) and sysdate
      and uszn.pkPerson.GetDocReqValueInt(rq.region_id, 8742, rq.pdoc_id)=1
      -- and uszn.pkDics.GetWorkdayCountBetweenDates(uszn.ToDateDef(rq.value), trunc(sysdate, 'dd')) > 2
	  and (trunc(sysdate, 'dd') - uszn.ToDateDef(rq.value)) > 2
      and uszn.pkPerson.GetDocReqValueInt(rq.region_id, 20905, rq.pdoc_id) is null