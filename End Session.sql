-- End Session
UPDATE session SET status = 'Done' WHERE reader_id in (1,2,3,4) and status = 'In Progress';