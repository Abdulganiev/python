SELECT
'1'                                                         as applicant, /*Тип заявителя: 1 – Физическое лицо; 2 – Индивидуальный предприниматель; 3 – Юридическое лицо*/
NVL(cso_frgu_code, '8900000000000003124')                   as department, /*Идентификатор ведомства, присвоенный в РГУ*/
NVL(cso_KPP, '890101001')                                   as kppogv,
'8900000000162378240'                                       as serviceCode, /*Идентификатор услуги, присвоенный в РГУ*/
'1'                                                         as targetCode, /*Идентификатор цели, присвоенный в РГУ*/
'2'                                                         as processingMethod, /* Способ обработки заявления: 1 – заявление обработано специалистом; 2 – заявление обработано без участия специалиста*/
a.orderIdEpgu                                               as orderIdEpgu, /*Номер заявления, присвоенный ЕПГУ*/
a.orderIdIs                                                 as orderIdIs, /*Номер заявления, присвоенный ВИС*/
'71953000'                                                  as oktmo,
trunc(sysdate, 'mm')-1                                      as dateStart, /*2021-12-06 - Дата начала предоставления услуги*/
trunc(sysdate, 'mm')                                        as dateEnd, /*2021-12-08 - Дата конца предоставления услуги*/
'1'                                                         as result, /*Результат оказания услуги: 1 – Положительное решение; 2 – Отрицательное решение; 3 – Отмена заявления*/
'5'                                                         as channel, /*Способ подачи заявления: 1 – ЕПГУ; 2 – МФЦ; 3 – Портал ведомства; 4 – РПГМУ; 5 – Личное посещение*/
--uszn.pkPerson.GetPersonalReq(a.region_id, a.id, 25)         as snils,  /*117-141-323 11*/
null												        as snils,  /*117-141-323 11*/
uszn.pkPerson.GetPersonalReq(a.region_id, a.id,  0)||' '||
uszn.pkPerson.GetPersonalReq(a.region_id, a.id,  1)         as firstName, /*Иванова Марина*/
uszn.pkPerson.GetPersonalReq(a.region_id, a.id,  2)         as patronymic, /*Анатольевна*/
'7'||nvl(a.phone, a.phone2)                                 as phone, /*9003957073*/
null                                                        as email, /*Адрес электронной почты заявителя Поле обязательно для заполнения, если не заполнено поле «Телефон»*/
CASE WHEN uszn.pkPerson.GetPersonalReq(a.region_id, a.id,  4)=1
  THEN 2 ELSE 1 END 									    as gender, /*Пол заявителя: 1 – Мужской; 2 – Женский*/
to_date(uszn.pkPerson.GetPersonalReq(a.region_id, a.id, 3)) as age, /*Дата рождения заявителя*/
'2'                                                         as representative, /*Заявление подано представителем: 1 – Да; 2 – Нет*/
'1'                                                         as specialistId,
'Сотрудник'                                                 as specialistName,
REPLACE(a.cso, '"', '')                                     as nameUl,
NVL(cso_INN, '8901017082')                                  as innUl, /*ИНН ведомства, предоставляющего услугу*/
NVL(cso_KPP, '890101001')                                   as kppUl /*КПП ведомства, предоставляющего услугу*/

FROM
(SELECT distinct
     t1.region_id,
     t1.people_coll_id as id,
     '1' as orderIdEpgu,
     '1' as orderIdIs,
     uszn.pkPerson.GetRawPCReqValue(t1.region_id, t1.people_coll_id, 11432) as phone,
     CASE
      WHEN length(uszn.pkPerson.GetRawPCReqValue(t1.region_id, t1.people_coll_id, 8348))=11
       THEN substr(uszn.pkPerson.GetRawPCReqValue(t1.region_id, t1.people_coll_id, 8348), 2, 10)
      WHEN length(uszn.pkPerson.GetRawPCReqValue(t1.region_id, t1.people_coll_id, 8348))=10
       THEN uszn.pkPerson.GetRawPCReqValue(t1.region_id, t1.people_coll_id, 8348)
     END as phone2,
     (SELECT t3.frgu_code FROM uszn.v_agents t3
           WHERE t3.region_id*1000000+t3.id=(SELECT t2.region_id*1000000+t2.agent_id FROM uszn.dic_agent_departments t2
                                               WHERE t1.department_key=t2.region_id*1000000+t2.id)) as cso_frgu_code,
     (SELECT t3.name FROM uszn.v_agents t3
           WHERE t3.region_id*1000000+t3.id=(SELECT t2.region_id*1000000+t2.agent_id FROM uszn.dic_agent_departments t2
                                               WHERE t1.department_key=t2.region_id*1000000+t2.id)) as cso,
     (SELECT t3.inn_code FROM uszn.v_agents t3
           WHERE t3.region_id*1000000+t3.id=(SELECT t2.region_id*1000000+t2.agent_id FROM uszn.dic_agent_departments t2
                                               WHERE t1.department_key=t2.region_id*1000000+t2.id)) as cso_INN,
     (SELECT t3.kpp_code FROM uszn.v_agents t3
           WHERE t3.region_id*1000000+t3.id=(SELECT t2.region_id*1000000+t2.agent_id FROM uszn.dic_agent_departments t2
                                               WHERE t1.department_key=t2.region_id*1000000+t2.id)) as cso_KPP
   FROM uszn.v_pd_c_8907 t1
   WHERE t1.region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) --=60
         and t1.service_date between trunc(sysdate, 'dd')-1 and trunc(sysdate, 'dd')
         and t1.latitude is not null
         --and t1.people_coll_id=5464
         ) a
  WHERE (upper(a.cso) LIKE '%ГБУ%' OR upper(a.cso) LIKE '%ГКУ%')
        AND (a.phone is not null or a.phone2 is not null)