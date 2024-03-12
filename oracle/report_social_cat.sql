create table uszn.temp$_r_social_categories as

select region_id, people_id, cat, min(date_start) as date_start, max(date_end) as date_end
from
( -- Участники ВОВ
  select 'Участник ВОВ' as cat, c1.pc_region_id as region_id, c1.pc_id as people_id, c1.date_start, c1.date_end
    from uszn.r_categories_assigned c1 left join uszn.r_categories_assigned c2
   on c1.pc_region_id=c2.pc_region_id and c1.pc_id=c2.pc_id
      and Trunc(current_date, 'dd') between c2.date_start and c2.date_end
      and (c2.pccat_id, c2.pccat_region_id) in ((325,0),(239,0),(772,0),(734,0),(735,0),(736,0),(737,0),(738,0),(739,0),(787,0),(938,0))
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
        and Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((314,0))
        and c2.pc_id is null
  union all
  -- лица, награжденные медалью «За оборону Ленинграда»
  select 'Лицо, награжденное медалью «За оборону Ленинграда»', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((668,0))
  union all
  -- Лица, награжденные знаком «Жителю блокадного Ленинграда»
  select 'Лицо, награжденное знаком «Жителю блокадного Ленинграда»', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((481,0))
  union all
  -- Труженики тыла
  select 'Труженик тыла', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((15,104),(443,0))
  union all
  -- 2.1 Бывшие совершеннолетние узники концлагерей, гетто других мест принудительного содержания
  select 'Бывший совершеннолетний узник', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((483,0))
  union all
  -- '2.2 Бывшие несовершеннолетние узники концлагерей, гетто других мест принудительного содержания
  select 'Бывший несовершеннолетний узник', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((345,0),(795,0))
  union all
  --  3.1 Инвалиды ВОВ
  select 'Инвалид ВОВ', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1 inner join uszn.r_categories_assigned c2
      on c1.pc_region_id=c2.pc_region_id and c1.pc_id=c2.pc_id
       where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
             Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((239,0)) and
             Trunc(current_date, 'dd') between c2.date_start and c2.date_end and (c2.pccat_id, c2.pccat_region_id) in ((785,0),(721,0))
  union all
  --  3.2 Инвалиды боевых действий
  select 'Инвалид боевых действий', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((490,0),(623,0), (640,0))
  union all
  -- 4.1 Участники ВОВ, ставшие инвалидами вследствие общего заболевания
  select 'Участник ВОВ, ставший инвалидом вследствие общего заболевания', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end
   from uszn.r_categories_assigned c1 inner join uszn.r_categories_assigned c2
      on c1.pc_region_id=c2.pc_region_id and c1.pc_id=c2.pc_id
      where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
            Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((387,0),(325,0)) and
            Trunc(current_date, 'dd') between c2.date_start and c2.date_end and (c2.pccat_id, c2.pccat_region_id) in ((314,0),(315,0),(438,0),(442,0),(439,0),(759,0),(668,0),(440,0),(316,0),(441,0),(319,0))
  union all
  -- 5. Ветераны боевых действий
  select 'Ветеран боевых действий', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((789,0),(244,0))
  union all
  -- 6.1 Члены семей погибших (умерших) участников ВОВ
  select 'Член семьи погибшего (умершего) участника ВОВ', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_region_id, c1.pccat_id) in ((0,650),(0,659),(0,657),(0,656),(0,753),(0,522),(0,523),(0,525),(0,527),(0,817))
  union all
  -- 6.2 Члены семей погибших (умерших) ветеранов боевых действий
  select 'Член семьи погибшего (умершего) ветерана боевых действий', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end
   from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_region_id, c1.pccat_id) in ((0,526),(0,524),(0,658),(0,655),(0,812),(0,813))
  union all
  -- 6.3 Члены семей погибших при исполнении обязанностей военной службы (служебных обязанностей)
  select 'Члены семьи погибшего при исполнении обязанностей военной службы (служебных обязанностей)', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end
   from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_region_id, c1.pccat_id) in ((0,1139),(0,669),(0,1002),(0,489),(0,404))
  union all
  -- 7 Родители погибших (умерших) участников вооруженных конфликтов
  select 'Родитель погибшего (умершего) участника вооруженных конфликтов', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_region_id, c1.pccat_id) in ((0,609))
  union all
  -- 8 Ветераны труда
  select 'Ветеран труда', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_region_id, c1.pccat_id) in ((0,242))
  union all
  -- 11 Ветераны ЯНАО
  select 'Ветеран ЯНАО', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_region_id, c1.pccat_id) in ((104,1))
  union all
 -- 12 Реабилитированные граждане
  select 'Реабилитированный гражданин', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((336,0),(013,104))
  union all
 -- 13 Лица, признанные пострадавшими от политических репрессий
  select 'Лицо, признанное пострадавшим от политических репрессий', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((337,0),(014,104))
  union all
 -- 14 Доноры
  select 'Почетный донор', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_region_id, c1.pccat_id) in ((0,444),(0,782))
  union all
 -- 17 Специалисты бюджетной сферы
  select 'Специалист бюджетной сферы', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end
  from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((46,104),(47,104),(48,104),(49,104),(50,104),(51,104),(24,104))
  union all
 -- 18 Специалисты-пенсионеры бюджетной сферы
  select 'Специалист-пенсионер бюджетной сферы', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((52,104),(53,104),(54,104),(55,104),(56,104),(57,104),(23,104))
  union all
 -- 21.1 - инвалиды 1 группы
  select 'Инвалид 1 группы', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
   where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
         Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((798,0),(282,0))
  union all
 -- 21.2 - инвалиды 2 группы
  select 'Инвалид 2 группы', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
     where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
           Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((797,0),(283,0))
  union all
  -- 21.3 - инвалиды 3 группы
  select 'Инвалид 3 группы', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
     where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
           Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((796,0),(284,0))
  union all
 -- 21.5 - Ребенок-инвалид до 18 лет
  select 'Ребенок-инвалид до 18 лет', c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end from uszn.r_categories_assigned c1
     where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70) and
           Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((800,0),(1131,0))
  union all
 -- 27 Лицо, проживавшее во время ВОВ на территории СССР, которому на время окончания ВОВ (03.09.1945 года) не исполнилось 18 лет, стаж в ЯНАО 15 и более лет
  select 'Лицо, проживавшее во время ВОВ на территории СССР, которому на время окончания ВОВ (09 мая 1945 года) не исполнилось 18 лет, стаж в ЯНАО 15 и более лет',
         c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end
   from uszn.r_categories_assigned c1 join uszn.r_categories_assigned c2 on c1.pc_region_id=c2.pc_region_id and c1.pc_id=c2.pc_id
      where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
            and Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((180,104))
            and Trunc(current_date, 'dd') between c2.date_start and c2.date_end and (c2.pccat_id, c2.pccat_region_id) in ((3,104))
  union all
