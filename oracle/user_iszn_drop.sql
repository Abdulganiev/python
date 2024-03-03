select 'alter system kill session '''||sid||','||serial#||''''
    from v$session where username not in ('ADMIN104', 'BERS104', 'USZN')