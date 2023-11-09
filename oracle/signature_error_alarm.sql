DECLARE
  iiIDs		uszn.pkGen.TIntegers;
  i$ 		PLS_INTEGER;
BEGIN
	SELECT id BULK COLLECT INTO iiIDs
		FROM uszn.all_smev3_inc_messages
		WHERE date_created >= TRUNC(SYSDATE-30, 'dd') AND proc_status_id=3;
  FOR i IN 1..iiIDs.COUNT LOOP
    BEGIN
      i$ := uszn.pkSMEV3.ProcessInMessage(iiIDs(i), 1, 1,'Принудительная обработка входящего сообщения СМЭВ-3');
    COMMIT;
    EXCEPTION
      WHEN OTHERS THEN
        ROLLBACK;
        RAISE;
    END;
  END LOOP;
END;