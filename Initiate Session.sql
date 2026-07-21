/* Start Session */

-- Set Line Position to 0 and Status to In Progress for next person in line
UPDATE session
SET 
    queue_position = 0, 
    status = 'In Progress' 
WHERE reader_id in (1, 2, 3, 4) and queue_position = 1;

-- Update the line position for everyone else in queue
UPDATE session SET queue_position = queue_position - 1 where reader_id in (1,2,3,4) and status = 'Waiting';

