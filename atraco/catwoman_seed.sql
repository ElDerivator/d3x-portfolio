-- ========================================================================
-- Gotham Heist DB  ·  lab Catwoman SQL  ·  100% sintetico, random.seed(2026)
-- Reskin de labs/googlesql_f1 (dominio consultoria/PM) a SQLite estandar.
-- ========================================================================

DROP TABLE IF EXISTS gear;
DROP TABLE IF EXISTS shifts;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS crew;
DROP TABLE IF EXISTS heists;
DROP TABLE IF EXISTS patrons;

-- patrons: los compradores en las sombras que encargan un golpe (antes: clients).
CREATE TABLE patrons (
    patron_id      INTEGER PRIMARY KEY,
    alias          TEXT NOT NULL,
    specialty      TEXT NOT NULL,   -- jewels / art / tech / antiquities / information
    city           TEXT NOT NULL,
    first_contact  TEXT NOT NULL    -- fecha YYYY-MM-DD
);

-- heists: cada golpe pertenece a un patron (antes: projects).
CREATE TABLE heists (
    heist_id       INTEGER PRIMARY KEY,
    patron_id      INTEGER NOT NULL REFERENCES patrons(patron_id),
    codename       TEXT NOT NULL,
    target_type    TEXT NOT NULL,   -- museum / gala / penthouse / bank / rooftop
    start_date     TEXT NOT NULL,
    end_date       TEXT,            -- NULL = sigue abierto
    status         TEXT NOT NULL,   -- planning / active / pulled_off / busted
    take_estimate  REAL NOT NULL    -- botin estimado en USD (antes: budget)
);

-- crew: la banda de Selina (antes: consultants).
CREATE TABLE crew (
    crew_id        INTEGER PRIMARY KEY,
    alias          TEXT NOT NULL,
    specialty_role TEXT NOT NULL,   -- acrobat / hacker / driver / grifter / safecracker / lookout
    rank           TEXT NOT NULL,   -- rookie / pro / veteran / legend
    cut_rate       REAL NOT NULL,   -- su tajada por hora, USD (antes: hourly_rate)
    joined         TEXT NOT NULL
);

-- jobs: las tareas dentro de un golpe (antes: tasks).
CREATE TABLE jobs (
    job_id         INTEGER PRIMARY KEY,
    heist_id       INTEGER NOT NULL REFERENCES heists(heist_id),
    job_name       TEXT NOT NULL,
    job_type       TEXT NOT NULL,   -- casing / alarms / vault / forgery / getaway
    planned_hours  REAL NOT NULL
);

-- shifts: horas que cada miembro mete en un job (antes: timesheets).
CREATE TABLE shifts (
    shift_id       INTEGER PRIMARY KEY,
    job_id         INTEGER NOT NULL REFERENCES jobs(job_id),
    crew_id        INTEGER NOT NULL REFERENCES crew(crew_id),
    work_date      TEXT NOT NULL,
    hours          REAL NOT NULL,
    on_the_books   INTEGER NOT NULL -- 1 = cuenta para el reparto oficial, 0 = fuera de libros
);

-- gear: gastos no-laborales del golpe (antes: costs).
CREATE TABLE gear (
    gear_id        INTEGER PRIMARY KEY,
    heist_id       INTEGER NOT NULL REFERENCES heists(heist_id),
    gear_type      TEXT NOT NULL,   -- tools / vehicle / bribe / disguise
    cost           REAL NOT NULL,
    acquired       TEXT NOT NULL
);


-- patrons: 6 filas
INSERT INTO patrons (patron_id, alias, specialty, city, first_contact) VALUES (1, 'The Broker', 'information', 'Gotham', '2023-01-10');
INSERT INTO patrons (patron_id, alias, specialty, city, first_contact) VALUES (2, 'Madame Noir', 'art', 'Gotham', '2023-03-22');
INSERT INTO patrons (patron_id, alias, specialty, city, first_contact) VALUES (3, 'Mr. Wren', 'jewels', 'Bludhaven', '2022-11-05');
INSERT INTO patrons (patron_id, alias, specialty, city, first_contact) VALUES (4, 'The Penguin', 'antiquities', 'Gotham', '2021-07-19');
INSERT INTO patrons (patron_id, alias, specialty, city, first_contact) VALUES (5, 'Lady Vale', 'jewels', 'Metropolis', '2024-02-14');
INSERT INTO patrons (patron_id, alias, specialty, city, first_contact) VALUES (6, 'The Collector', 'tech', 'Gotham', '2023-09-30');

