select distinct
      pc.region_id,
      '0'||pc.region_id||' - '||uszn.pkTSrv.GetRegionName(pc.region_id)||' - может купить, но не имеет право на авиабилет - '||count(1) over(partition BY pc.region_id) as name,
  	  '0'||pc.region_id||' - '||uszn.pkTSrv.GetRegionName(pc.region_id) as MO,
      pc.region_id||'-'||pc.people_id as pc_id,
      pc.people_desc,
      Floor(Months_Between(Trunc(SysDate,'dd'), uszn.pkPerson.GetBirthDate(t1.pc_region_id, t1.pc_id))/12) as age
      --, t1.min_date_start_c, t2.min_date_start
      , t1.max_date_end_c as date_ticket
      , t2.max_date_end as date_family
         from
         uszn.v_coll_membership_periods pc
         inner join
         (select t1.pc_region_id, t1.pc_id, min(t1.date_start) as min_date_start_c, max(t1.date_end) as max_date_end_c
             from uszn.r_categories_assigned t1
              where t1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
                    --t1.pc_region_id=60
                    and Trunc(SysDate,'dd') between t1.date_start and t1.date_end
                    and (t1.pccat_id, t1.pccat_region_id) in ((918,0),(1058,0))
             group by t1.pc_region_id, t1.pc_id) t1
            on t1.pc_region_id=pc.region_id and t1.pc_id=pc.people_id
               and pc.role_class_id=10
               and Trunc(SysDate,'dd') between pc.date_start and pc.date_end
              left join
         (select t1.pc_region_id, t1.pc_id, min(t1.date_start) as min_date_start, max(t1.date_end) as max_date_end
             from uszn.r_categories_assigned t1
              where t1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
                    --t1.pc_region_id=60
                    --and Trunc(SysDate,'dd') between t1.date_start and t1.date_end
                    and (t1.pccat_id, t1.pccat_region_id) in ((485,0),(1059,0))
             group by t1.pc_region_id, t1.pc_id) t2
         on t1.pc_region_id=t2.pc_region_id and t1.pc_id=t2.pc_id
where --Floor(Months_Between(Trunc(SysDate,'dd'), uszn.pkPerson.GetBirthDate(t1.pc_region_id, t1.pc_id))/12) between 18 and 22 AND
      Floor(Months_Between(Trunc(SysDate,'dd'), uszn.pkPerson.GetBirthDate(t1.pc_region_id, t1.pc_id))/12) between 0 and 22 AND
      t1.max_date_end_c > sysdate and t2.max_date_end < sysdate