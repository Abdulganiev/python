select *

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
          ext_region_id in (select parent_id from uszn.tsrv_flat_regions where child_id=59) and
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
      pa.region_id=59 and
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
