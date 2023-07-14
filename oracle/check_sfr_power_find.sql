select region_id, id, uszn.pkXMLUtils.GUIDToStr(message_guid) as MessageId
  from uszn.r_smev3_inc_messages
  where data_kind_region_id=0 and data_kind_id=41 and
		date_created between trunc(sysdate-1, 'dd') and trunc(sysdate, 'dd')
--		date_created between to_date('01.07.2023') and trunc(sysdate, 'dd')