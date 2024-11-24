-- Lista los nombres de todas las personas que han dirigido una película que recibió una calificación de al menos 9.0.
SELECT DISTINCT name
FROM people
WHERE id IN (
    SELECT person_id
    FROM directors
    WHERE movie_id IN (
        SELECT movie_id
        FROM ratings
        WHERE rating >= 9.0
    )
);
