-- Available Readers
select r.name
from reader r
left join (
    select distinct r.name
    from reader r
    left join session s on r.reader_id = s.reader_id
    where s.status = 'In Progress'
) a on r.name = a.name
where a.name is null;
