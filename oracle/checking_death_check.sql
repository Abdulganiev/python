select
 (select uszn.pkXMLImp.GetAttribValueByName(resp.id, 'РезОбраб')
   from uszn.r$_parsed_xml_data resp
        left join uszn.r$_parsed_xml_data reg1
     on reg1.owner_id=resp.id and reg1.name='СведРегСмерт'
   where resp.id=r$.id and (reg1.id is null or (reg1.id=reg.id and reg1.id=reg.first_id))  ) as rezult

from uszn.r$_parsed_xml_data r$
     left join
     (select id, owner_id , First_Value(id) over (partition by owner_id order by id) as first_id
        from uszn.r$_parsed_xml_data where name='СведРегСмерт') reg
  on reg.owner_id=r$.id
where r$.name='СведОтветАГС'
order by r$.id, reg.id

-- '1' - 'сведения в ЕГР ЗАГС найдены'
-- '2' - 'сведения в ЕГР ЗАГС отсутствуют или не переданы из региональной системы   '
-- '3' - 'нельзя однозначно определить сведения в ЕГР ЗАГС, требуется уточнение сведений в запросе'
-- '4' - 'сведения в ЕГР ЗАГС найдены, но не могут быть переданы из-за ошибок валидации по действующим форматам ВС'