DECLARE
	iiIDs        uszn.pkGen.TIntegers;
	iMO          uszn.pkGen.TIntegers;
BEGIN

 delete from uszn.temp$_cso_urgent;

  SELECT id bulk collect INTO iMO
		FROM uszn.tsrv_regions WHERE owner_id=104 AND id not in (900, 71);

	FOR region in 1..iMO.count LOOP

    insert into uszn.temp$_cso_urgent
  select
   (select name from uszn.dic_ssvc_service_forms where id in (select atr1.service_form_id
     from uszn.dic_ssvc_pk_item_attribs atr1 where usl.item_key=atr1.item_region_id*1000000+atr1.item_id)) as form,
   (select name from uszn.dic_ssvc_service_kinds where id in (select atr1.service_kind_id
     from uszn.dic_ssvc_pk_item_attribs atr1 where usl.item_key=atr1.item_region_id*1000000+atr1.item_id)) as vid,
   uszn.pkPerson.GetDocReqValue(usl.region_id, 9019, usl.doc_instance_id) as psu,
   uszn.pkPerson.GetDocReqValueDate(usl.region_id, 9018, usl.doc_instance_id) as application_date,
   uszn.pkPerson.GetDocReqValueDate(usl.region_id, 9084, usl.doc_instance_id) as application_from,
   uszn.pkPerson.GetDocReqValueDate(usl.region_id, 9085, usl.doc_instance_id) as application_to,
   (select uszn.StrCommaConcat(uszn.pkGen.StripRgnPrefix(decoded_value))
     from uszn.all_personal_doc_reqs where class_id=9082 and region_id=usl.region_id and pdoc_id=usl.doc_instance_id) as circumstances,
   uszn.pkGen.StripRgnPrefix(usl.item_name) as item_name,
   uszn.pkPerson.GetDocReqValueDate(usl.region_id, 9021, usl.doc_instance_id) as decision_date,
   uszn.pkPerson.GetDocReqValue(usl.region_id, 9022, usl.doc_instance_id) as decision_num,
   (select uszn.StrCommaConcat(uszn.pkGen.StripRgnPrefix(decoded_value))
     from uszn.all_personal_doc_reqs where class_id=9026 and region_id=usl.region_id and pdoc_id=usl.doc_instance_id) as basis,
   uszn.pkPerson.GetDocReqValueDate(usl.region_id, 9028, usl.doc_instance_id) as decision_from,
   uszn.pkPerson.GetDocReqValueDate(usl.region_id, 9029, usl.doc_instance_id) as decision_to,
   usl.region_id,
   usl.people_coll_id as people_id,
   case when uszn.pkPerson.GetDocReqValue(usl.region_id, 19128, usl.doc_instance_id, usl.order_num) is null then null else usl.people_coll_id end as people_ek,

   usl.service_date,
   usl.fact_count,
   case when uszn.pkPerson.GetDocReqValue(usl.region_id, 19128, usl.doc_instance_id, usl.order_num) is null then 0 else 1 end as fact_count_ek,
   usl.department_name

   from uszn.v_pd_c_9030 usl
     where usl.service_date between to_date('01.01.2000') and trunc(sysdate, 'dd')-1
           and usl.region_id=iMO(region);

	END LOOP;
END;