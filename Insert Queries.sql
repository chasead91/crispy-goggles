INSERT INTO reader (name, bio, offering, location) 
    VALUES 
        ('Taralynn','A beautiful soul','Creative Mirroring','Room 4'),
        ('Jack','The Mayor','Energy Work','Room 3');

INSERT INTO sitter (name)
    VALUES 
    ('A. Nell Sechs'),
    ('A.S. Muncher'),
    ('Amanda DP Throat'),
    ('Amanda Hump'),
    ('Craven Moorehead'),
    ('Dick Raasch'),
    ('E. Norma Stits'),
    ('Eaton Beaver');

INSERT INTO session (reader_id, sitter_id, queue_position, status)
    VALUES
    (1,1,1,'Waiting'),
    (1,2,2,'Waiting'),
    (1,3,3,'Waiting'),
    (2,4,1,'Waiting'),
    (2,5,2,'Waiting'),
    (2,6,3,'Waiting'),
    (3,7,1,'Waiting'),
    (3,8,2,'Waiting'),
    (3,9,3,'Waiting'),
    (4,10,1,'Waiting'),
    (4,11,2,'Waiting');