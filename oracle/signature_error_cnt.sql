SELECT COUNT(*) 
	FROM uszn.all_smev3_inc_messages
	WHERE date_created >= TRUNC(SYSDATE-30, 'dd') AND proc_status_id=3