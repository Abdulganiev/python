select count(*)
from uszn.r_yanao_uc_messages
where
 (export_kind_id in (3, 4) and is_incoming=1 and message_kind=1 and process_status<>1)
 or
 (export_kind_id=5 and is_incoming=0 and message_kind=1 and delivery_status<>1)
