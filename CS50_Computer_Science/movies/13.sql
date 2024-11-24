-- Lista los nombres de todas las personas que actuaron en una película en la que también actuó Kevin Bacon.
SELECT DISTINCT name
FROM people
WHERE id IN (
    SELECT person_id
    FROM stars
    WHERE movie_id IN (
        SELECT movie_id
        FROM stars
        WHERE person_id = (
            SELECT id
            FROM people
            WHERE name = 'Kevin Bacon' AND birth = 1958
        )
    )
) AND name != 'Kevin Bacon';
