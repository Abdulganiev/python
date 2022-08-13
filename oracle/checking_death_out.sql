select

Nvl(uszn.DateToChar(uszn.pkXMLImp.GetTagValueDateByName(reg.id, 'ДатаЗапис', 0, 1)),
    uszn.pkEgrZags.DescribeDocumentedDate(uszn.pkXMLImp.GetTagID(reg.id, 'ДатаЗаписДок', 0, 0), 0)) as az_date,

  uszn.pkXMLImp.GetAttribValueByName(reg.id, 'НомерЗаписЕГР') as az_num,
  
  uszn.pkXMLImp.GetAttribValueByName(reg.id, 'НомАГССвид') as az_zags_num,
  
Coalesce(uszn.pkEgrZags.DecodeActRecStateAndStatus(uszn.pkXMLImp.GetAttribValueByName(reg.id, 'КодСостСтат'), 0),
           'Неизвестный код: '||uszn.pkXMLImp.GetAttribValueByName(reg.id, 'КодСостСтат')) as az_status,
  
(select uszn.pkXMLImp.GetAttribValueByName(zags.id, 'НаимЗАГС')
  from uszn.r$_parsed_xml_data zags
  where zags.owner_id=reg.id and zags.name='ОрганЗАГС') as AZ,
  
(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Фамилия', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data fio on fio.owner_id=sved.id and fio.name='ФИОУмер'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as last_name,
 
(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Имя', 0, 0)
  from  uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data fio on fio.owner_id=sved.id and fio.name='ФИОУмер'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as first_name,

(select uszn.pkXMLImp.GetTagValueByName(fio.id, 'Отчество', 0, 0)
  from uszn.r$_parsed_xml_data sved inner join uszn.r$_parsed_xml_data fio on fio.owner_id=sved.id and fio.name='ФИОУмер'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as middle_name,
 
(select Nvl(uszn.DateToChar(uszn.pkXMLImp.GetTagValueDateByName(sved.id, 'ДатаРождКаленд', 0, 1)),
            uszn.pkEgrZags.DescribeDocumentedDate(uszn.pkXMLImp.GetTagID(sved.id, 'ДатаРождДок', 0, 0), 0))
  from uszn.r$_parsed_xml_data reg1 join uszn.r$_parsed_xml_data sved on sved.owner_id=reg1.id and sved.name='ПрдСведРег'
  where reg1.id=reg.id) as birth_date,
 
(select (case when bp.id is not null then uszn.pkXMLImp.GetAttribValueByName(bp.id, 'МестоТекст') end)
  from uszn.r$_parsed_xml_data sved left join uszn.r$_parsed_xml_data bp on bp.owner_id=sved.id and bp.name='МестоРожден'
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as birth_place,

(select Nvl(uszn.DateToChar(uszn.pkXMLImp.GetTagValueDateByName(sved.id, 'ДатаСмертКаленд', 0, 1)),
            uszn.pkEgrZags.DescribeDocumentedDate(uszn.pkXMLImp.GetTagID(sved.id, 'ДатаСмертДок', 0, 0), 0))
  from uszn.r$_parsed_xml_data sved
  where sved.owner_id=reg.id and sved.name='ПрдСведРег') as death_date,
 
(select uszn.pkXMLImp.GetTagValueByName(svid.id, 'СерияСвидет', 0, 0)
 from uszn.r$_parsed_xml_data svid
 where svid.owner_id=reg.id and svid.name='СвидетСмерт') as sv_ser,

(select uszn.pkXMLImp.GetTagValueByName(svid.id, 'НомерСвидет', 0, 0)
 from uszn.r$_parsed_xml_data svid
 where svid.owner_id=reg.id and svid.name='СвидетСмерт') as sv_num,

(select Nvl(uszn.DateToChar(uszn.pkXMLImp.GetTagValueDateByName(svid.id, 'ДатаВыдСвидет', 0, 1)),
            uszn.pkEgrZags.DescribeDocumentedDate(uszn.pkXMLImp.GetTagID(svid.id, 'ДатаВыдСвидетДок'), 0))
 from uszn.r$_parsed_xml_data svid
 where svid.owner_id=reg.id and svid.name='СвидетСмерт') as sv_date


from uszn.r$_parsed_xml_data r$
     left join
     (select id, owner_id , First_Value(id) over (partition by owner_id order by id) as first_id
        from uszn.r$_parsed_xml_data where name='СведРегСмерт') reg
  on reg.owner_id=r$.id
where r$.name='СведОтветАГС'
order by r$.id, reg.id