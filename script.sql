-- Create a new database called 'nba'
CREATE DATABASE nba;

-- Connect to the 'nba' database
\c nba;

-- Create a table 'games_details' with the schema matching the CSV file
CREATE TABLE games_details (
    game_id BIGINT,
    team_id BIGINT,
    team_abbreviation VARCHAR(10),
    team_city VARCHAR(50),
    player_id BIGINT,
    player_name VARCHAR(100),
    nickname VARCHAR(50),
    start_position VARCHAR(5),
    comment TEXT,
    min VARCHAR(50),
    fgm DECIMAL,
    fga DECIMAL,
    fg_pct DECIMAL,
    fg3m DECIMAL,
    fg3a DECIMAL,
    fg3_pct DECIMAL,
    ftm DECIMAL,
    fta DECIMAL,
    ft_pct DECIMAL,
    oreb DECIMAL,
    dreb DECIMAL,
    reb DECIMAL,
    ast DECIMAL,
    stl DECIMAL,
    blk DECIMAL,
    to_ DECIMAL,
    pf DECIMAL,
    pts DECIMAL,
    plus_minus DECIMAL
);

-- Copy data from 'games_details.csv' into the 'games_details' table
\copy games_details FROM 'games_details.csv' WITH CSV HEADER
