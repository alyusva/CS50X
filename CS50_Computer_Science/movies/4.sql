-- Determina el número de películas con una calificación de IMDb de 10.0.
SELECT COUNT(*)
FROM ratings
WHERE rating = 10.0;
