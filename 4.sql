SELECT COUNT(*) FROM movies WHERE id in (SELECT movie_id FROM ratings where rating = 10)