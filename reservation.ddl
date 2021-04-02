-- Reservation Schema.

-- Constraints not enforced
---- A craft can be any integer length

-- Redundancies that can occur
---- Multiple reservations can occur on the same day

drop schema if exists reservation cascade;
create schema reservation;
set search_path to reservation;

-- Skippers, who each have a sID.
CREATE TABLE Skippers (
    -- The id assigned to the skipper.
    sID integer primary key,
    -- The name of the skipper.
    sName varchar(50) NOT NULL,
    -- The age of the skipper.
    age integer NOT NULL,
    -- The rating of the skipper (from 0-5).
    rating integer NOT NULL,
    -- Constraints
    -- Age is a number greater than 0
    check (age > 0),
    -- Rating is a number between 0 and 5, inclusive
    check (0 <= rating AND rating <= 5)
);

-- Crafts, which each have
CREATE TABLE Crafts (
    -- The id assigned to the craft.
    cID integer primary key,
    -- The name of the craft.
    cName varchar(50) NOT NULL,
    -- The length of the craft (in ft).
    length integer NOT NULL
);

-- A reservation for a craft with a skipper.
CREATE TABLE reservation (
    -- The id assigned to the skipper in the Skippers table.
    skipperId integer references Skippers(sID),
    -- The id assigned to the craft in the Crafts table.
    craftId integer references Crafts(cID),
    -- The day and time of the reservation.
    day timestamp NOT NULL
);
