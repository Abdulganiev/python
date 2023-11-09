select id
 from uszn.dic_state_services
 where folder_id=2 
       and folder_region_id=104 
	   and id NOT IN (17, 68)
	   and is_actual=1
 order by name