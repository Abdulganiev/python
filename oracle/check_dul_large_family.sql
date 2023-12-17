select distinct
      region_id,
      '0'||region_id||' - '||uszn.pkTSrv.GetRegionName(region_id)||' - неправильный ДУЛ у ребенка- '||count(distinct pc_id) over(partition BY region_id) as name,
  	  '0'||region_id||' - '||uszn.pkTSrv.GetRegionName(region_id) as MO,
  	  pc_id,
	  pc_desc,
  	  identity_doc_class_name,
  	  identity_doc_desc

from (
SELECT
       t2.region_id,
       t2.region_id||'-'||t2.id as pc_id,
       t2.pc_desc,
       t2.identity_doc_class_name,
       t2.identity_doc_desc
		 FROM uszn.r_categories_assigned t1
			  join
			  uszn.v_people_and_colls t2
           ON t1.pc_region_id=t2.region_id AND t1.pc_id=t2.id
			        AND t1.pc_region_id IN (58,59,60,61,62,63,64,65,66,67,68,69,70)
              AND CURRENT_DATE BETWEEN t1.date_start AND t1.date_end
        			AND (t1.pccat_region_id, t1.pccat_id) IN ((0,918),(0,1058),(0,1067),(0,1068),(0,1059),(0,485),(0,907),(0,1065),(0,1066))
			        AND t2.death_date IS NULL
              AND t2.close_date IS NULL
        			AND FLOOR(MONTHS_BETWEEN(CURRENT_DATE, t2.birth_date)/12)<23
        			AND t2.identity_doc_class_id=7623
union all
SELECT
       t2.region_id,
       t2.region_id||'-'||t2.id as pc_id,
       t2.pc_desc,
       t2.identity_doc_class_name,
       t2.identity_doc_desc
		 FROM uszn.r_categories_assigned t1
			  join
			  uszn.v_people_and_colls t2
           ON t1.pc_region_id=t2.region_id AND t1.pc_id=t2.id
			        AND t1.pc_region_id IN (58,59,60,61,62,63,64,65,66,67,68,69,70)
              AND CURRENT_DATE BETWEEN t1.date_start AND t1.date_end
        			AND (t1.pccat_region_id, t1.pccat_id) IN ((0,918),(0,1058),(0,1067),(0,1068),(0,1059),(0,485),(0,907),(0,1065),(0,1066))
			        AND t2.death_date IS NULL
              AND t2.close_date IS NULL
        			AND FLOOR(MONTHS_BETWEEN(CURRENT_DATE, t2.birth_date)/12)<23
              AND t2.identity_doc_class_id=6
              AND uszn.pkPerson.GetPersonalReq(t2.region_id, t2.id, 20)='#######'


)
