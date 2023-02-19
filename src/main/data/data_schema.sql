DROP TABLE IF EXISTS Politician;
DROP TABLE IF EXISTS City;
DROP TABLE IF EXISTS Office;
DROP TABLE IF EXISTS Issue;
DROP TABLE IF EXISTS Committee;

CREATE TABLE IF NOT EXISTS Politician (
    politician_id int not null primary key,
    name varchar,
    gov_link varchar,
    campaign_link varchar,
    email varchar,
    phone varchar,
    address varchar,
    party varchar,
    date_elected date,
    biography text,
    district varchar
);

CREATE TABLE IF NOT EXISTS City (
    city_id int not null primary key,
    politician_id int not null,
    name varchar,
    state varchar,
    foreign key(politician_id) references Politician(politician_id)
);

CREATE TABLE IF NOT EXISTS Office (
    office_id int not null primary key,
    politician_id int not null,
    name varchar,
    role varchar,
    foreign key(politician_id) references Politician(politician_id)
);

CREATE TABLE IF NOT EXISTS Issue (
    issue_id int not null primary key,
    politician_id int not null,
    name varchar,
    copy varchar,
    foreign key(politician_id) references Politician(politician_id)
);

CREATE TABLE IF NOT EXISTS Committee (
    committee_id int not null primary key,
    politician_id int not null,
    name varchar,
    chair varchar,
    groups_overseen varchar,
    committee_web varchar,
    foreign key(politician_id) references Politician(politician_id)
);