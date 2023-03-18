INSERT INTO uszn.temp$_birth

select
mes.value as guid,
reg.custom_data,
uszn.ToDateISODef(dat.value) as date_information,
id_sv.value as id_information,
uszn.ToDateISODef(uszn.pkXMLImp.GetTagValueByName(reg.id, 'ДатаЗапис', 0, 0)) as az_date,
uszn.pkXMLImp.GetAttribValueByName(reg.id, 'НомерЗапис') as az_num,

(select uszn.pkXMLImp.GetAttribValueByName(zags.id, 'НаимСостСтат')
  from uszn.r$_parsed_xml_data zags
  where zags.owner_id=reg.id and zags.name='СостСтатЗаписи') as ZAGZ_status,

(select uszn.pkXMLImp.GetAttribValueByName(zags.id, 'КодЗАГС')
  from uszn.r$_parsed_xml_data zags
  where zags.owner_id=reg.id and zags.name='ОрганЗАГС') as ZAGZ_nom,

(select uszn.pkXMLImp.GetAttribValueByName(zags.id, 'НаимЗАГС')
  from uszn.r$_parsed_xml_data zags
  where zags.owner_id=reg.id and zags.name='ОрганЗАГС') as ZAGZ,

(select uszn.pkXMLImp.GetTagValueByName(birth.id, 'СчетРебен', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведСчетРебен'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as baby_nomer,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Фамилия', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведРодившемся'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ФИОРожд'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as baby_last_name,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Имя', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведРодившемся'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ФИОРожд'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as baby_first_name,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Отчество', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведРодившемся'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ФИОРожд'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as baby_middle_name,

(select uszn.ToDateISODef(nvl(uszn.pkXMLImp.GetTagValueByName(birth.id, 'ДатаРождКаленд', 0, 0), uszn.pkXMLImp.GetTagValueByName(birth.id, 'ДатаРожд', 0, 0)))
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведРодившемся'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as baby_birth_date,

(select uszn.pkXMLImp.GetTagValueByName(birth.id, 'ДатаРождКаленд', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведРодившемся'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as baby_birth_date_egisso,

(select uszn.pkXMLImp.GetTagValueByName(bp.id, 'НаимСтраны', 0, 1)||' '||uszn.pkXMLImp.GetTagValueByName(bp.id, 'МестоТекст', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведРодившемся'
       left join uszn.r$_parsed_xml_data bp on bp.owner_id=birth.id and bp.name='МестоРожден'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as baby_birth_place,

(select uszn.pkXMLImp.GetTagValueByName(bp.id, 'НаимСубъект', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведРодившемся'
       left join uszn.r$_parsed_xml_data bp on bp.owner_id=birth.id and bp.name='МестоРожден'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as baby_birth_place_sub,

(select uszn.pkXMLImp.GetTagValueByName(bp.id, 'Регион', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведРодившемся'
       left join uszn.r$_parsed_xml_data bp on bp.owner_id=birth.id and bp.name='МестоРожден'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as baby_birth_place_sub_nom,

(select uszn.pkXMLImp.GetTagValueByName(bp.id, 'ОКТМО', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведРодившемся'
       left join uszn.r$_parsed_xml_data bp on bp.owner_id=birth.id and bp.name='МестоРожден'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as baby_birth_place_oktmo,


(select uszn.pkXMLImp.GetTagValueByName(birth.id, 'СНИЛС', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведРодившемся'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as baby_snils,

case when (select uszn.pkXMLImp.GetTagValueByName(birth.id, 'Пол', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведРодившемся'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег')=1 then 'М' else 'Ж' end as baby_sex,

case when (select uszn.pkXMLImp.GetTagValueByName(birth.id, 'ЖивМертв', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведРодившемся'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег')=0 then 'Живорожденный' else 'Мертворожденный' end as baby_Alive_Dead,

(select uszn.pkXMLImp.GetTagValueByName(max(svid.id), 'СерияСвидет', 0, 1)
 from uszn.r$_parsed_xml_data svid
 where svid.owner_id=reg.id and svid.name='СвидетРожд') as sv_ser,

(select uszn.pkXMLImp.GetTagValueByName(max(svid.id), 'НомерСвидет', 0, 1)
 from uszn.r$_parsed_xml_data svid
 where svid.owner_id=reg.id and svid.name='СвидетРожд') as sv_num,

(select uszn.ToDateISODef(uszn.pkXMLImp.GetTagValueByName(max(svid.id), 'ДатаВыдСвидет', 0, 1))
 from uszn.r$_parsed_xml_data svid
 where svid.owner_id=reg.id and svid.name='СвидетРожд') as sv_date,

(select uszn.pkXMLImp.GetTagValueByName(max(svid.id), 'ДатаВыдСвидет', 0, 1)
 from uszn.r$_parsed_xml_data svid
 where svid.owner_id=reg.id and svid.name='СвидетРожд') as sv_date_egisso,

(select uszn.pkXMLImp.GetTagValueByName(sved.id, 'КолРодДетей', 0, 1)
  from uszn.r$_parsed_xml_data sved where sved.owner_id=reg.id and sved.name='ПрдСведРег') as kol_vo,

case when (select uszn.pkXMLImp.GetTagValueByName(sved.id, 'ПрМать', 0, 0)
       from uszn.r$_parsed_xml_data sved
        where sved.owner_id=reg.id and sved.name='ПрдСведРег')=1 then 'Данные о матери отсутствуют' else '' end as mama,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Фамилия', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ФИО'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as mama_last_name,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Имя', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ФИО'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as mama_first_name,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Отчество', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ФИО'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as mama_middle_name,

(select uszn.ToDateISODef(nvl(uszn.pkXMLImp.GetTagValueByName(birth.id, 'ДатаРождКаленд', 0, 0), uszn.pkXMLImp.GetTagValueByName(birth.id, 'ДатаРожд', 0, 0)))
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as mama_birth_date,

(select uszn.pkXMLImp.GetTagValueByName(birth.id, 'ДатаРождКаленд', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as mama_birth_date_egisso,

(select uszn.pkXMLImp.GetTagValueByName(bp.id, 'НаимСтраны', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
       left join uszn.r$_parsed_xml_data bp on bp.owner_id=birth.id and bp.name='Гражданство'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as mama_citizenship,

(select uszn.pkXMLImp.GetTagValueByName(bp.id, 'НаимСтраны', 0, 1)||' '||uszn.pkXMLImp.GetTagValueByName(bp.id, 'МестоТекст', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
       left join uszn.r$_parsed_xml_data bp on bp.owner_id=birth.id and bp.name='МестоРожден'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as mama_birth_place,

(select uszn.pkXMLImp.GetTagValueByName(birth.id, 'СНИЛС', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as mama_snils,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'НаимДок', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='УдЛичнФЛ'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as mama_dul_type,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'СерНомДок', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='УдЛичнФЛ'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as mama_dul_ser_nom,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'ВыдДок', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='УдЛичнФЛ'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as mama_dul_issued,

(select uszn.ToDateISODef(uszn.pkXMLImp.GetTagValueByName(fio.id, 'ДатаДокКаленд', 0, 1))
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='УдЛичнФЛ'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as mama_dul_data,

NVL(
(select uszn.pkXMLImp.GetTagValueByName(adr_text.id, 'АдрРФТекст', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='АдрМЖ'
       inner join uszn.r$_parsed_xml_data adr on adr.owner_id=fio.id and adr.name='АдрМЖРФ'
       inner join uszn.r$_parsed_xml_data adr_text on adr_text.owner_id=adr.id and adr_text.name='АдрРФНеФИАС'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег'),
(select uszn.pkXMLImp.GetTagValueByName(adr.id, 'АдрТекст', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведМать'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='АдрМЖ'
       inner join uszn.r$_parsed_xml_data adr on adr.owner_id=fio.id and adr.name='АдрМЖИн'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') ) as mama_adr,

case when (select uszn.pkXMLImp.GetTagValueByName(sved.id, 'ПрОтец', 0, 0)
       from uszn.r$_parsed_xml_data sved
        where sved.owner_id=reg.id and sved.name='ПрдСведРег')=1 then 'Данные об отце отсутствуют' else '' end as papa,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Фамилия', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ФИО'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_last_name,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Имя', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ФИО'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_first_name,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Отчество', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ФИО'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_middle_name,

(select uszn.ToDateISODef(nvl(uszn.pkXMLImp.GetTagValueByName(birth.id, 'ДатаРождКаленд', 0, 0), uszn.pkXMLImp.GetTagValueByName(birth.id, 'ДатаРожд', 0, 0)))
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_birth_date,

(select uszn.pkXMLImp.GetTagValueByName(birth.id, 'ДатаРождКаленд', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_birth_date_egisso,

(select uszn.pkXMLImp.GetTagValueByName(bp.id, 'НаимСтраны', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
       left join uszn.r$_parsed_xml_data bp on bp.owner_id=birth.id and bp.name='Гражданство'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_citizenship,

(select uszn.pkXMLImp.GetTagValueByName(bp.id, 'НаимСтраны', 0, 1)||' '||uszn.pkXMLImp.GetTagValueByName(bp.id, 'МестоТекст', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
       left join uszn.r$_parsed_xml_data bp on bp.owner_id=birth.id and bp.name='МестоРожден'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_birth_place,

(select uszn.pkXMLImp.GetTagValueByName(birth.id, 'СНИЛС', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_snils,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'НаимДок', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='УдЛичнФЛ'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_dul_type,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'СерНомДок', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='УдЛичнФЛ'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_dul_ser_nom,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'ВыдДок', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='УдЛичнФЛ'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_dul_issued,

(select uszn.ToDateISODef(uszn.pkXMLImp.GetTagValueByName(fio.id, 'ДатаДокКаленд', 0, 1))
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='УдЛичнФЛ'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_dul_data,

NVL(
(select uszn.pkXMLImp.GetTagValueByName(adr_text.id, 'АдрРФТекст', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='АдрМЖ'
       inner join uszn.r$_parsed_xml_data adr on adr.owner_id=fio.id and adr.name='АдрМЖРФ'
       inner join uszn.r$_parsed_xml_data adr_text on adr_text.owner_id=adr.id and adr_text.name='АдрРФНеФИАС'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег'),
(select uszn.pkXMLImp.GetTagValueByName(adr.id, 'АдрТекст', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='АдрМЖ'
       inner join uszn.r$_parsed_xml_data adr on adr.owner_id=fio.id and adr.name='АдрМЖИн'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') ) as papa_adr,

case when (select uszn.pkXMLImp.GetTagValueByName(sved.id, 'ПрСведДокОснОтец', 0, 0)
       from uszn.r$_parsed_xml_data sved
        where sved.owner_id=reg.id and sved.name='ПрдСведРег')=1 then 'Отсутствуют сведений о документе, на основании которого указаны сведения об отце' else '' end as papa_osn,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'НаимТипЗапис', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведДокОснОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ЗапАктОсн'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_osn_type,

(select uszn.ToDateISODef(uszn.pkXMLImp.GetTagValueByName(fio.id, 'ДатаЗапис', 0, 1))
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведДокОснОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ЗапАктОсн'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_osn_data,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'НомерЗапис', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведДокОснОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ЗапАктОсн'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_osn_nom,

(select uszn.pkXMLImp.GetTagValueByName(zagz.id, 'КодЗАГС', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведДокОснОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ЗапАктОсн'
       inner join uszn.r$_parsed_xml_data zagz on zagz.owner_id=fio.id and zagz.name='ОрганЗАГС'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_osn_kod,

(select uszn.pkXMLImp.GetTagValueByName(zagz.id, 'НаимЗАГС', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведДокОснОтец'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=birth.id and fio.name='ЗапАктОсн'
       inner join uszn.r$_parsed_xml_data zagz on zagz.owner_id=fio.id and zagz.name='ОрганЗАГС'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as papa_osn_name,

(select uszn.pkXMLImp.GetTagValueByName(birth.id, 'НаимДок', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведДокРод'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as birth_doc_type,


(select uszn.ToDateISODef(uszn.pkXMLImp.GetTagValueByName(birth.id, 'ДатаДокКаленд', 0, 1))
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведДокРод'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as birth_doc_data,

(select uszn.pkXMLImp.GetTagValueByName(birth.id, 'СерНомДок', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведДокРод'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as birth_doc_ser_nom,

(select uszn.pkXMLImp.GetTagValueByName(birth.id, 'НаимОрг', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data birth on birth.owner_id=sved.id and birth.name='СведДокРод'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as birth_doc_kontora

from uszn.r$_parsed_xml_data reg
     inner join uszn.r$_parsed_xml_data dat
  on reg.name='СведРегРожд' and reg.owner_id=dat.owner_id and dat.name='ДатаСвед'
     inner join uszn.r$_parsed_xml_data id_sv
  on reg.owner_id=id_sv.owner_id and id_sv.name='ИдСвед'
     inner join uszn.r$_parsed_xml_data mes
  on reg.custom_data=mes.custom_data and mes.name='MessageID'
  