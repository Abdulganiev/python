select t1.region_id,
       '0'||t1.region_id||' - '||uszn.pkTSrv.GetRegionName(t1.region_id)||' - имеет право на РСД, но не назначено - '||count(1) over(partition BY t1.region_id) as name,
       '0'||t1.region_id||' - '||uszn.pkTSrv.GetRegionName(t1.region_id) as MO,	   
       t1.region_id||'-'||t1.people_id as id,
       t1.snils,
	   uszn.pkPerson.DescribeManColl(t1.region_id, t1.people_id, 0) as pc_desc,
       t2.asg_date,
       t1.kind as pens,
       t1.amount as amount_pens,
       t2.amount as sum_amount,
       uszn.pkPayFml.Get_ProjMin(104, trunc(current_date, 'mm'), 3) as Prog_Min
from uszn.temp$_kind_as_rsd t1
      join
     (select snils, max(to_date(DATA_REGISTRA)) as date_file 
	   from uszn.temp$_pfr622_C where DATA_REGISTRA> ADD_MONTHS(trunc(current_date, 'mm'), -1) group by snils) t5
      on t1.snils=t5.snils
      join
     (select region_id, people_id, asg_date, sum(amount) as amount 
	   from uszn.temp$_kind_as_rsd group by region_id, people_id, asg_date) t2
     on upper(t1.kind) like upper('%Пенсия%')
        and t2.amount < uszn.pkPayFml.Get_ProjMin(104, trunc(current_date, 'mm'), 3)
        and t1.region_id=t2.region_id and t1.people_id=t2.people_id
      join
      uszn.r_categories_assigned t3
     on t1.region_id=t3.pc_region_id and t1.people_id=t3.pc_id
     and trunc(current_date, 'mm') between date_start and date_end and (pccat_id, pccat_region_id) in ((1280,0))
      left join
      uszn.all_asg_amounts t4
     on t1.region_id=t4.region_id and t1.people_id=t4.pka_people_coll_id
        and trunc(current_date, 'mm') between t4.rap_date_start and t4.rap_date_end
        and (t4.pka_kind_region_id, t4.pka_kind_id) in ((104, 49))
where t4.region_id is null
order by t1.region_id, t1.amount