INSERT INTO uszn.temp$_sfr_power

select
    uszn.pkXMLImp.GetTagValueByName(
      uszn.pkXMLImp.GetTagID(-1, 'MessageMetadata', 0, 0),
      'MessageId', 0, 0) as MessageId,

  To_Char(
  uszn.pkXML.StrToDateTime(
    uszn.pkXMLImp.GetTagValueByName(
      uszn.pkXMLImp.GetTagID(-1, 'MessageMetadata', 0, 0),
      'SendingTimestamp', 0, 0),
    1, 0), 'dd.mm.yyyy hh24:mi:ss') as SendingTimestamp,
      
  To_Char(
  uszn.pkXML.StrToDateTime(
    uszn.pkXMLImp.GetTagValueByName(
      uszn.pkXMLImp.GetTagID(-1, 'MessageMetadata', 0, 0),
      'DeliveryTimestamp', 0, 0),
    1, 0), 'dd.mm.yyyy hh24:mi:ss') as DeliveryTimestamp,

  uszn.pkOutDocCol.FormatPensInsuranceNum(uszn.pkXMLImp.GetTagValueByName(reg.id, 'Snils', 0, 0)) as snils,
  uszn.pkXMLImp.GetTagValueByName(reg.id, 'FamilyName', 0, 0) as last_name,
  uszn.pkXMLImp.GetTagValueByName(reg.id, 'FirstName', 0, 0) as first_name,
  uszn.pkXMLImp.GetTagValueByName(reg.id, 'Patronymic', 0, 0) as middle_name,

  to_date('01.'||uszn.pkXML.GMonthStrToInt(uszn.pkXMLImp.GetTagValueByName(p.id, 'ReportMonth', 1, 0), 1)
               ||'.'||uszn.pkXMLImp.GetTagValueIntByName(p.id, 'ReportYear', 1, 1)) as month,
   case uszn.pkXMLImp.GetTagValueByName(p.id, 'JobStatus', 1, 0)
      when 'D' then 'Да'
      when 'N' then 'Нет' end as fact_power
     
from uszn.r$_parsed_xml_data reg
     join
     uszn.r$_parsed_xml_data pps
  on reg.name='WorkFactResponse' and pps.owner_id=reg.id
     join
     uszn.r$_parsed_xml_data p
  on p.owner_id=pps.id and p.name='Period' and pps.name='Periods'