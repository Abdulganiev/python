select
'О'||
-- страховой номер
RPad(Nvl(uszn.pkPerson.GetRawPCReqValue(c.region_id, c.people_id, 3371), '   -   -      '), 14, ' ')||
-- код региона по ОКАТО
RPad('71900000', 8, ' ')||
-- код ОПФР
RPad('030', 3, ' ')||
-- код района
case c.region_id
  when 60 then '001'
  when 62 then '002'
  when 63 then '003'
  when 66 then '004'
  when 58 then '005'
  when 65 then '006'
  when 59 then '007'
  when 61 then '008'
  when 67 then '009'
  when 70 then '010'
  when 69 then '011'
  when 68 then '012'
  when 64 then '014'
  else '000'
end||
-- фамилия
RPad(Nvl(Upper(uszn.pkPerson.GetPersonalReq(c.region_id, c.people_id, 0)), ' '), 40, ' ')||
-- имя
RPad(Nvl(Upper(uszn.pkPerson.GetPersonalReq(c.region_id, c.people_id, 1)), ' '), 40, ' ')||
-- отчество
RPad(Nvl(Upper(uszn.pkPerson.GetPersonalReq(c.region_id, c.people_id, 2)), ' '), 40, ' ')||
-- пол
(case uszn.ToIntDef(uszn.pkPerson.GetPersonalReq(c.region_id, c.people_id, 4))
  when 1 then 'Ж'
  else 'М' end)||
-- дата рождения
RPad(Nvl(To_Char(uszn.ToDateDef(uszn.pkPerson.GetPersonalReq(c.region_id, c.people_id, 3)), 'yyyy/mm/dd'), ' '), 10, ' ')||
-- пусто
RPad(' ', 201, ' ')||
-- код ДУЛ
RPad(
  case uszn.pkPerson.GetDocInstanceClass(uszn.pkPerson.GetMainPersonIdentity(c.region_id, c.people_id, 0), c.region_id, 0)
    when 6143 then 'ВИД НА ЖИТЕЛЬ'
    when 6242 then 'ВИД НА ЖИТЕЛЬ'
    when 2468 then 'ВОЕННЫЙ БИЛЕТ'
    when 2973 then 'ВРЕМ УДОСТ'
    when    4 then 'ПАСПОРТ РОССИИ'
    when 6139 then 'ПАСПОРТ'
    when 6142 then 'ИНПАСПОРТ'
    when    6 then 'СВИД О РОЖД'
    when 6114 then 'СВИД О РОЖД'
    when 6144 then 'СПРАВКА ОБ ОСВ'
    when 6141 then 'УДОСТ ЛИЧ ВОЕН'
    else 'ПРОЧЕЕ'
  end,
  14, ' ')||
-- серия ДУЛ
RPad(Nvl(uszn.pkPerson.GetPersonalReq(c.region_id, c.people_id, 19), ' '), 9, ' ')||
-- номер ДУЛ
RPad(Nvl(uszn.pkPerson.GetPersonalReq(c.region_id, c.people_id, 20), ' '), 9, ' ')||
-- дата выдачи ДУЛ
RPad(Nvl(To_Char(uszn.ToDateDef(uszn.pkPerson.GetPersonalReq(c.region_id, c.people_id, 23)), 'yyyy/mm/dd'), ' '), 10, ' ')||
-- организация ДУЛ
RPad(Nvl(Upper(uszn.pkPerson.GetPersonalReq(c.region_id, c.people_id, 22)), ' '), 80, ' ')||
-- почтовый индекс места регистрации
RPad(Nvl(Upper(uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 1, null, 0), 6, 0, 1, 0)), ' '), 6, ' ')||
-- регион места регистрации
RPad(Nvl(Upper(uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 1, null, 0), 5, 1, 1, 0)||' '||
               uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 1, null, 0), 4, 1, 1, 0)), ' '), 50, ' ')||
-- район места регистрации
RPad(Nvl(Upper(uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 1, null, 0), 5, 2, 1, 0)||' '||
               uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 1, null, 0), 4, 2, 1, 0)), ' '), 50, ' ')||
-- нас.пункт места регистрации
RPad(Nvl(Upper(uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 1, null, 0), 5, 0, 1, 0)||' '||
               uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 1, null, 0), 4, 0, 1, 0)), ' '), 50, ' ')||
-- улица места регистрации
RPad(Nvl(Upper(uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 2, 1, null, 0)), ' '), 40, ' ')||
-- дом места регистрации
RPad(Nvl(Upper(uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 3, 1, null, 0)), ' '), 8, ' ')||
-- корпус места регистрации
RPad(Nvl(Upper(uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 4, 1, null, 0)), ' '), 15, ' ')||
-- квартира места регистрации
RPad(Nvl(Upper(uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 5, 1, null, 0)), ' '), 6, ' ')||
-- почтовый индекс места пребывания
RPad(Nvl(Upper(uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 2, null, 0), 6, 0, 1, 0)), ' '), 6, ' ')||
-- регион места пребывания
RPad(Nvl(Upper(uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 2, null, 0), 5, 1, 1, 0)||' '||
               uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 2, null, 0), 4, 1, 1, 0)), ' '), 50, ' ')||
