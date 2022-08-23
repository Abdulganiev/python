INSERT INTO uszn.temp$_death

select
mes.value as guid,
reg.custom_data,
uszn.ToDateISODef(dat.value) as date_information,
id_sv.value as id_information,
uszn.ToDateISODef(uszn.pkXMLImp.GetAttribValueByName(reg.id, 'ДатаЗапис')) as az_date,
uszn.pkXMLImp.GetAttribValueByName(reg.id, 'НомерЗапис') as az_num,

(select uszn.pkXMLImp.GetAttribValueByName(zags.id, 'НаимСтатус')
  from uszn.r$_parsed_xml_data zags
  where zags.owner_id=reg.id and zags.name='СтатусЗаписи') as ZAGZ_status,

(select uszn.pkXMLImp.GetAttribValueByName(zags.id, 'КодЗАГС')
  from uszn.r$_parsed_xml_data zags
  where zags.owner_id=reg.id and zags.name='ОрганЗАГС') as ZAGZ_nom,

(select uszn.pkXMLImp.GetAttribValueByName(zags.id, 'НаимЗАГС')
  from uszn.r$_parsed_xml_data zags
  where zags.owner_id=reg.id and zags.name='ОрганЗАГС') as ZAGZ,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Фамилия', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=death.id and fio.name='ФИОУмер'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as last_name,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Имя', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=death.id and fio.name='ФИОУмер'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as first_name,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Отчество', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
       inner join uszn.r$_parsed_xml_data fio on fio.owner_id=death.id and fio.name='ФИОУмер'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as middle_name,

(select uszn.DateToChar(uszn.pkXMLImp.GetTagValueDateByName(death.id, 'ДатаРождКаленд', 0, 0))
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as birth_date,

(select uszn.pkXMLImp.GetTagValueByName(death.id, 'ДатаРождКаленд', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as birth_date_egisso,

(select uszn.pkXMLImp.GetTagValueByName(bp.id, 'НаимСтраны', 0, 1)||' '||uszn.pkXMLImp.GetTagValueByName(bp.id, 'МестоТекст', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
       left join uszn.r$_parsed_xml_data bp on bp.owner_id=death.id and bp.name='МестоРожден'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as birth_place,

(select uszn.pkXMLImp.GetTagValueByName(death.id, 'СНИЛС', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as snils,

(select uszn.pkXMLImp.GetTagValueByName(death.id, 'Пол', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as sex,

(select uszn.ToDateISODef(uszn.pkXMLImp.GetTagValueByName(death.id, 'ДатаСмертКаленд', 0, 0))
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as death_date,

(select uszn.pkXMLImp.GetTagValueByName(death_data.id, 'ПрДень', 0, 0)||'.'||
        uszn.pkXMLImp.GetTagValueByName(death_data.id, 'Месяц', 0, 0)||'.'||
        uszn.pkXMLImp.GetTagValueByName(death_data.id, 'Год', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
       left  join uszn.r$_parsed_xml_data death_data on death_data.owner_id=death.id and death_data.name='ДатаСмертДок'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as death_date_doc,

(select uszn.pkXMLImp.GetTagValueByName(death.id, 'ДатаСмертКаленд', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as death_date_egisso,

(select uszn.pkXMLImp.GetTagValueByName(svid.id, 'СерияСвидет', 0, 1)
 from uszn.r$_parsed_xml_data svid
 where svid.owner_id=reg.id and svid.name='СведСвидет') as sv_ser,

(select uszn.pkXMLImp.GetTagValueByName(svid.id, 'НомерСвидет', 0, 1)
 from uszn.r$_parsed_xml_data svid
 where svid.owner_id=reg.id and svid.name='СведСвидет') as sv_num,

(select uszn.ToDateISODef(uszn.pkXMLImp.GetTagValueByName(svid.id, 'ДатаВыдСвидет', 0, 1))
 from uszn.r$_parsed_xml_data svid
 where svid.owner_id=reg.id and svid.name='СведСвидет') as sv_date,

(select uszn.pkXMLImp.GetTagValueByName(svid.id, 'ДатаВыдСвидет', 0, 1)
 from uszn.r$_parsed_xml_data svid
 where svid.owner_id=reg.id and svid.name='СведСвидет') as sv_date_egisso,

(select uszn.pkXMLImp.GetTagValueByName(rprf.id, 'АдрРФТекст', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
       left join uszn.r$_parsed_xml_data rp on rp.owner_id=death.id and rp.name='МЖПосл'
       left join uszn.r$_parsed_xml_data rprf on rprf.owner_id=rp.id and rprf.name='МЖПослРФ'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as residence_place,

(select uszn.pkXMLImp.GetTagValueByName(dul.id, 'НаимДок', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
       left join uszn.r$_parsed_xml_data dul on dul.owner_id=death.id and dul.name='УдЛичнФЛ'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as dul_type,

(select uszn.pkXMLImp.GetTagValueByName(dul.id, 'СерНомДок', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
       left join uszn.r$_parsed_xml_data dul on dul.owner_id=death.id and dul.name='УдЛичнФЛ'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as dul_nom,

(select uszn.ToDateISODef(uszn.pkXMLImp.GetTagValueByName(dul.id, 'ДатаДок', 0, 1))
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
       left join uszn.r$_parsed_xml_data dul on dul.owner_id=death.id and dul.name='УдЛичнФЛ'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as dul_date,

(select uszn.pkXMLImp.GetTagValueByName(dp.id, 'МестоТекст', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
       left join uszn.r$_parsed_xml_data dp on dp.owner_id=death.id and dp.name='МестоСмерт'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as death_place,

(select uszn.pkXMLImp.GetTagValueByName(dp.id, 'Регион', 0, 1)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data death on death.owner_id=sved.id and death.name='СведУмер'
       left join uszn.r$_parsed_xml_data dp on dp.owner_id=death.id and dp.name='МестоСмерт'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as death_place_region



from uszn.r$_parsed_xml_data reg
     inner join uszn.r$_parsed_xml_data dat
  on reg.name='СведРегСмерт' and reg.owner_id=dat.owner_id and dat.name='ДатаСвед'
     inner join uszn.r$_parsed_xml_data id_sv
  on reg.owner_id=id_sv.owner_id and id_sv.name='ИдСвед'
     inner join uszn.r$_parsed_xml_data mes
  on reg.custom_data=mes.custom_data and mes.name='MessageID'
