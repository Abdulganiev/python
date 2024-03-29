SELECT
	uszn.pkGen.GetDelimitedStringPart(row_title, '|', 1) as "№",
	uszn.pkGen.GetDelimitedStringPart(row_title, '|', 2) as "Показатель",
	uszn.pkGen.GetDelimitedStringPart(row_title, '|', 3) as "Ед. изм.",
	sum_total as "по ЯНАО"

from (
  select
      ud.id as stat_row_num,
      Decode(
        ud.id,
       15, '15.|Общее количество положительных решений (выданных документов, совершенных действий), принятых по результатам предоставления гос. (муниц.) услуги, в отношении заявителей - физических лиц|ед.|',
       16, '16.|Общее количество положительных решений (выданных документов, совершенных действий), принятых по результатам предоставления гос. (муниц.) услуги, в отношении заявителей - юр. лиц и (или) инд. предпринимателей|ед.|',
       17, '17.|Общее количество принятых в результате рассмотрения заявлений о предоставлении гос. (муниц.) услуги решений о приостановлении предоставления гос. (муниц.) услуги, в отношении заявителей – физических лиц|ед.|',
       18, '18.|Общее количество принятых в результате рассмотрения заявлений о предоставлении гос. (муниц.) услуги решений о приостановлении предоставления гос. (муниц.) услуги, в отношении заявителей – юр. лиц и (или) инд. предпринимателей|ед.|',
       19, '19.|Общее количество отказов (отрицательных решений), принятых по результатам рассмотрения заявлений о предоставлении гос. (муниц.) услуги, в отношении заявителей – физических лиц|ед.|',
       20, '20.|Общее количество отказов (отрицательных решений), принятых по результатам рассмотрения заявлений о предоставлении гос. (муниц.) услуги, в отношении заявителей – юр. лиц и (или) инд. предпринимателей|ед.|'
        ) as row_title,
      NVL(Sum(sk.id), 0) as sum_total
    from uszn.u_dummy ud, uszn.r$_stats_rkeys sk
    where ud.id between 15 and 20 and sk.kind_id(+)=ud.id
    group by ud.id)