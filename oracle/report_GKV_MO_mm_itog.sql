select
'' as e34,
'Итог по МО '||uszn.pkTSrv.GetRegionName({region_id}) as d34,
sum(a01)+sum(a02)+sum(a03)+sum(a04)+sum(a05)+sum(a06)+sum(a07)+sum(a08)+sum(a09)+sum(a10)+sum(a11)+sum(a12)+sum(a42)+sum(a43)+sum(a44)+sum(a14)+sum(a15)+sum(a16)+sum(a17)+sum(a18)+sum(a19)+sum(a20)+sum(a21)+sum(a22)+sum(a23)+sum(a24)+sum(a25)+sum(a27)+sum(a30)+sum(a31)+sum(a32)+sum(a33) as a34,
sum(b01)+sum(b02)+sum(b03)+sum(b04)+sum(b05)+sum(b06)+sum(b07)+sum(b08)+sum(b09)+sum(b10)+sum(b11)+sum(b12)+sum(b42)+sum(b43)+sum(b44)+sum(b14)+sum(b15)+sum(b16)+sum(b17)+sum(b18)+sum(b19)+sum(b20)+sum(b21)+sum(b22)+sum(b23)+sum(b24)+sum(b25)+sum(b27)+sum(b30)+sum(b31)+sum(b32)+sum(b33) as b34,
sum(c01)+sum(c02)+sum(c03)+sum(c04)+sum(c05)+sum(c06)+sum(c07)+sum(c08)+sum(c09)+sum(c10)+sum(c11)+sum(c12)+sum(c42)+sum(c43)+sum(c44)+sum(c14)+sum(c15)+sum(c16)+sum(c17)+sum(c18)+sum(c19)+sum(c20)+sum(c21)+sum(c22)+sum(c23)+sum(c24)+sum(c25)+sum(c27)+sum(c30)+sum(c31)+sum(c32)+sum(c33) as c34

