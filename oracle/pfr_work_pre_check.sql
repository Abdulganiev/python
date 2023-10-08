declare
  iiIDs        uszn.pkGen.TIntegers;
  i$ Pls_Integer;
begin
  select id bulk collect into iiIDs
   from uszn.all_smev3_inc_messages
  where date_created>=To_Date('01.01.2023,00:00:00','dd.mm.yyyy,hh24:mi:ss') and
       data_kind_region_id=0 and data_kind_id=41 and is_processed=0 and message_data is not null;
  for i in 1..iiIDs.count loop
    begin
      i$ :=uszn.pkSMEV3.ProcessInMessage(iiIDs(i),1,1,'Принудительная асинхронная обработка входящего сообщения СМЭВ-3');
      commit;
    exception
      when Others then
        rollback;
    end;
  end loop;
end;