--  28 Инвалид, проживавшее во время ВОВ на территории СССР, которому на время окончания ВОВ (03.09.1945 года) не исполнилось 18 лет, стаж в ЯНАО 10 и более лет
  select 'Инвалид, проживавшее во время ВОВ на территории СССР, которому на время окончания ВОВ (03.09.1945 года) не исполнилось 18 лет, стаж в ЯНАО 10 и более лет',
         c1.pc_region_id, c1.pc_id, c1.date_start, c1.date_end
   from uszn.r_categories_assigned c1 join uszn.r_categories_assigned c2 on c1.pc_region_id=c2.pc_region_id and c1.pc_id=c2.pc_id
        join uszn.r_categories_assigned c3 on c1.pc_region_id=c3.pc_region_id and c1.pc_id=c3.pc_id
      where c1.pc_region_id in (58,59,60,61,62,63,64,65,66,67,68,69,70)
            and Trunc(current_date, 'dd') between c1.date_start and c1.date_end and (c1.pccat_id, c1.pccat_region_id) in ((180,104))
            and Trunc(current_date, 'dd') between c2.date_start and c2.date_end and (c2.pccat_id, c2.pccat_region_id) in ((2,104))
            and Trunc(current_date, 'dd') between c3.date_start and c3.date_end and (c3.pccat_id, c3.pccat_region_id) in ((325,0)))
group by cat, region_id, people_id