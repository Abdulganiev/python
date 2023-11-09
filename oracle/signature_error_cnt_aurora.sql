SELECT COUNT(*) 
	FROM uszn.all_smev2_inc_messages
	WHERE error_message LIKE 'ORA-29516%Aurora%' AND date_created>=TRUNC(SYSDATE-30, 'dd')