SELECT AVG(rating) FROM ratings where movie_id in (SELECT id FROM movies WHERE year = '2012');