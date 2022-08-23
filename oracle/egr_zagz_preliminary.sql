begin
  uszn.pkXMLImp.ClearParsedXMLData(0);
  for msg in (
      select id, uszn.pkEgrZags.DirectiveDeathToRiurXML(id) as data
        from uszn.r_smev3_inc_messages
        where
          message_kind_id=1 and /* запрос */
          data_kind_region_id=0 and data_kind_id in (16, 28) and /* Регистрация смерти */
          Trunc(date_created, 'dd') between ADD_MONTHS(TRUNC(sysdate,'mm'),-1) and sysdate)
  loop
    uszn.pkXMLImp.ParseXMLData(msg.data, 0, 0, 0, 30, msg.id);
  end loop;
  uszn.pkXMLImp.AnalyzeParsedXMLData;
end;