-- crew: 12 filas
INSERT INTO crew (crew_id, alias, specialty_role, rank, cut_rate, joined) VALUES (1, 'Selina Kyle', 'acrobat', 'legend', 500, '2019-05-01');
INSERT INTO crew (crew_id, alias, specialty_role, rank, cut_rate, joined) VALUES (2, 'Whiskers', 'hacker', 'veteran', 320, '2020-02-11');
INSERT INTO crew (crew_id, alias, specialty_role, rank, cut_rate, joined) VALUES (3, 'Midnight', 'driver', 'pro', 240, '2021-06-03');
INSERT INTO crew (crew_id, alias, specialty_role, rank, cut_rate, joined) VALUES (4, 'Velvet', 'grifter', 'veteran', 300, '2020-09-17');
INSERT INTO crew (crew_id, alias, specialty_role, rank, cut_rate, joined) VALUES (5, 'Jinx', 'safecracker', 'legend', 450, '2019-08-22');
INSERT INTO crew (crew_id, alias, specialty_role, rank, cut_rate, joined) VALUES (6, 'Shadow', 'lookout', 'pro', 180, '2022-01-30');
INSERT INTO crew (crew_id, alias, specialty_role, rank, cut_rate, joined) VALUES (7, 'Patch', 'hacker', 'rookie', 150, '2024-03-12');
INSERT INTO crew (crew_id, alias, specialty_role, rank, cut_rate, joined) VALUES (8, 'Sable', 'acrobat', 'pro', 260, '2022-07-08');
INSERT INTO crew (crew_id, alias, specialty_role, rank, cut_rate, joined) VALUES (9, 'Dash', 'driver', 'veteran', 280, '2020-11-25');
INSERT INTO crew (crew_id, alias, specialty_role, rank, cut_rate, joined) VALUES (10, 'Pearl', 'grifter', 'rookie', 140, '2024-05-19');
INSERT INTO crew (crew_id, alias, specialty_role, rank, cut_rate, joined) VALUES (11, 'Cosmo', 'safecracker', 'pro', 300, '2021-10-14');
INSERT INTO crew (crew_id, alias, specialty_role, rank, cut_rate, joined) VALUES (12, 'Raven', 'lookout', 'veteran', 200, '2021-03-06');

-- heists: 10 filas
INSERT INTO heists (heist_id, patron_id, codename, target_type, start_date, end_date, status, take_estimate) VALUES (1, 2, 'Velvet Claw', 'museum', '2024-01-15', '2024-02-20', 'pulled_off', 2800000);
INSERT INTO heists (heist_id, patron_id, codename, target_type, start_date, end_date, status, take_estimate) VALUES (2, 3, 'Nine Lives', 'gala', '2024-03-01', '2024-03-05', 'pulled_off', 950000);
INSERT INTO heists (heist_id, patron_id, codename, target_type, start_date, end_date, status, take_estimate) VALUES (3, 1, 'Glass Rooftop', 'penthouse', '2024-04-10', NULL, 'active', 1200000);
INSERT INTO heists (heist_id, patron_id, codename, target_type, start_date, end_date, status, take_estimate) VALUES (4, 4, 'Midnight Vault', 'bank', '2024-02-28', '2024-04-01', 'busted', 4000000);
INSERT INTO heists (heist_id, patron_id, codename, target_type, start_date, end_date, status, take_estimate) VALUES (5, 5, 'Diamond District', 'gala', '2024-05-02', NULL, 'active', 1750000);
INSERT INTO heists (heist_id, patron_id, codename, target_type, start_date, end_date, status, take_estimate) VALUES (6, 2, 'Silent Gallery', 'museum', '2023-11-20', '2023-12-15', 'pulled_off', 2100000);
INSERT INTO heists (heist_id, patron_id, codename, target_type, start_date, end_date, status, take_estimate) VALUES (7, 3, 'Copper Wren', 'penthouse', '2024-06-01', NULL, 'planning', 680000);
INSERT INTO heists (heist_id, patron_id, codename, target_type, start_date, end_date, status, take_estimate) VALUES (8, 6, 'Server Farm', 'bank', '2024-05-20', NULL, 'active', 3200000);
INSERT INTO heists (heist_id, patron_id, codename, target_type, start_date, end_date, status, take_estimate) VALUES (9, 4, 'The Aviary', 'museum', '2023-09-01', '2023-10-10', 'pulled_off', 1500000);
INSERT INTO heists (heist_id, patron_id, codename, target_type, start_date, end_date, status, take_estimate) VALUES (10, 5, 'Catwalk', 'rooftop', '2024-06-15', NULL, 'planning', 520000);

