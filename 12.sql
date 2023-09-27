--A little inspiration from  https://stackoverflow.com/questions/3710483/select-where-count-of-one-field-is-greater-than-one
SELECT title FROM movies
JOIN stars
ON movies.id = stars.movie_id
JOIN people
ON people.id = stars.person_id
WHERE (people.name = 'Jennifer Lawrence' OR people.name = 'Bradley Cooper')
GROUP BY movie_id
HAVING COUNT(movie_id) > 1;