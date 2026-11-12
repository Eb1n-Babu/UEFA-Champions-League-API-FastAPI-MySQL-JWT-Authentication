
INSERT INTO teams (team_name, country, coach)
VALUES
('Real Madrid', 'Spain', 'Carlo Ancelotti'),
('Barcelona', 'Spain', 'Hansi Flick'),
('Manchester City', 'England', 'Pep Guardiola'),
('Liverpool', 'England', 'Arne Slot'),
('Bayern Munich', 'Germany', 'Vincent Kompany'),
('Paris Saint-Germain', 'France', 'Luis Enrique');


INSERT INTO stadiums (stadium_name, city, capacity)
VALUES
('Santiago Bernabeu', 'Madrid', 85000),
('Spotify Camp Nou', 'Barcelona', 99000),
('Etihad Stadium', 'Manchester', 53000),
('Anfield', 'Liverpool', 61000),
('Allianz Arena', 'Munich', 75000),
('Parc des Princes', 'Paris', 48000);



INSERT INTO players
(team_id, player_name, position, jersey_number)
VALUES
(1, 'Kylian Mbappe', 'Forward', 10),
(1, 'Jude Bellingham', 'Midfielder', 5),
(2, 'Lamine Yamal', 'Forward', 10),
(2, 'Pedri', 'Midfielder', 8),
(3, 'Erling Haaland', 'Forward', 9),
(3, 'Phil Foden', 'Midfielder', 47),
(4, 'Mohamed Salah', 'Forward', 11),
(4, 'Virgil van Dijk', 'Defender', 4),
(5, 'Harry Kane', 'Forward', 9),
(6, 'Ousmane Dembele', 'Forward', 10);



INSERT INTO matches
(home_team_id, away_team_id, stadium_id,
 match_date, home_score, away_score)
VALUES
(1, 2, 1, '2026-09-15', 2, 1),
(3, 4, 3, '2026-09-16', 1, 1),
(5, 6, 5, '2026-09-17', 3, 2),
(2, 3, 2, '2026-09-22', 0, 2),
(4, 1, 4, '2026-09-23', 1, 3);


SELECT
    t.team_name,
    COUNT(*) AS played,
    SUM(x.goals_for) AS goals_for,
    SUM(x.goals_against) AS goals_against,
    SUM(x.goals_for - x.goals_against) AS goal_difference,
    SUM(x.points) AS points
FROM (
    SELECT
        home_team_id AS team_id,
        home_score AS goals_for,
        away_score AS goals_against,
        CASE
            WHEN home_score > away_score THEN 3
            WHEN home_score = away_score THEN 1
            ELSE 0
        END AS points
    FROM matches

    UNION ALL

    SELECT
        away_team_id AS team_id,
        away_score AS goals_for,
        home_score AS goals_against,
        CASE
            WHEN away_score > home_score THEN 3
            WHEN away_score = home_score THEN 1
            ELSE 0
        END AS points
    FROM matches
) AS x
JOIN teams t ON t.team_id = x.team_id
GROUP BY t.team_id, t.team_name
ORDER BY points DESC, goal_difference DESC;
