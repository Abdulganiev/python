select distinct pc.region_id,
       '0'||pc.region_id||' - '||uszn.pkTSrv.GetRegionName(pc.region_id)||' - нет СНИЛС на '||sysdate||' - '||count(distinct pc.id) over(partition BY pc.region_id) as name,
       uszn.pkTSrv.GetRegionName(pc.region_id) as MO,
       pc.region_id||'-'||pc.id as id,
       pc.pc_desc,
       kind_name
from
(

/*select t1.region_id, t1.pka_payee_pc_id as id, t1.pka_kind_name as kind_name from uszn.all_asg_amounts t1
  where t1.pka_kind_region_id=104 and t1.pka_kind_id=261

  union all
select t1.region_id, t1.pka_people_coll_id, t1.pka_kind_name from uszn.all_asg_amounts t1
  where t1.pka_kind_region_id=104 and t1.pka_kind_id=261

union all*/
select pk.region_id, pk.pka_people_coll_id as id, pk.pka_kind_name as kind_name from uszn.all_asg_amounts pk
                where pk.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
                      and trunc(sysdate, 'mm') between pk.rap_date_start and pk.rap_date_end
                      and pk.amount>0 and (pk.pka_kind_region_id, pk.pka_kind_id) in
      (select region_id, id from uszn.u_payment_kinds pk
        where pk.is_assignable=1 and pk.region_id in (select id from uszn.v_filter_regions_up where filter_region_id=104) and
              Exists(select 1 from uszn.u_popts_to_pkinds lnk
                      where lnk.pkind_region_id=pk.region_id and lnk.pkind_id=pk.id)
                            start with region_id=0 and id=1 /* детские выплаты */
                            connect by owner_region_id=prior region_id and owner_id=prior id)

union all
select pk.region_id, pk.pka_payee_pc_id, pk.pka_kind_name
                from uszn.all_asg_amounts pk
                where pk.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
                      and trunc(sysdate, 'mm') between pk.rap_date_start and pk.rap_date_end
					  and (pk.pka_kind_region_id, pk.pka_kind_id) not in ((104, 261))
                      and pk.amount>0 and (pk.pka_kind_region_id, pk.pka_kind_id) in
      (select region_id, id from uszn.u_payment_kinds pk
        where pk.is_assignable=1 and pk.region_id in (select id from uszn.v_filter_regions_up where filter_region_id=104) and
              Exists(select 1 from uszn.u_popts_to_pkinds lnk
                      where lnk.pkind_region_id=pk.region_id and lnk.pkind_id=pk.id)
                            start with region_id=0 and id=1 /* детские выплаты */
                            connect by owner_region_id=prior region_id and owner_id=prior id)

union all
select pk.region_id, pk.pka_people_coll_id, pk.pka_kind_name
                from uszn.all_asg_amounts pk
                where pk.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
					  and (pk.pka_kind_region_id, pk.pka_kind_id) not in ((104, 261))
					  and trunc(sysdate, 'mm') between pk.rap_date_start and pk.rap_date_end
                      and pk.amount>0 and (pk.pka_kind_region_id, pk.pka_kind_id) in
      (select region_id, id from uszn.u_payment_kinds pk
        where pk.is_assignable=1 and pk.region_id in (select id from uszn.v_filter_regions_up where filter_region_id=104) and
              Exists(select 1 from uszn.u_popts_to_pkinds lnk
                      where lnk.pkind_region_id=pk.region_id and lnk.pkind_id=pk.id)
                            start with region_id=104 and id=86 /* 62-ЗАО */
                            connect by owner_region_id=prior region_id and owner_id=prior id)

union all
select pk.region_id, pk.pka_payee_pc_id, pk.pka_kind_name
                from uszn.all_asg_amounts pk
                where pk.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
                      and trunc(sysdate, 'mm') between pk.rap_date_start and pk.rap_date_end
                      and pk.amount>0 and (pk.pka_kind_region_id, pk.pka_kind_id) in
      (select region_id, id from uszn.u_payment_kinds pk
        where pk.is_assignable=1 and pk.region_id in (select id from uszn.v_filter_regions_up where filter_region_id=104) and
              Exists(select 1 from uszn.u_popts_to_pkinds lnk
                      where lnk.pkind_region_id=pk.region_id and lnk.pkind_id=pk.id)
                            start with region_id=104 and id=86 /* 62-ЗАО */
                            connect by owner_region_id=prior region_id and owner_id=prior id)

union all
select pk.region_id, pk.pka_people_coll_id, pk.pka_kind_name
                from uszn.all_asg_amounts pk
                where pk.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
                      and trunc(sysdate, 'mm') between pk.rap_date_start and pk.rap_date_end
                      and pk.amount>0 and (pk.pka_kind_region_id, pk.pka_kind_id) in
      (select region_id, id from uszn.u_payment_kinds pk
        where pk.is_assignable=1 and pk.region_id in (select id from uszn.v_filter_regions_up where filter_region_id=104) and
              Exists(select 1 from uszn.u_popts_to_pkinds lnk
                      where lnk.pkind_region_id=pk.region_id and lnk.pkind_id=pk.id)
                            start with region_id=0 and id=4 /* ЖКВ */
                            connect by owner_region_id=prior region_id and owner_id=prior id)

union all
select pk.region_id, pk.pka_payee_pc_id, pk.pka_kind_name
                from uszn.all_asg_amounts pk
                where pk.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
                      and trunc(sysdate, 'mm') between pk.rap_date_start and pk.rap_date_end
                      and pk.amount>0 and (pk.pka_kind_region_id, pk.pka_kind_id) in
      (select region_id, id from uszn.u_payment_kinds pk
        where pk.is_assignable=1 and pk.region_id in (select id from uszn.v_filter_regions_up where filter_region_id=104) and
              Exists(select 1 from uszn.u_popts_to_pkinds lnk
                      where lnk.pkind_region_id=pk.region_id and lnk.pkind_id=pk.id)
                            start with region_id=0 and id=4 /* ЖКВ */
                            connect by owner_region_id=prior region_id and owner_id=prior id)

union all
select pk.region_id, pk.pka_people_coll_id, pk.pka_kind_name
                from uszn.all_asg_amounts pk
                where pk.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
                      and trunc(sysdate, 'mm') between pk.rap_date_start and pk.rap_date_end
                      and pk.amount>0 and (pk.pka_kind_region_id, pk.pka_kind_id) in
      (select region_id, id from uszn.u_payment_kinds pk
        where pk.is_assignable=1 and pk.region_id in (select id from uszn.v_filter_regions_up where filter_region_id=104) and
              Exists(select 1 from uszn.u_popts_to_pkinds lnk
                      where lnk.pkind_region_id=pk.region_id and lnk.pkind_id=pk.id)
                            start with region_id=0 and id=89 /* ЧАЭС */
                            connect by owner_region_id=prior region_id and owner_id=prior id)

union all
select pk.region_id, pk.pka_payee_pc_id, pk.pka_kind_name
                from uszn.all_asg_amounts pk
                where pk.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
                      and trunc(sysdate, 'mm') between pk.rap_date_start and pk.rap_date_end
                      and pk.amount>0 and (pk.pka_kind_region_id, pk.pka_kind_id) in
      (select region_id, id from uszn.u_payment_kinds pk
        where pk.is_assignable=1 and pk.region_id in (select id from uszn.v_filter_regions_up where filter_region_id=104) and
              Exists(select 1 from uszn.u_popts_to_pkinds lnk
                      where lnk.pkind_region_id=pk.region_id and lnk.pkind_id=pk.id)
                            start with region_id=0 and id=89 /* ЧАЭС */
                            connect by owner_region_id=prior region_id and owner_id=prior id)
union all /*многодетные*/
select pc_region_id, pc_id, 'Многодетные для авиабилетов' as kind_name
 from uszn.r_categories_assigned
 where pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
       and trunc(sysdate, 'mm') between date_start and date_end and pccat_region_id = 0 and pccat_id in (918, 1058, 1067, 1068, 1059, 485, 907, 1065, 1066)

union all /*члены ЖКВ*/	   
select t3.region_id, t3.people_id, t1.pka_kind_name
 from uszn.all_asg_amounts t1
      inner join
      uszn.v_coll_membership_periods t2
  on t1.region_id=t2.region_id and t1.pka_people_coll_id=t2.people_id
     and t1.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
     and t1.pka_status_num in (0, 1) and t1.pka_kind_region_id=104 and t1.pka_kind_id=29 and trunc(sysdate, 'mm') between t1.rap_date_start and t1.rap_date_end and t1.amount > 0
     and t2.coll_class_id=45
     and trunc(sysdate, 'mm') between t2.date_start and t2.date_end
     inner join
     uszn.v_coll_membership_periods t3
  on t2.region_id=t3.region_id and t2.coll_id=t3.coll_id
     and trunc(sysdate, 'mm') between t3.date_start and t3.date_end
	   
  ) c
  inner join
  uszn.v_people_and_colls pc
on pc.region_id=c.region_id and pc.id=c.id and uszn.pkPerson.GetPersonalReq(c.region_id, c.id, 26) is null
   and pc.is_coll_instance=0
order by pc.region_id, pc.pc_desc