from
(select

      -- ============================================================
      -- Федеральный закон от 12 января 1995 года №5-ФЗ «О ветеранах»
      -- ============================================================
      -- Инвалиды войны
      Nvl(Decode(n_row, 01, Sum(fam)),  0) as a01,
      Nvl(Decode(n_row, 01, Sum(cnt)),  0) as b01,
      Nvl(Decode(n_row, 01, Sum(area)), 0) as c01,
      -- Участники Великой Отечественной войны, ставшие инвалидами
      Nvl(Decode(n_row, 02, Sum(fam)),  0) as a02,
      Nvl(Decode(n_row, 02, Sum(cnt)),  0) as b02,
      Nvl(Decode(n_row, 02, Sum(area)), 0) as c02,
      -- Военнослужащие и лица рядового и начальствующего состава органов внутренних дел, Государственной противопожарной службы, учреждений и органов уголовно-исполнительной системы, ставшие инвалидами вследствие ранения, контузии или увечья, полученных при исполнении обязанностей военной службы (служебных обязанностей)
      Nvl(Decode(n_row, 03, Sum(fam)),  0) as a03,
      Nvl(Decode(n_row, 03, Sum(cnt)),  0) as b03,
      Nvl(Decode(n_row, 03, Sum(area)), 0) as c03,
      -- Участники Великой Отечественной войны
      Nvl(Decode(n_row, 04, Sum(fam)),  0) as a04,
      Nvl(Decode(n_row, 04, Sum(cnt)),  0) as b04,
      Nvl(Decode(n_row, 04, Sum(area)), 0) as c04,
      -- Лица, награждённые знаком «Жителю блокадного Ленинграда», признанные инвалидами вследствие общего заболевания, трудового увечья и других причин (кроме лиц, инвалидность которых наступила вследствие их противоправных действий)
      Nvl(Decode(n_row, 05, Sum(fam)),  0) as a05,
      Nvl(Decode(n_row, 05, Sum(cnt)),  0) as b05,
      Nvl(Decode(n_row, 05, Sum(area)), 0) as c05,
      -- Ветераны боевых действий
      Nvl(Decode(n_row, 06, Sum(fam)),  0) as a06,
      Nvl(Decode(n_row, 06, Sum(cnt)),  0) as b06,
      Nvl(Decode(n_row, 06, Sum(area)), 0) as c06,
      -- Члены семей погибших (умерших) инвалидов войны, участников Великой Отечественной войны и ветеранов боевых действий
      Nvl(Decode(n_row, 07, Sum(fam)),  0) as a07,
      Nvl(Decode(n_row, 07, Sum(cnt)),  0) as b07,
      Nvl(Decode(n_row, 07, Sum(area)), 0) as c07,
      -- Члены семей погибших в Великой Отечественной войне лиц из числа личного состава групп самозащиты объектовых и аварийных команд местной противовоздушной обороны, а также члены семей погибших работников госпиталей и больниц города Ленинграда
      Nvl(Decode(n_row, 08, Sum(fam)),  0) as a08,
      Nvl(Decode(n_row, 08, Sum(cnt)),  0) as b08,
      Nvl(Decode(n_row, 08, Sum(area)), 0) as c08,
      -- Члены семей военнослужащих, лиц рядового и начальствующего состава органов внутренних дел, Государственной противопожарной службы, учреждений и органов уголовно-исполнительной системы и органов государственной безопасности, погибших при исполнении обязанностей военной службы (служебных обязанностей)
      Nvl(Decode(n_row, 09, Sum(fam)),  0) as a09,
      Nvl(Decode(n_row, 09, Sum(cnt)),  0) as b09,
      Nvl(Decode(n_row, 09, Sum(area)), 0) as c09,
      -- Члены семей военнослужащих, погибших в плену, признанных в установленном порядке пропавшими без вести в районах боевых действий со времени исключения указанных военнослужащих из списков воинских частей
      Nvl(Decode(n_row, 10, Sum(fam)),  0) as a10,
      Nvl(Decode(n_row, 10, Sum(cnt)),  0) as b10,
      Nvl(Decode(n_row, 10, Sum(area)), 0) as c10,

      -- ============================================================
      -- Федеральный закон от 22 августа 2004 года №122-ФЗ
      -- ============================================================
      -- Бывшие несовершеннолетние узники концлагерей, гетто, других мест принудительного содержания, созданных фашистами и их союзниками в период второй мировой войны, признанные инвалидами вследствие общего заболевания, трудового увечья и других причин (за исключением лиц, инвалидность которых наступила вследствие их противоправных действий)
      Nvl(Decode(n_row, 11, Sum(fam)),  0) as a11,
      Nvl(Decode(n_row, 11, Sum(cnt)),  0) as b11,
      Nvl(Decode(n_row, 11, Sum(area)), 0) as c11,
      -- Бывшие несовершеннолетние узники концлагерей, гетто, других мест принудительного содержания, созданных фашистами и их союзниками в период второй мировой войны
      Nvl(Decode(n_row, 12, Sum(fam)),  0) as a12,
      Nvl(Decode(n_row, 12, Sum(cnt)),  0) as b12,
      Nvl(Decode(n_row, 12, Sum(area)), 0) as c12,

      -- ============================================================
      -- Федеральный закон от 24 ноября 1995 года №181-ФЗ «О социальной защите инвалидов в Российской Федерации»
      -- ============================================================
      'Инвалиды' as d13,
      Nvl(Decode(n_row, 13, Sum(fam)),  0) as a13,
      Nvl(Decode(n_row, 13, Sum(cnt)),  0) as b13,
      Nvl(Decode(n_row, 13, Sum(area)), 0) as c13,
      -- Инвалиды 1 группы
      Nvl(Decode(n_row, 42, Sum(fam)),  0) as a42,
      Nvl(Decode(n_row, 42, Sum(cnt)),  0) as b42,
      Nvl(Decode(n_row, 42, Sum(area)), 0) as c42,
      -- Инвалиды 2 группы
      Nvl(Decode(n_row, 43, Sum(fam)),  0) as a43,
      Nvl(Decode(n_row, 43, Sum(cnt)),  0) as b43,
      Nvl(Decode(n_row, 43, Sum(area)), 0) as c43,
      -- Инвалиды 3 группы
      Nvl(Decode(n_row, 44, Sum(fam)),  0) as a44,
      Nvl(Decode(n_row, 44, Sum(cnt)),  0) as b44,
      Nvl(Decode(n_row, 44, Sum(area)), 0) as c44,
      -- Семьи, имеющие детей-инвалидов
      Nvl(Decode(n_row, 14, Sum(fam)),  0) as a14,
      Nvl(Decode(n_row, 14, Sum(cnt)),  0) as b14,
      Nvl(Decode(n_row, 14, Sum(area)), 0) as c14,

      -- ============================================================
      -- Закон Российской Федерации от 15 мая 1991 года №1244-1
      -- ============================================================
      -- Граждане, получившие или перенёсшие лучевую болезнь и другие заболевания, связанные с радиационным воздействием
      -- вследствие чернобыльской катастрофы или с работами по ликвидации последствий катастрофы на Чернобыльской АЭС
      Nvl(Decode(n_row, 15, Sum(fam)),  0) as a15,
      Nvl(Decode(n_row, 15, Sum(cnt)),  0) as b15,
      Nvl(Decode(n_row, 15, Sum(area)), 0) as c15,
      -- Инвалиды вследствие чернобыльской катастрофы
      Nvl(Decode(n_row, 16, Sum(fam)),  0) as a16,
      Nvl(Decode(n_row, 16, Sum(cnt)),  0) as b16,
      Nvl(Decode(n_row, 16, Sum(area)), 0) as c16,
      -- Граждане (в том числе временно направленные или командированные), принимавшие в 1986 – 1987 годах участие в работах
      -- по ликвидации последствий чернобыльской катастрофы в пределах зоны отчуждения...
      Nvl(Decode(n_row, 17, Sum(fam)),  0) as a17,
      Nvl(Decode(n_row, 17, Sum(cnt)),  0) as b17,
      Nvl(Decode(n_row, 17, Sum(area)), 0) as c17,
        -- Граждане, эвакуированные (в том числе выехавшие добровольно) в 1986 году из зоны отчуждения
      Nvl(Decode(n_row, 18, Sum(fam)),  0) as a18,
      Nvl(Decode(n_row, 18, Sum(cnt)),  0) as b18,
      Nvl(Decode(n_row, 18, Sum(area)), 0) as c18,
      -- Дети и подростки, страдающие болезнями вследствие чернобыльской катастрофы..., ставшие инвалидами
      Nvl(Decode(n_row, 19, Sum(fam)),  0) as a19,
      Nvl(Decode(n_row, 19, Sum(cnt)),  0) as b19,
      Nvl(Decode(n_row, 19, Sum(area)), 0) as c19,
      -- Дети и подростки, страдающие болезнями вследствие чернобыльской катастрофы..., ставшие инвалидами
      Nvl(Decode(n_row, 20, Sum(fam)),  0) as a20,
      Nvl(Decode(n_row, 20, Sum(cnt)),  0) as b20,
      Nvl(Decode(n_row, 20, Sum(area)), 0) as c20,
      -- Рабочие и служащие, а также военнослужащие, лица начальствующего и рядового состава органов внутренних дел, Государственной
      -- противопожарной службы, получившие профессиональные заболевания, связанные с лучевым воздействием на работах в зоне отчуждения
      Nvl(Decode(n_row, 21, Sum(fam)),  0) as a21,
      Nvl(Decode(n_row, 21, Sum(cnt)),  0) as b21,
      Nvl(Decode(n_row, 21, Sum(area)), 0) as c21,
      -- Семьи, в том числе вдовы (вдовцы) умерших участников ликвидации последствий катастрофы на Чернобыльской АЭС 1986 – 1987 гг.
      Nvl(Decode(n_row, 22, Sum(fam)),  0) as a22,
      Nvl(Decode(n_row, 22, Sum(cnt)),  0) as b22,
      Nvl(Decode(n_row, 22, Sum(area)), 0) as c22,
      -- Семьи, потерявшие кормильца из числа граждан, погибших в результате катастрофы на Чернобыльской АЭС...
      Nvl(Decode(n_row, 23, Sum(fam)),  0) as a23,
      Nvl(Decode(n_row, 23, Sum(cnt)),  0) as b23,
      Nvl(Decode(n_row, 23, Sum(area)), 0) as c23,

      -- ============================================================
      -- Федеральный закон от 26 ноября 1998 года №175-ФЗ
      -- ============================================================
      -- Граждане, ставшие инвалидами в результате воздействия радиации вследствие аварии в 1957 году на производственном
      -- объединении «Маяк» и сбросов радиоактивных отходов в реку Теча
      Nvl(Decode(n_row, 24, Sum(fam)),  0) as a24,
      Nvl(Decode(n_row, 24, Sum(cnt)),  0) as b24,
      Nvl(Decode(n_row, 24, Sum(area)), 0) as c24,
      -- Граждане, получившие лучевую болезнь, другие заболевания, включенные в перечень заболеваний, возникновение или обострение
      -- которых обусловлены воздействием радиации вследствие аварии в 1957 году на производственном объединении «Маяк» и сбросов
      -- радиоактивных отходов в реку Теча
      Nvl(Decode(n_row, 25, Sum(fam)),  0) as a25,
      Nvl(Decode(n_row, 25, Sum(cnt)),  0) as b25,
      Nvl(Decode(n_row, 25, Sum(area)), 0) as c25,
      -- Граждане (в том числе временно направленные или командированные), включая военнослужащих и военнообязанных...
      -- занятые на работах по проведению защитных мероприятий и реабилитации радиоактивно загрязнённых территорий вдоль реки
      -- Теча в 1949 – 1956 годах
      Nvl(Decode(n_row, 26, Sum(fam)),  0) as a26,
      Nvl(Decode(n_row, 26, Sum(cnt)),  0) as b26,
      Nvl(Decode(n_row, 26, Sum(area)), 0) as c26,
      -- Граждане, эвакуированные (переселенные), а также добровольно выехавшие из населённых пунктов...
      -- в 1957 году из зоны радиоактивного загрязнения
      Nvl(Decode(n_row, 27, Sum(fam)),  0) as a27,
      Nvl(Decode(n_row, 27, Sum(cnt)),  0) as b27,
      Nvl(Decode(n_row, 27, Sum(area)), 0) as c27,
      -- Семьи, потерявшие кормильца из числа граждан, получивших лучевую болезнь...
      -- в результате аварии в 1957 году на производственном объединении «Маяк» и сбросов радиоактивных отходов в реку «Теча»
      /* 0 0 0 (нет данных) */
      -- Семьи, потерявшие кормильца из числа инвалидов вследствие воздействия радиации в случае, если смерть являлась следствием
      -- воздействия радиации в результате аварии в 1957 году на производственном объединении «Маяк» и сбросов радиоактивных
      -- отходов в реку «Теча»
      /* 0 0 0 (нет данных) */

      -- ============================================================
      -- Постановление Верховного Совета Российской Федерации от 27 декабря 1991 года №2123-1
      -- ============================================================
      -- Граждане из подразделений особого риска, имеющие инвалидность
      Nvl(Decode(n_row, 30, Sum(fam)),  0) as a30,
      Nvl(Decode(n_row, 30, Sum(cnt)),  0) as b30,
      Nvl(Decode(n_row, 30, Sum(area)), 0) as c30,
      -- Граждане из подразделений особого риска, не имеющие инвалидности
      Nvl(Decode(n_row, 31, Sum(fam)),  0) as a31,
      Nvl(Decode(n_row, 31, Sum(cnt)),  0) as b31,
      Nvl(Decode(n_row, 31, Sum(area)), 0) as c31,
      -- Семьи, потерявшие кормильца из числа граждан из подразделений особого риска
      Nvl(Decode(n_row, 32, Sum(fam)),  0) as a32,
      Nvl(Decode(n_row, 32, Sum(cnt)),  0) as b32,
      Nvl(Decode(n_row, 32, Sum(area)), 0) as c32,

      -- ============================================================
      -- Федеральный закон от 10 января 2002 года №2-ФЗ
      -- ============================================================
      -- Граждане, получившие суммарную (накопленную) эффективную дозу облучения, превышающую 25 сЗв (бэр)
      Nvl(Decode(n_row, 33, Sum(fam)),  0) as a33,
      Nvl(Decode(n_row, 33, Sum(cnt)),  0) as b33,
      Nvl(Decode(n_row, 33, Sum(area)), 0) as c33,

      -- ============================================================
      -- Итоги
      -- ============================================================
      -- Федеральный закон от 12 января 1995 года №5-ФЗ «О ветеранах»
      Nvl(Decode(n_row, 34, Sum(fam)),  0) as a34,
      Nvl(Decode(n_row, 34, Sum(cnt)),  0) as b34,
      Nvl(Decode(n_row, 34, Sum(area)), 0) as c34,
      -- Федеральный закон от 22 августа 2004 года №122-ФЗ
      Nvl(Decode(n_row, 35, Sum(fam)),  0) as a35,
      Nvl(Decode(n_row, 35, Sum(cnt)),  0) as b35,
      Nvl(Decode(n_row, 35, Sum(area)), 0) as c35,
      -- Федеральный закон от 24 ноября 1995 года №181-ФЗ «О социальной защите инвалидов в Российской Федерации»
      Nvl(Decode(n_row, 36, Sum(fam)),  0) as a36,
      Nvl(Decode(n_row, 36, Sum(cnt)),  0) as b36,
      Nvl(Decode(n_row, 36, Sum(area)), 0) as c36,
      -- Закон Российской Федерации от 15 мая 1991 года №1244-1
      Nvl(Decode(n_row, 37, Sum(fam)),  0) as a37,
      Nvl(Decode(n_row, 37, Sum(cnt)),  0) as b37,
      Nvl(Decode(n_row, 37, Sum(area)), 0) as c37,
      -- Федеральный закон от 26 ноября 1998 года №175-ФЗ
      Nvl(Decode(n_row, 38, Sum(fam)),  0) as a38,
      Nvl(Decode(n_row, 38, Sum(cnt)),  0) as b38,
      Nvl(Decode(n_row, 38, Sum(area)), 0) as c38,
      -- Постановление Верховного Совета Российской Федерации от 27 декабря 1991 года №2123-1
      Nvl(Decode(n_row, 39, Sum(fam)),  0) as a39,
      Nvl(Decode(n_row, 39, Sum(cnt)),  0) as b39,
      Nvl(Decode(n_row, 39, Sum(area)), 0) as c39,
      -- Федеральный закон от 10 января 2002 года №2-ФЗ
      Nvl(Decode(n_row, 40, Sum(fam)),  0) as a40,
      Nvl(Decode(n_row, 40, Sum(cnt)),  0) as b40,
      Nvl(Decode(n_row, 40, Sum(area)), 0) as c40,
      -- Итого
      Nvl(Decode(n_row, 41, Sum(fam)),  0) as a41,
      Nvl(Decode(n_row, 41, Sum(cnt)),  0) as b41,
      Nvl(Decode(n_row, 41, Sum(area)), 0) as c41
    from
      -- Выборка a, b и c по каждой строке (группировка по номеру строки)
      (select
          n_row,
          Nvl(Sum(fam_memb), 0) as fam, -- количество человек с членами семьи
          Nvl(Sum(cnt),      0) as cnt, -- количество носителей льгот
          Nvl(Sum(area),     0) as area -- площадь
        from
          -- Выборка каждого показателя в разрезе строк и семей + комплект строк с нулями, чтобы были все строки
          (select
              -- номер строки выходного документа
              n_row,
              -- количество льготников вместе с членами семьи
              Ceil(Sum(pc_count)) as fam_memb,
              -- количество льготников
              Count(*) as cnt,
              -- площадь берём наибольшую, т. к. гипотетически у нескольких льготников она могла оказаться разной из-за разных дат
              Max(area) as area
            from
              (select
                  data.region_id,
                  data.coll_id,
                  data.pc_count,
                  -- перевод категорий ПФ РФ в номер строки выходного документа
                  case
                    -- собственно данные
                    when levels.lvl=1 then Decode(data.n_cat, 010, 01, 011, 02, 012, 03, 020, 04, 051, 05, 030, 06, 060, 07, 061, 08, 062, 09, 064, 09, 063, 10, 140, 11, 150, 12, /*083, 13, 082, 13, 081, 13, 085, 13,*/ 083, 42, 082, 43, 081, 44, 085, 44, 084, 14, 091, 15, 092, 16, 093, 17, 098, 18, 101, 19, 102, 20, 141, 21, 350, 22, 340, 23, 341, 23, 342, 23, 122, 24, 121, 25, 123, 26, 128, 27, 132, 30, 131, 31, 351, 32, 111, 33)
                    -- подитоги по законам
                    when levels.lvl=2 then Decode(data.n_cat, 010, 34, 011, 34, 012, 34, 020, 34, 051, 34, 030, 34, 060, 34, 061, 34, 062, 34, 064, 34, 063, 34, 140, 35, 150, 35, 083, 36, 082, 36, 081, 36, 085, 36, 084, 36, 091, 37, 092, 37, 093, 37, 098, 37, 101, 37, 102, 37, 141, 37, 350, 37, 340, 37, 341, 37, 342, 37, 122, 38, 121, 38, 123, 38, 128, 38, 132, 39, 131, 39, 351, 39, 111, 40)
                    -- общий итог
                    when levels.lvl=3 then 41
                  end as n_row,
                  -- общая площадь жилья на дату суммы из сведений о жилищных условиях
                  uszn.ToNumberDef(uszn.pkPerson.GetRawPCReqValueOnDate(data.region_id, data.coll_id, 3760, 3845, null, data.payout_date), 0) as area
                from
                  -- утраиваем все строки: 1 - для собственно данных, 2 - для подитогов и 3 - для общего итога
                  (select id as lvl from uszn.u_dummy where id<=3) levels,
                  -- сведения о получении льготы на основании оплаченных сумм за период
                  (with
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
                      a.region_id,
                      a.pka_people_coll_id as people_id,
                      a.poi_payout_date as payout_date,
                      a.pc_count_applied_to as pc_count,
                      -- перевод признака учёта в категорию ПФ РФ
                      uszn.pkOutDocCol.GetPFRF_Cat(
                        a.region_id, a.pka_people_coll_id, a.pkaf_region_id, a.pkaf_id,
                        Trunc(a.poi_payout_date, 'mm'), Last_Day(a.poi_payout_date)) as n_cat,
                      -- коллектив ищем на дату суммы
                      uszn.pkPic.GetCollByRole(a.region_id, a.pka_people_coll_id, 46, a.poi_payout_date, 0, 0) as coll_id
                    from uszn.all_po_amounts a
                    where
                      (a.region_id, a.id) in (
                        select
                            a.region_id,
                            First_Value(a.id) over (
                              partition by a.region_id, a.poi_assigned_id
                              order by a.poi_payout_date desc, a.pc_count_applied_to desc, a.income_date desc, a.id) as amount_id
                          from uszn.all_po_amounts a
                          where
                            -- фильтр по району
                            a.region_id={region_id} and
                            -- виды выплат, заданные в параметрах выходного документа
                            (a.pka_kind_region_id, a.pka_kind_id) in ((104,29),(104,29)) and
                            -- источник финансирования - федеральный бюджет
                            a.finsrc_region_id=0 and a.finsrc_id=1 and
                            -- оплачено
                            a.status_kind_id=2 and
                            -- за период выборки
                            a.poi_payout_date between TRUNC(ADD_MONTHS(SYSDATE,-1),'MM') and TRUNC(SYSDATE,'MM')-1 and
                            ( -- фильтр по признакам учёта
                              ( -- признак учёта "Наличие документа «Сведения о получении льгот на ЖКУ на декабрь 2008 года»"
                                (a.pkaf_region_id, a.pkaf_id) in ((104, 339)) and
                                -- наличие соответствия в справочнике соответствия данных для обмена
                                -- для льготного основания, указанного  в сведениях о получении льгот
                                Exists(
                                  select 1
                                    from uszn.r_personal_doc_instances d, mapped_pkafs m
                                    where
                                      d.region_id=a.region_id and d.people_coll_id=a.pka_people_coll_id and
                                      -- реквизит "Правовое основание"
                                      d.class_id=7116 and
                                      -- slurp-ключ признака учёта ищем в персональном документе "Сведения о получении льгот..."
                                      m.pkaf_region_id*1000000+m.pkaf_id=uszn.ToIntDef(d.value)
                                )
                              ) or
                              -- остальные признаки учёта, при наличии соответствия в справочнике
                              (a.pkaf_region_id, a.pkaf_id) in (select pkaf_region_id, pkaf_id from mapped_pkafs)
                            ) /* фильтр по признакам учёта */
                          ) /* in */
                  ) data)
            where n_row is not null
            group by n_row, region_id, coll_id
            union all
            select id, 0, 0, 0 from uszn.u_dummy where id<45)
        group by n_row)
    group by n_row)