declare
  iRegionID    Pls_Integer := {region_id};
  iID          Pls_Integer := {id};
  iMessageID   Pls_Integer;
  iCallID      Pls_Integer;
  bMessageData BLOB;
begin
  -- находим ID последнего входящего сообщения СМЭВ-3 по запросу
  for r in (
    select i.id as msg_id, i.id as call_id
      from uszn.all_smev3_inc_messages i
      where i.region_id=iRegionID and i.id=iID
      order by i.id desc)
  loop
    iMessageID := r.msg_id;
    iCallID    := r.call_id;
    Exit;
  end loop;
  if iMessageID is null then
    Raise_Application_Error(-20000, 'Ответное сообщение не найдено');
  end if;
  -- получаем данные сообщения СМЭВ-3
  select message_data into bMessageData from uszn.all_smev3_inc_messages where id=iMessageID;
  -- парсим сообщение; столбец дополнительных данных будут содержать ID записи об отправке запроса
  uszn.pkXMLImp.ParseXMLData(bMessageData, 1, 1, 1, 30, iCallID);
  uszn.pkXMLImp.ComputeNSAttribs(1, 1);
end;