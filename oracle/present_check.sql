select distinct count(*)
from uszn.temp$_v_birth t
where baby_birth_date>to_date('28.02.2023')