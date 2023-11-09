DECLARE
  iiIDs		uszn.pkGen.TIntegers;
  i$		PLS_INTEGER;
BEGIN
    SELECT id BULK COLLECT INTO iiIDs
      FROM  uszn.all_smev2_inc_messages
      WHERE error_message LIKE 'ORA-29516%Aurora%' AND date_created>=TRUNC(SYSDATE-30, 'dd');
  FOR i IN 1..iiIDs.COUNT LOOP
    BEGIN
      i$ := uszn.pkSMEVProv.AsyncProcessMessage(iiIDs(i),1,1,'Принудительная обработка входящего сообщения СМЭВ-2');
      COMMIT;
    EXCEPTION
      WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
    END;
  END LOOP;
END;