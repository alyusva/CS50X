-- Lista los títulos de todas las películas con fecha de lanzamiento en o después de 2018, en orden alfabético.
SELECT title
FROM movies
WHERE year >= 2018
ORDER BY title;
