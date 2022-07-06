select
 'В'||
  RPad('1.0', 10)||
  '       030-030-999999'||
  RPad(uszn.pkInstance.GetSettingValue('CUSTOMER_NAME'), 100) as f$_3
from dual