-- jobs: 28 filas
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (1, 1, 'Case the east wing', 'casing', 20);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (2, 1, 'Loop the cameras', 'alarms', 14);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (3, 1, 'Lift the canvas', 'vault', 10);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (4, 1, 'Clean exit', 'getaway', 6);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (5, 2, 'Guest list recon', 'casing', 12);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (6, 2, 'Swap the necklace', 'forgery', 8);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (7, 2, 'Slip out', 'getaway', 4);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (8, 3, 'Blueprint pull', 'casing', 16);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (9, 3, 'Kill the sensors', 'alarms', 18);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (10, 3, 'Crack the safe', 'vault', 12);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (11, 4, 'Floor plans', 'casing', 22);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (12, 4, 'Jam the alarms', 'alarms', 20);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (13, 4, 'Drill the vault', 'vault', 30);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (14, 4, 'Driver on standby', 'getaway', 8);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (15, 5, 'Scout the venue', 'casing', 14);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (16, 5, 'Forge invites', 'forgery', 10);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (17, 5, 'Grab the stones', 'vault', 9);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (18, 6, 'Night recon', 'casing', 18);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (19, 6, 'Disable grid', 'alarms', 12);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (20, 6, 'Take the sculpture', 'vault', 8);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (21, 7, 'Study the mark', 'casing', 10);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (22, 7, 'Plan the climb', 'casing', 6);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (23, 8, 'Map the network', 'casing', 20);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (24, 8, 'Breach the firewall', 'alarms', 24);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (25, 8, 'Clone the drives', 'vault', 16);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (26, 9, 'Case the atrium', 'casing', 15);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (27, 9, 'Loop feeds', 'alarms', 10);
INSERT INTO jobs (job_id, heist_id, job_name, job_type, planned_hours) VALUES (28, 9, 'Lift the relic', 'vault', 7);

