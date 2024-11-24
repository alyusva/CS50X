-- Lista los títulos y los años de lanzamiento de todas las películas de Harry Potter, en orden cronológico.
SELECT title, year
FROM movies
WHERE title LIKE 'Harry Potter%'
ORDER BY year;
