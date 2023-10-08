INSERT INTO uszn.temp$_pfr_work

select
r$.custom_data,
uszn.pkXMLImp.GetTagValueByName(
      uszn.pkXMLImp.GetTagID(-1, 'MessageMetadata', 0, 0), 'MessageId', 0, 0) as MessageId,
 To_Char(
  uszn.pkXML.StrToDateTime(
    uszn.pkXMLImp.GetTagValueByName(
      uszn.pkXMLImp.GetTagID(-1, 'MessageMetadata', 0, 0),
      'SendingTimestamp', 0, 0), 1, 0), 'dd.mm.yyyy hh24:mi:ss') as date_request,
 To_Char(
  uszn.pkXML.StrToDateTime(
    uszn.pkXMLImp.GetTagValueByName(
      uszn.pkXMLImp.GetTagID(-1, 'MessageMetadata', 0, 0),
      'DeliveryTimestamp', 0, 0), 1, 0), 'dd.mm.yyyy hh24:mi:ss') as date_response,
 pc.region_id, pc.id,
 uszn.pkXMLImp.GetTagValueByName(r$.id, 'FamilyName', 0, 0) as F,
 uszn.pkXMLImp.GetTagValueByName(r$.id, 'FirstName', 0, 0) as I,
 uszn.pkXMLImp.GetTagValueByName(r$.id, 'Patronymic', 0, 0) as O,
 uszn.pkOutDocCol.FormatPensInsuranceNum(uszn.pkXMLImp.GetTagValueByName(r$.id, 'Snils', 0, 0)) as SNILS,
  to_date('01.'||LPAD(uszn.pkXML.GMonthStrToInt(uszn.pkXMLImp.GetTagValueByName(p.id, 'ReportMonth', 1, 0), 1), 2, '0')||'.'||
  uszn.pkXMLImp.GetTagValueIntByName(p.id, 'ReportYear', 1, 1)) as date_work,
  uszn.pkXMLImp.GetTagValueByName(p.id, 'JobStatus', 1, 0) as works
from uszn.r$_parsed_xml_data r$
   join
  uszn.r$_parsed_xml_data pps
  on pps.owner_id=r$.id and r$.name='WorkFactResponse'
   join
  uszn.r$_parsed_xml_data p
  on p.owner_id=pps.id and p.name='Period' and pps.name='Periods'
   join
  uszn.r_people_and_colls pc
  on  uszn.pkXMLImp.GetTagValueByName(r$.id, 'Snils', 0, 0)=pc.snils
