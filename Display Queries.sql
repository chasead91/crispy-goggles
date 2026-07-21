SELECT * FROM reader;

SELECT * FROM sitter;

-- Lobby View
select
    si.name AS 'Sitter',
    r.name AS 'Reader',
    r.offering AS 'Session Type',
    s.queue_position AS 'Line Position',
    s.status AS 'Session Status'
from session s
left join reader r on s.reader_id = r.reader_id
left JOIN sitter si on s.sitter_id = si.sitter_id;

-- Admin Views