-- район места пребывания
RPad(Nvl(Upper(uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 2, null, 0), 5, 2, 1, 0)||' '||
               uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 2, null, 0), 4, 2, 1, 0)), ' '), 50, ' ')||
-- нас.пункт места пребывания
RPad(Nvl(Upper(uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 1, 2, null, 0)), ' '), 50, ' ')||
-- улица места пребывания
RPad(Nvl(Upper(uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 2, 2, null, 0)), ' '), 40, ' ')||
-- дом места пребывания
RPad(Nvl(Upper(uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 3, 2, null, 0)), ' '), 8, ' ')||
-- корпус места пребывания
RPad(Nvl(Upper(uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 4, 2, null, 0)), ' '), 15, ' ')||
-- квартира места пребывания
RPad(Nvl(Upper(uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 5, 2, null, 0)), ' '), 6, ' ')||
-- место проживания: Г-город, С-село
case Nvl(Upper(uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 1, null, 0), 5, 0, 1, 0)), ' ')
  when 'Г' then 'Г'
  when ' ' then
    case Nvl(Upper(uszn.pkAddr.GetKLADRObjInfoByCity(c.region_id, uszn.pkPCAddr.GetPCAddress(c.region_id, c.people_id, 6, 2, null, 0), 5, 0, 1, 0)), ' ')
      when 'Г' then 'Г'
      when ' ' then
        case c.region_id
          when 59 then 'С'
          when 63 then 'Г'
          when 61 then 'С'
          when 67 then 'С'
          when 70 then 'С'
          when 69 then 'С'
          when 68 then 'С'
          when 64 then 'Г'
          when 62 then 'Г'
          when 65 then 'Г'
          when 58 then 'Г'
          when 66 then 'Г'
          when 60 then 'Г'
          else 'С'
        end
      else 'С'
    end
  else 'С'
end||
-- пусто
RPad(' ', 244, ' ')||
-- категория получателя (запись типа "М")
RPad('06', 2, ' ')||
-- Признак наличия сведений о законном представителе (опекун, попечитель, родитель) лица либо о его представителе по доверенности ("Д" / "Н")
RPad(' ', 4, ' ')||
-- дата, из параметров выгрузки
RPad(Nvl(To_Char(TRUNC(LAST_DAY(SYSDATE))+1, 'yyyy/mm/dd'), ' '), 10, ' ')||
-- дата "По" из параметров выплаты
RPad(Nvl(To_Char(Last_Day(TRUNC(LAST_DAY(SYSDATE))+1), 'yyyy/mm/dd'), ' '), 10, ' ')||
-- Запись о праве гражданина на получение социальной доплаты к пенсии
RPad(' ', 3, ' ')||
-- вид регистрации получателя
case when uszn.ToDateDef(uszn.pkPerson.GetPersonalReq(c.region_id, c.people_id, 14))<uszn.pkGen.GetLastDate then 'В' else 'П' end||
-- признак работы пенсионера
RPad('НЕТ', 3, ' ')||
-- прожиточный минимум в ЯНАО
LPad(Nvl(To_Char(uszn.pkPayFml.Get_ProjMin(104, sysdate, 3), 'FM999999999999.00'), ' '), 15, '0')||
-- прожиточный минимум в РФ
LPad(Nvl(To_Char(uszn.pkPayFml.Get_ProjMin(0  , sysdate, 3), 'FM999999999999.00'), ' '), 15, '0')||
-- Признак отсутствия сведений о лице, указанном в запросе - "Н"
RPad(' ', 1, ' ')||
-- Нестандартная дата рождения
RPad(' ', 10, ' ')||
-- Дата увольнения
RPad(' ', 10, ' ')||
-- Дата поступления на работу
RPad(' ', 10, ' ')
from
(select region_id,
        pka_people_coll_id as people_id
       from uszn.all_asg_amounts
       where --region_id = 62
			 region_id not in (71,72,104)
             and pka_kind_region_id=104 and pka_kind_id=49 and pka_status_num=0
             and TRUNC(LAST_DAY(SYSDATE))+1 between rap_date_start and rap_date_end
       group by region_id,pka_people_coll_id
    union
 select region_id,
        people_coll_id as people_id
       from uszn.all_pk_assigned
       where --region_id = 62
	         region_id not in (71,72,104)
			 and kind_id=49 and kind_region_id=104 and status_num=1
             and ceasing_reason_id in (3,6,8,9,10,11,12) and cease_date>=To_Date('01.01.2019')
             and uszn.pkPerson.GetDeathDate(region_id,people_coll_id) is not null
             and uszn.pkPerson.GetCloseDate(region_id,people_coll_id) is not null
       group by region_id,people_coll_id) c
  inner join
  uszn.r_categories_assigned t2
on t2.pc_region_id=c.region_id and t2.pc_id=c.people_id
   and TRUNC(LAST_DAY(SYSDATE))+1 between t2.date_start and t2.date_end
   and t2.pccat_region_id=0 and t2.pccat_id = {pccat_id}