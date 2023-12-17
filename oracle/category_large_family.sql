DECLARE
	iiIDs        uszn.pkGen.TIntegers;
	iMO          uszn.pkGen.TIntegers;
BEGIN 
	-- заполнение таблицы
 	uszn.pkCat.FillCategoriesToCompute('(000, 661), (000, 515), (000, 662), (000, 516), (000, 663), (000, 517), (000, 664), (000, 518), (000, 665), (000, 519), (000, 1084), (000, 910)');
 
	SELECT id BULK COLLECT INTO iMO
		FROM uszn.tsrv_regions WHERE owner_id=104 AND id={region_id};
	
	FOR region in 1..iMO.COUNT LOOP
	
      SELECT t1.pc_id BULK COLLECT INTO iiIDs
		 FROM uszn.r_categories_assigned t1
			  join
			  uszn.r_people_and_colls t2
			ON t1.pc_region_id=t2.region_id AND t1.pc_id=t2.id
			   AND t1.pc_region_id=iMO(region)
			   AND t2.coll_class_id=6
			   AND CURRENT_DATE BETWEEN t1.date_start AND t1.date_end
			   AND (t1.pccat_id, t1.pccat_region_id) IN ((1153,0));
	
	  	FOR i IN 1..iiIDs.count LOOP
	  	    uszn.pkCat.ComputeCategories(iMO(region), iiIDs(i), 0);
	  	END LOOP;
	END LOOP;
END;