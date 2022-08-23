select region_id, id
 from uszn.r_smev3_inc_messages
 where message_kind_id=1 and /* запрос */
       data_kind_region_id=0 and data_kind_id in (16, 28) and /* Регистрация смерти */
       date_created between trunc(sysdate-1, 'dd') and trunc(sysdate, 'dd')
                              --to_date('01.01.2018') and trunc(sysdate, 'dd')