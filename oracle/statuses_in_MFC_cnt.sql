select count(*)    
 from uszn.r_smev2_calls b1
      join
      (select c1.region_id, max(c1.id) as id -- находим у этих сообщений макс ИД отправлений
        from uszn.r_smev2_calls c1
        join
        (select t1.region_id, t1.id -- находим для этих отправлений сообщения СМЭВ2
          from uszn.r_smev2_requests t1
          join
          (select id, region_id, request_id -- находим все отправления с ошибками
            from uszn.r_smev2_calls where error_message is not null and date_created > to_date('01.01.2023')) t2
          on t1.region_id=t2.region_id and t1.id=t2.request_id) c2
        on c1.region_id=c2.region_id and c1.request_id=c2.id
           group by c1.region_id) b2
      on b1.region_id=b2.region_id and b1.id=b2.id
         where b1.error_message is not null