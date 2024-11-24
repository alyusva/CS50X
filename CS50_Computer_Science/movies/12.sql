-- Lista los títulos de todas las películas en las que actuaron tanto Bradley Cooper como Jennifer Lawrence.
SELECT title
FROM movies
WHERE id IN (
    SELECT movie_id
    FROM stars
    WHERE person_id = (
        SELECT id
        FROM people
        WHERE name = 'Bradley Cooper'
    )
) AND id IN (
    SELECT movie_id
    FROM stars
    WHERE person_id = (
        SELECT id
        FROM people
        WHERE name = 'Jennifer Lawrence'
    )
);
