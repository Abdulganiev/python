DECLARE
	iiIDs        uszn.pkGen.TIntegers;
	iMO          uszn.pkGen.TIntegers;
BEGIN 
	-- заполнение таблицы
 	uszn.pkCat.FillCategoriesToCompute('(0,918),(0,1058),(0,1067),(0,1068),(0,1059),(0,485),(0,907),(0,1065),(0,1066)');
 
	SELECT id BULK COLLECT INTO iMO
		FROM uszn.tsrv_regions WHERE owner_id=104 AND id={region_id};
	
	FOR region IN 1..iMO.COUNT LOOP
	
      SELECT t1.pc_id BULK COLLECT INTO iiIDs
		 FROM uszn.r_categories_assigned t1
			  join
			  uszn.r_people_and_colls t2
           ON t1.pc_region_id=t2.region_id AND t1.pc_id=t2.id
			AND t1.pc_region_id=iMO(region)
            AND TRUNC(CURRENT_DATE, 'yyyy') - INTERVAL '1' YEAR <= t1.date_end
            AND TRUNC(CURRENT_DATE, 'yyyy') + INTERVAL '1' YEAR >= t1.date_start
			AND (t1.pccat_region_id, t1.pccat_id) IN ((0,918),(0,1058),(0,1067),(0,1068),(0,1059),(0,485),(0,907),(0,1065),(0,1066))
			AND t2.death_date IS NULL
            AND t2.close_date IS NULL
			AND FLOOR(MONTHS_BETWEEN(CURRENT_DATE, t2.birth_date)/12)<23
		GROUP BY t1.pc_id;
	
	  	FOR i IN 1..iiIDs.COUNT LOOP
	  	    uszn.pkCat.ComputeCategories(iMO(region), iiIDs(i), 0);
	  	END LOOP;
	END LOOP;
END;