-- shifts: 126 filas
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (1, 1, 1, '2024-02-04', 8, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (2, 1, 1, '2024-02-03', 5.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (3, 1, 1, '2024-02-01', 8.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (4, 2, 12, '2024-01-17', 2, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (5, 2, 12, '2024-01-29', 2.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (6, 2, 12, '2024-01-21', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (7, 2, 2, '2024-01-27', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (8, 2, 2, '2024-01-17', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (9, 2, 7, '2024-02-04', 6, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (10, 3, 1, '2024-02-02', 5.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (11, 3, 1, '2024-01-28', 5.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (12, 3, 5, '2024-01-23', 8.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (13, 3, 5, '2024-01-30', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (14, 3, 5, '2024-01-19', 8, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (15, 3, 11, '2024-01-18', 6.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (16, 3, 11, '2024-01-30', 3, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (17, 3, 11, '2024-01-29', 6.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (18, 4, 9, '2024-02-04', 5.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (19, 4, 9, '2024-01-27', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (20, 4, 9, '2024-01-23', 2, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (21, 4, 3, '2024-01-29', 8.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (22, 4, 3, '2024-01-21', 4.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (23, 4, 3, '2024-01-30', 8.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (24, 5, 1, '2024-03-15', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (25, 6, 10, '2024-03-16', 2, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (26, 6, 10, '2024-03-12', 2, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (27, 6, 10, '2024-03-14', 3.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (28, 7, 3, '2024-03-19', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (29, 7, 3, '2024-03-07', 3, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (30, 8, 1, '2024-04-28', 5.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (31, 8, 1, '2024-04-14', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (32, 8, 1, '2024-04-14', 5, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (33, 8, 12, '2024-04-15', 3, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (34, 8, 12, '2024-04-22', 8, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (35, 8, 12, '2024-04-16', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (36, 8, 4, '2024-04-12', 2, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (37, 8, 4, '2024-04-10', 2.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (38, 9, 12, '2024-04-25', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (39, 9, 6, '2024-04-16', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (40, 9, 6, '2024-04-17', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (41, 9, 6, '2024-04-11', 3, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (42, 10, 1, '2024-04-10', 3, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (43, 10, 1, '2024-04-26', 3, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (44, 10, 5, '2024-04-22', 4.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (45, 10, 11, '2024-04-22', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (46, 11, 8, '2024-03-08', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (47, 11, 8, '2024-03-14', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (48, 11, 12, '2024-03-07', 8, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (49, 11, 12, '2024-03-06', 2, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (50, 11, 12, '2024-03-19', 4.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (51, 12, 6, '2024-03-10', 5, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (52, 12, 2, '2024-03-07', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (53, 12, 2, '2024-03-17', 4, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (54, 12, 2, '2024-03-07', 2.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (55, 12, 12, '2024-02-29', 8, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (56, 12, 12, '2024-03-04', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (57, 12, 12, '2024-03-07', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (58, 13, 1, '2024-03-12', 8, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (59, 13, 11, '2024-02-29', 2, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (60, 14, 3, '2024-03-16', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (61, 14, 3, '2024-03-13', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (62, 14, 3, '2024-03-09', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (63, 15, 12, '2024-05-13', 8, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (64, 15, 12, '2024-05-13', 2.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (65, 15, 12, '2024-05-11', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (66, 15, 1, '2024-05-11', 8.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (67, 16, 7, '2024-05-19', 2, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (68, 17, 1, '2024-05-06', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (69, 18, 6, '2023-11-24', 4.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (70, 18, 6, '2023-11-27', 8.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (71, 18, 6, '2023-11-24', 3, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (72, 18, 1, '2023-12-07', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (73, 18, 1, '2023-11-27', 2, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (74, 18, 1, '2023-12-05', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (75, 18, 8, '2023-12-10', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (76, 19, 2, '2023-12-10', 5, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (77, 19, 2, '2023-11-20', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (78, 19, 7, '2023-12-06', 8, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (79, 19, 6, '2023-12-01', 8, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (80, 19, 6, '2023-11-28', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (81, 20, 11, '2023-12-08', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (82, 20, 11, '2023-12-03', 3.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (83, 20, 11, '2023-12-01', 8.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (84, 20, 8, '2023-11-25', 2, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (85, 20, 8, '2023-11-28', 3, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (86, 20, 8, '2023-11-20', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (87, 21, 10, '2024-06-13', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (88, 21, 10, '2024-06-04', 2, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (89, 21, 6, '2024-06-18', 4, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (90, 21, 6, '2024-06-19', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (91, 21, 1, '2024-06-10', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (92, 21, 1, '2024-06-13', 3, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (93, 22, 8, '2024-06-06', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (94, 22, 8, '2024-06-18', 3, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (95, 22, 8, '2024-06-04', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (96, 22, 12, '2024-06-12', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (97, 22, 6, '2024-06-20', 3, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (98, 22, 6, '2024-06-11', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (99, 22, 6, '2024-06-03', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (100, 23, 1, '2024-05-23', 5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (101, 23, 1, '2024-06-03', 5, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (102, 23, 6, '2024-06-04', 8, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (103, 23, 8, '2024-05-27', 3, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (104, 23, 8, '2024-06-06', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (105, 23, 8, '2024-06-04', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (106, 24, 6, '2024-05-31', 4.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (107, 24, 6, '2024-06-03', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (108, 24, 7, '2024-05-23', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (109, 24, 7, '2024-06-03', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (110, 25, 5, '2024-05-23', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (111, 25, 5, '2024-06-09', 4.5, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (112, 25, 5, '2024-05-30', 6.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (113, 25, 11, '2024-06-04', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (114, 25, 11, '2024-06-09', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (115, 25, 11, '2024-05-25', 2, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (116, 26, 4, '2023-09-14', 8.5, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (117, 26, 4, '2023-09-16', 4, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (118, 26, 4, '2023-09-08', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (119, 26, 6, '2023-09-11', 2, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (120, 26, 6, '2023-09-17', 4, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (121, 27, 6, '2023-09-05', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (122, 27, 7, '2023-09-20', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (123, 27, 2, '2023-09-19', 4, 0);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (124, 28, 11, '2023-09-18', 6, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (125, 28, 1, '2023-09-11', 4, 1);
INSERT INTO shifts (shift_id, job_id, crew_id, work_date, hours, on_the_books) VALUES (126, 28, 1, '2023-09-16', 4.5, 1);

-- gear: 17 filas
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (1, 1, 'tools', 10978.53, '2024-01-14');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (2, 1, 'tools', 9414.52, '2024-01-21');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (3, 2, 'disguise', 4192.4, '2024-03-04');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (4, 2, 'disguise', 4824.41, '2024-02-26');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (5, 3, 'tools', 11768.55, '2024-04-14');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (6, 3, 'disguise', 6698.46, '2024-04-15');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (7, 4, 'bribe', 55706.79, '2024-03-05');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (8, 4, 'vehicle', 17342.04, '2024-02-28');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (9, 5, 'disguise', 6783.25, '2024-05-03');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (10, 5, 'tools', 9252.57, '2024-05-03');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (11, 6, 'vehicle', 30410.44, '2023-11-23');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (12, 6, 'disguise', 3820.27, '2023-11-25');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (13, 8, 'disguise', 6196.22, '2024-05-21');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (14, 8, 'vehicle', 33203.17, '2024-05-19');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (15, 9, 'vehicle', 18937.7, '2023-08-28');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (16, 9, 'tools', 7491.52, '2023-09-05');
INSERT INTO gear (gear_id, heist_id, gear_type, cost, acquired) VALUES (17, 9, 'vehicle', 19175.66, '2023-09-07');

-- totales: patrons=6 crew=12 heists=10 jobs=28 shifts=126 gear=17
