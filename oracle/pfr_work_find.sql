select region_id, id
  from uszn.all_smev3_inc_messages
  where --region_id=104 and
        message_kind_id=2 and
        data_kind_region_id=0 and data_kind_id=41 and
   		date_created between trunc(sysdate-1, 'dd') and trunc(sysdate, 'dd') and message_data is not null
		--date_created between to_date('01.01.2023') and trunc(sysdate, 'dd') and message_data is not null

