create table uszn.temp$_kind_as_rsd as
select * from
(select region_id, -- субъекты назначения
        pka_people_coll_id as people_id,
		uszn.pkPerson.GetPersonalReq(region_id, pka_people_coll_id, 25) AS SNILS,
        pka_kind_name as kind,
        amount,
        trunc(current_date, 'mm') as asg_date,
        rap_date_start,
        rap_date_end
   from uszn.all_asg_amounts
   where region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
         and trunc(current_date, 'mm') between rap_date_start and rap_date_end and (pka_kind_region_id, pka_kind_id) in
         ((0, 190), (0, 142), (104, 29), (0, 148), (0, 2), (104, 47), (104, 2), (104, 10), (104, 48), (104, 9), (104, 12), (104, 266))
  union all
 select region_id, -- получатели
        pka_payee_pc_id as people_id,
		uszn.pkPerson.GetPersonalReq(region_id, pka_people_coll_id, 25) AS SNILS,
        pka_kind_name as kind,
        amount,
        trunc(current_date, 'mm') as asg_date,
        rap_date_start,
        rap_date_end
   from uszn.all_asg_amounts
   where region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
         and (pka_kind_region_id, pka_kind_id) in ((104, 211), (104, 047), (104, 067), (000, 224))
         and trunc(current_date, 'mm') between rap_date_start and rap_date_end
  union all
  select
      t1.region_id, -- выплаты из заявления на РСД
      uszn.pkPerson.GetDocInstancePC(t1.pdoc_id, t1.region_id) as people_id,
	  uszn.pkPerson.GetPersonalReq(t1.region_id, uszn.pkPerson.GetDocInstancePC(t1.pdoc_id, t1.region_id), 25) AS SNILS,
      uszn.pkGen.RgnPrefix(t3.region_id)||t3.name as kind,
      uszn.pkPerson.GetDocReqValueNumber(t2.region_id, 7242, t2.pdoc_id, t2.order_num, t2.owner_id) as amount,
      trunc(current_date, 'mm') as asg_date,
      uszn.ToDateDef(t1.value) as Date_From,
      uszn.pkPerson.GetDocReqValueDate(t1.region_id, 7245, t1.pdoc_id, t1.order_num) as Date_To
    from uszn.r_personal_doc_reqs t1
           inner join
         uszn.r_personal_doc_reqs t2
       on t1.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
          and t1.class_id=7239 and t2.class_id=7241
          and t1.region_id=t2.region_id and t1.pdoc_id=t2.pdoc_id and t1.id=t2.owner_id
          and uszn.ToDateDef(t1.value) < = trunc(current_date, 'mm') and uszn.pkPerson.GetDocReqValueDate(t1.region_id, 7245, t1.pdoc_id, t1.order_num) >= trunc(current_date, 'mm')
           inner join uszn.dic_pc_income_kinds t3
       on t2.value=t3.region_id*1000000+t3.id
           inner join uszn.dic_pc_income_kinds_to_groups t4
      on t3.region_id=0 and t3.region_id=t4.income_kind_region_id and t3.id=t4.income_kind_id and t4.group_region_id=104 and t4.group_id=16
  union all
 select t1.region_id, -- выплаты из ПФР на РСД
        t1.people_coll_id as people_id,
		uszn.pkPerson.GetPersonalReq(t1.region_id, t1.people_coll_id, 25) AS SNILS,
        t2.pkind_name as kind,
        t1.asg_amount as amount,
        t1.asg_date,
        t2.date_from,
        t2.date_to
  from uszn.v_pd_c_15754 t1 inner join uszn.v_pd_c_15750 t2
   on t1.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
      and t1.asg_date=trunc(current_date, 'mm') 
	  --and t1.asg_amount>0 and trunc(current_date, 'mm') between t2.date_from and t2.date_to
      and t1.doc_instance_id=t2.doc_instance_id and t1.region_id=t2.region_id and t2.id=t1.owner_id)
