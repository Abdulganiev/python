select *
from
(select 
  '0'||pc.region_id||'-'||uszn.pkTSrv.GetRegionName(pc.region_id)||' - список умерших',
  pc.region_id||'-'||pc.id,
  pc.id,
  uszn.pkPerson.DescribeManColl(pc.region_id, pc.id, 0),
  pc.death_date,
  pc.close_date,
  z.F||' '||z.I||' '||z.O||' '||z.DR,
  z.ds,
  z.ds2,
  z.d_akt,
  z.n_akt
from
 uszn.v_people_and_colls pc,
(select distinct last_name as f, first_name as i, middle_name as o,
         uszn.pkXML.StrToDate(birth_date) as dr,
         uszn.pkXML.StrToDate(death_date) as ds, death_date as ds2, record_date as d_akt, record_num as n_akt
from
  (select fn.value as first_name, mn.value as middle_name, ln.value as last_name,
          bd.value as birth_date, dd.value as death_date, uszn.pkXML.StrToDate(dz.value) as record_date, nz.value as record_num
     from uszn.r$_parsed_xml_data rec, uszn.r$_parsed_xml_data dz, uszn.r$_parsed_xml_data nz, uszn.r$_parsed_xml_data st,
          uszn.r$_parsed_xml_data fn, uszn.r$_parsed_xml_data mn, uszn.r$_parsed_xml_data ln, uszn.r$_parsed_xml_data bd, uszn.r$_parsed_xml_data dd
     where rec.name='regDeath' and  st.value!='03' and -- исключаем записи "Аннулирование записи"
           dz.owner_id=rec.id and dz.name='recDate' and nz.owner_id=rec.id and nz.name='recNum' and st.owner_id=rec.id and st.name='recStatus' and
           fn.owner_id(+)=rec.id and fn.name(+)='firstName' and mn.name(+)='middleName' and mn.owner_id(+)=rec.id and ln.name(+)='lastName' and ln.owner_id(+)=rec.id and
           bd.name(+)='birthDate' and bd.owner_id(+)=rec.id and dd.name(+)='deathDate' and dd.owner_id(+)=rec.id)) z
where
    Translate(UPPER(pc.last_name), 'Ё', 'Е')   = Translate(UPPER(z.F), 'Ё', 'Е') and
    Translate(UPPER(pc.first_name), 'Ё', 'Е')  = Translate(UPPER(z.I), 'Ё', 'Е') and
    Translate(UPPER(pc.middle_name), 'Ё', 'Е') = Translate(UPPER(z.O), 'Ё', 'Е') and
    pc.birth_date=z.DR and pc.death_date is null and pc.close_date is null
union
select distinct
    '0'||t1.region_id||'-'||uszn.pkTSrv.GetRegionName(t1.region_id)||' - список умерших' as name,
    t1.region_id||'-'||t1.id,
    t1.id as id,
    uszn.pkPerson.DescribeManColl(t1.region_id, t1.id, 0) as pc_desc,
    t1.death_date,
    t1.close_date,
    t3.last_name||' '||t3.first_name||' '||t3.middle_name||' '||t3.birth_date as az_desc,
    t3.death_date az_dt,
    t3.death_date_egisso az_dt_eg,
    t3.az_date,
    t3.az_num
from uszn.v_people_and_colls t1 inner join
(select region_id, pka_people_coll_id as people_id
 from uszn.all_asg_periods
 where --region_id=59 and
       trunc(sysdate, 'mm') between date_start and date_end and (pka_kind_region_id, pka_kind_id) in
       ( (000,133), (000,022), (000,147), (000,134), (000,132), (000,104),  -- авто
         (104,076), (104,021), (104,080), (104,078), (104,081), (104,014),  /*звания*/
         (000,142), (000,137), (104,029), (104,053), /*ЖКВ*/
         (104,075), (104,058), (104,057), (104,268), /*мат_капитал*/
         (000,165), (000,164), (000,161), (104,112), (104,213), (104,063), (104,061), (104,206), /*МСЭ*/
         (104,066), (104,088), /*опека*/
         (104,011), (104,051), (104,050), /*пенсия*/
         (000,119), (000,002), (104,067), (104,047), (104,261), (104,211), /*пособие на детей*/
         (000,153), (000,112), (000,152), (000,101), /*проезд*/
         (104,210), -- соц.помощник
         (104,009), /*ДМО*/
         (104,005), (104,016), /*55-зао до 31.12.2016*/
         (104,084), (104,083), /*55-зао с 01.01.2017 до 31.12.2020*/
         (104,279), /*ежемесячная ГСП с 01.01.2021*/
         (104,278), (104,277), (104,283), /*соц.контракт с 01.01.2021*/
         (104,276), (104,070), (104,069), (104,049),  /*55*/
         (104,294), (104,241), (104,060), (104,212), (104,055), (104,028), (104,027), (104,013), (104,052), (104,010), (104,002), (104,007), (104,048), -- 62зао
         (000,167), (000,148), (000,129), (000,168), (104,012), (104,273), (104,295), (104,285), (104,062), (104,266), (104,298)) -- прочее
 union
 select region_id, pka_payee_pc_id
 from uszn.all_asg_periods
 where --region_id=59 and
       trunc(sysdate, 'mm') between date_start and date_end and (pka_kind_region_id, pka_kind_id) in
       ( (000,133), (000,022), (000,147), (000,134), (000,132), (000,104),  -- авто
         (104,076), (104,021), (104,080), (104,078), (104,081), (104,014),  /*звания*/
         (000,142), (000,137), (104,029), (104,053), /*ЖКВ*/
         (104,075), (104,058), (104,057), (104,268), /*мат_капитал*/
         (000,165), (000,164), (000,161), (104,112), (104,213), (104,063), (104,061), (104,206), /*МСЭ*/
         (104,066), (104,088), /*опека*/
         (104,011), (104,051), (104,050), /*пенсия*/
         (000,119), (000,002), (104,067), (104,047), (104,261), (104,211), /*пособие на детей*/
         (000,153), (000,112), (000,152), (000,101), /*проезд*/
         (104,210), -- соц.помощник
         (104,009), /*ДМО*/
         (104,005), (104,016), /*55-зао до 31.12.2016*/
         (104,084), (104,083), /*55-зао с 01.01.2017 до 31.12.2020*/
         (104,279), /*ежемесячная ГСП с 01.01.2021*/
         (104,278), (104,277), (104,283), /*соц.контракт с 01.01.2021*/
         (104,276), (104,070), (104,069), (104,049),  /*55*/
         (104,294), (104,241), (104,060), (104,212), (104,055), (104,028), (104,027), (104,013), (104,052), (104,010), (104,002), (104,007), (104,048), -- 62зао
         (000,167), (000,148), (000,129), (000,168), (104,012), (104,273), (104,295), (104,285), (104,062), (104,266), (104,298)) -- прочее
       ) t2
on t1.death_date is null and t1.region_id=t2.region_id and t1.id=t2.people_id and t1.is_coll_instance=0
inner join uszn.temp$_death t3
on Translate(UPPER(t1.last_name), 'Ё', 'Е')   = Translate(UPPER(t3.last_name), 'Ё', 'Е')   and
   Translate(UPPER(t1.first_name), 'Ё', 'Е')  = Translate(UPPER(t3.first_name), 'Ё', 'Е')  and
   Translate(UPPER(t1.middle_name), 'Ё', 'Е') = Translate(UPPER(t3.middle_name), 'Ё', 'Е') and
   t1.birth_date = t3.birth_date and t1.close_date is null and
   replace(t3.dul_nom, ' ', '') = replace(uszn.pkPerson.GetPersonalReq(t1.region_id, t1.id, 19)||uszn.pkPerson.GetPersonalReq(t1.region_id, t1.id, 20), ' ', '')
)