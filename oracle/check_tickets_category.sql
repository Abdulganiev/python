DECLARE
	iiIDs        uszn.pkGen.TIntegers;
	iMO          uszn.pkGen.TIntegers;
BEGIN 
	-- заполнение таблицы
 	uszn.pkCat.FillCategoriesToCompute('(0, 918),(0,1058),(0,1067),(0,1068),(0,1059),(0, 485),(0, 907),(0,1065),(0,1066),(0,1305),(0,916),(0,1163),(0,1153),(0,1154),(0,1155),(0, 660),(0, 514),(0, 661),(0, 515),(0, 662),(0, 516),(0,663),(0, 517),(0, 664),(0, 518),(0, 665),(0, 519),(0,1084),(0, 910)');
 
	SELECT id bulk collect INTO iMO
		FROM uszn.tsrv_regions WHERE owner_id=104 AND id not in (900, 71,72);
	
	FOR region in 1..iMO.count LOOP
	
		SELECT pc.people_id bulk collect INTO iiIDs
		    FROM 	uszn.v_coll_membership_periods pc
		    		INNER JOIN
		        	(SELECT t1.pc_region_id, t1.pc_id, min(t1.date_start) as min_date_start_c, max(t1.date_end) as max_date_end_c
		        	    FROM 	uszn.r_categories_assigned t1
		        	    WHERE 	t1.pc_region_id=iMO(region)
		        	           	AND Trunc(SysDate,'dd') BETWEEN t1.date_start AND t1.date_end
		        	           	AND (t1.pccat_id, t1.pccat_region_id) in ((918,0),(1058,0))
		        	    GROUP BY t1.pc_region_id, t1.pc_id) t1
		            on 	t1.pc_region_id=pc.region_id AND t1.pc_id=pc.people_id
		            	AND pc.role_class_id=10
		            	AND Trunc(SysDate,'dd') BETWEEN pc.date_start AND pc.date_end
		            LEFT JOIN
		        	(SELECT t1.pc_region_id, t1.pc_id, min(t1.date_start) as min_date_start, max(t1.date_end) as max_date_end
		        	    FROM uszn.r_categories_assigned t1
		        	    WHERE 	t1.pc_region_id=iMO(region)
		        	           	AND (t1.pccat_id, t1.pccat_region_id) in ((485,0),(1059,0))
		        	    GROUP BY t1.pc_region_id, t1.pc_id) t2
		        	ON t1.pc_region_id=t2.pc_region_id AND t1.pc_id=t2.pc_id
			WHERE Floor(Months_Between(Trunc(SysDate,'dd'), uszn.pkPerson.GetBirthDate(t1.pc_region_id, t1.pc_id))/12) BETWEEN 0 AND 22 AND
			      t1.max_date_end_c > sysdate AND t2.max_date_end < sysdate;
	
	  	FOR i in 1..iiIDs.count LOOP
	  	    uszn.pkCat.ComputeCategories(iMO(region), iiIDs(i), 0);
	  	END LOOP;
	END LOOP;
END;