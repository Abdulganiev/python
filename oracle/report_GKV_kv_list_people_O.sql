select
  'О'||
  RPad( Nvl( uszn.pkPerson.GetPersonalReq(r.region_id, r.people_id, 25), ' '),14)||
  LPad(30, 3, '0')||
  LPad(Nvl(uszn.pkXfer.GetExternalID(uszn.pkXfer.GetXferKindID('PF_SZN_RegionCode'), r.region_id, 104), '0'),3, '0')||
  'С'||
  RPad(Nvl(uszn.pkPerson.GetPersonalReq(r.region_id, r.people_id, 0), ' '),40)||
  RPad(Nvl(uszn.pkPerson.GetPersonalReq(r.region_id, r.people_id, 1), ' '),40)||
  RPad(Nvl(uszn.pkPerson.GetPersonalReq(r.region_id, r.people_id, 2), ' '),40)||
  Decode(uszn.pkPerson.GetPersonalReq(r.region_id, r.people_id, 4), 0, 'М',1, 'Ж',' ')||
  RPad(Nvl(To_Char(uszn.ToDateDef(uszn.pkPerson.GetPersonalReq(r.region_id, r.people_id, 3)), 'yyyy/mm/dd'),' '),10)||
  RPad(Nvl(uszn.pkPerson.GetPersonalReq(r.region_id, r.people_id, 21), ' '),80)||
  RPad(Nvl(uszn.pkPerson.GetPersonalReq(r.region_id, r.people_id, 19), ' '),8)||
  LPad(Nvl(uszn.pkPerson.GetPersonalReq(r.region_id, r.people_id, 20), '0'),8, '0')||
  RPad(Nvl(To_Char(uszn.ToDateDef(uszn.pkPerson.GetPersonalReq(r.region_id, r.people_id, 23)), 'yyyy/mm/dd'),' '),10)||
  RPad(Nvl(uszn.pkPerson.GetPersonalReq(r.region_id, r.people_id, 22), ' '),80)||
  RPad(Nvl(uszn.pkOutDocCol.GetPFRF_Formatted_Address(r.region_id, r.people_id, 0), ' '),200)||
  RPad('Денежная', 100)||
  LPad(To_Char(Nvl(r.basis_cnt, 0)), 3, '0')||
  RPad( Nvl( uszn.pkPerson.GetRawPCReqValueOnDate( r.region_id, uszn.pkPIC.GetCollByRole(r.region_id, r.people_id, 46, ADD_MONTHS(TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q'), 3)-1), 3760,  -- общая площадь
  3845,  -- дата с
  null,  -- дата по
  ADD_MONTHS(TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q'), 3)-1 ),' '),100 )||
  RPad(Nvl(To_Char(r.pc_house), ' '),40)||
  RPad(Nvl(To_Char(r.pc_srv), ' '),40)||
  RPad(' ', 100) as record_C,
  r.people_id

from (
  with
    -- признаки учёта, имеющиеся в справочнике соответствия данных для обмена
    mapped_pkafs as (
      select
          int_region_id as pkaf_region_id,
          int_id as pkaf_id,
          uszn.ToIntDef(ext_code) as cat_code
        from uszn.dic_data_exchange_mappings
        where
          -- вид соответствия: PrivRegCats_PKAF
          kind_id=70 and
          -- фильтр района внешнего ключа по району
          ext_region_id in (select parent_id from uszn.tsrv_flat_regions where child_id={region_id}) and
          -- исключаем:
          -- (040) «Участник ВОВ не в составе действующей армии (пп. з, п. 1, ст. 2, 5-ФЗ)»
          -- (050) «Лицо, награждённое знаком «Жителю блокадного Ленинграда»
          uszn.ToIntDef(ext_code) not in (40, 50) and
          ( -- федеральный регистр
            (uszn.ToIntDef(ext_code) between 10 and 150) or
            -- члены семей умерших от радиации
            (uszn.ToIntDef(ext_code) between 340 and 351)
          ))
  select
      pa.region_id,
      pa.pka_people_coll_id as people_id,
      -- жилищные услуги: количество человек, на которое распространяется льгота
      Nvl(
        Ceil(Max(
          case
            when
              (pa.poi_item_region_id=0 and pa.poi_item_id in (2, 3, 4, 12, 13)) or
              (pa.poi_item_region_id=104 and pa.poi_item_id=72)
            then pa.pc_count_applied_to
          end)),
        0) as pc_house,
      -- коммунальные услуги: количество человек, на которое распространяется льгота
      Nvl(
        Ceil(Max(
          case
            when
              (pa.poi_item_region_id=0 and pa.poi_item_id not in (2, 3, 4, 12, 13)) or
              (pa.poi_item_region_id=104 and pa.poi_item_id in (73, 194))
            then pa.pc_count_applied_to
          end)),
        0) as pc_srv,
      -- количество льготных оснований
      Count(distinct uszn.pkGen.EncodeIDRgnID(pa.pkaf_id, pa.pkaf_region_id)) as basis_cnt
    from uszn.all_po_amounts_ex pa
    where
      -- фильтр по району
      pa.region_id={region_id} and
      -- виды выплат, заданные в параметрах выходного документа
      (pa.pka_kind_region_id, pa.pka_kind_id) in ((104,29),(104,29)) and
      -- источник финансирования - федеральный бюджет
      pa.finsrc_region_id=0 and pa.finsrc_id=1 and
      -- оплачено
      pa.st_kind_id=2 and
      -- за период выборки
      pa.poi_payout_date between TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q') and ADD_MONTHS(TRUNC(ADD_MONTHS(SYSDATE, -3), 'Q'), 3)-1 and
      ( -- фильтр по признакам учёта
        ( -- признак учёта присутствует в параметрах перекодировки признаков учёта для заданного в параметрах выходного документа вида перекодиовки
          (pa.pkaf_region_id, pa.pkaf_id) in
            (select pkaf_region_id, pkaf_id
              from uszn.dic_exp_pkaf_params
              where (exp_kind_region_id, exp_kind_id) in ((104,1)))
        ) or
        ( -- признак учёта "Наличие документа «Сведения о получении льгот на ЖКУ на декабрь 2008 года»"
          (pa.pkaf_region_id, pa.pkaf_id) in ((104, 339)) and
          -- наличие соответствия в справочнике соответствия данных для обмена
          -- для льготного основания, указанного  в сведениях о получении льгот
          Exists(
            select 1
              from uszn.r_personal_doc_instances d, mapped_pkafs m
              where
                d.region_id=pa.region_id and d.people_coll_id=pa.pka_people_coll_id and
                -- реквизит "Правовое основание"
                d.class_id=7116 and
                -- slurp-ключ признака учёта ищем в персональном документе "Сведения о получении льгот..."
                m.pkaf_region_id*1000000+m.pkaf_id=uszn.ToIntDef(d.value)
          )
        ) or
        -- остальные признаки учёта, при наличии соответствия в справочнике
        (pa.pkaf_region_id, pa.pkaf_id) in (select pkaf_region_id, pkaf_id from mapped_pkafs)
      ) /* фильтр по признакам учёта */
    group by pa.region_id, pa.pka_people_coll_id
) r
