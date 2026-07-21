select
    r.reader_id as "Reader ID",
    r.name as "Reader",
    s.sitter_id as "Sitter ID",
    s.name as "Sitter",
    se.queue_position,
    se.status
from session se
left join reader r on se.reader_id = r.reader_id
left join sitter s on se.sitter_id = s.sitter_id
order by r.name, se.queue_position;