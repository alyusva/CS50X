-- Determina la calificación promedio de todas las películas lanzadas en 2012.
SELECT AVG(rating)
FROM ratings
JOIN movies ON ratings.movie_id = movies.id
WHERE movies.year = 2012;
