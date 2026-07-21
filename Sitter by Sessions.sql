-- Sitter by Sessions
select
    se.status,
    s.name AS 'Sitter',
    r.name AS 'Reader',
    r.offering AS 'Session Type'
from session se
left join sitter s on se.sitter_id = s.sitter_id
left join reader r on se.reader_id = r.reader_id;