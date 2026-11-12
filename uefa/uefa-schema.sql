
CREATE DATABASE uefa_champions_league;

USE uefa_champions_league;

-- 1. Teams table
CREATE TABLE teams (
    team_id INT PRIMARY KEY AUTO_INCREMENT,
    team_name VARCHAR(100) NOT NULL,
    country VARCHAR(50),
    coach VARCHAR(100)
);

-- 2. Players table
CREATE TABLE players (
    player_id INT PRIMARY KEY AUTO_INCREMENT,
    team_id INT,
    player_name VARCHAR(100) NOT NULL,
    position VARCHAR(30),
    jersey_number INT,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

-- 3. Stadiums table
CREATE TABLE stadiums (
    stadium_id INT PRIMARY KEY AUTO_INCREMENT,
    stadium_name VARCHAR(100),
    city VARCHAR(100),
    capacity INT
);

-- 4. Matches table
CREATE TABLE matches (
    match_id INT PRIMARY KEY AUTO_INCREMENT,
    home_team_id INT,
    away_team_id INT,
    stadium_id INT,
    match_date DATE,
    home_score INT DEFAULT 0,
    away_score INT DEFAULT 0,
    FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (stadium_id) REFERENCES stadiums(stadium_id)
);
