declare
  iRgnID     Pls_Integer := {region_id};            -- id района
  iPCID      Pls_Integer := {people_id};            -- id человека
  iClsID     Pls_Integer := 18899;                  -- ID класса документа
  iEK		 Pls_Integer := {ek};                   -- ID класса документа
  iDIID      Pls_Integer;                           -- ID документа
  sAudNotes   Varchar2(4000) := 'Документ создан сценарием';
begin
  -- триггер до добавлени¤ документа
  uszn.pkPerson.BeforeDocInstanceAdd(iRgnID, iPCID, iClsID);
  -- создать ID документа
  iDIID :=uszn.pkPerson.CreateDocInstance(iRgnID, iPCID, iClsID); -- —оздаЄт запись экземпл¤ра персонального документа и возвращает его ID
    -- iRegionID - ID района; iPeopleCollID - ID владельца документа; iDocClassID - ID класса документа;
  uszn.pkPerson.SetRawDocReqValue(iRgnID, iDIID, 18900, To_Char(iEK));
  -- записать в аудит
  uszn.pkAud.Log_PDoc_Create(iRgnID, iDIID, 1, sAudNotes);
  -- триггер после добавлени¤ документа
  uszn.pkPerson.AfterDocInstanceAdd(iRgnID, iDIID);
end;
