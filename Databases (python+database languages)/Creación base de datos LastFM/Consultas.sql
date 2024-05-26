-- 1. Obtener el número total de usuarios distintos que han escuchado a Led Zeppelin.
SELECT COUNT(indice)
FROM escuchas as e
INNER JOIN artistas as a on a.internartid = e.internartid
WHERE a.artname = 'Led Zeppelin';

-- RESPUESTA: 456

-- 2. Obtener el número total de mujeres que han escuchado a Madonna.
SELECT COUNT(u.internuserid)
FROM usuarios as u 
INNER JOIN escuchas as e on e.internuserid = u.internuserid
INNER JOIN artistas as a on a.internartid = e.interntraid
WHERE u.gender = 'f' AND a.artname = 'Madonna'; -- No hay escuchas de mujeres de madonna? 

-- RESPUESTA: 0 

-- 3. Obtener el número total de usuarios que o bien son de España (Spain) o bien han escuchado a ’Red Hot Chili Peppers’.
SELECT COUNT(u.internuserid)
FROM usuarios as u 
INNER JOIN paises as p ON p.interncountryid = u.interncountryid
INNER JOIN escuchas as e ON e.internuserid = u.internuserid
INNER JOIN artistas as a ON a.internartid = e.internartid
WHERE p.country = 'Spain' OR a.artname = 'Red Hot Chili Peppers';

-- RESPUESTA: 2032

-- 4. Obtener la media del total de escuchas de los usuarios (de media un usuario hace tantas escuchas) 
SELECT AVG(conteo)
FROM (SELECT internuserid, COUNT(indice) as conteo -- sacamos las escuchas de cada usuario y hacemos la media 
FROM escuchas
GROUP BY internuserid) as sbq;

-- RESPUESTA: '18518.5185'

 -- 5. Obtener los usuarios cuyo número total de escuchas superan a la media del total de escuchas de los usuarios. 
SELECT *
FROM (SELECT internuserid, COUNT(indice) as conteo -- sacamos las escuchas de cada usuario y hacemos la media 
FROM escuchas
GROUP BY internuserid) as sbq1
WHERE conteo > (SELECT AVG(conteo)
FROM (SELECT internuserid, COUNT(indice) as conteo -- sacamos las escuchas de cada usuario y hacemos la media 
FROM escuchas
GROUP BY internuserid) as sbq2);

-- Respuesta: '2', '53429'
/*
'6', '20044'
'8', '35471'
'12', '67389'
'16', '20077'
'17', '18630'
'19', '25801'
'21', '65139'
'22', '41510'
'23', '40136'
'25', '35022'
'26', '38973'
'29', '34651'
'31', '33431'
'33', '66481'
'52', '29661'
'54', '33244'
*/

-- 6. Número total de escuchas por país.
SELECT p.country, COUNT(e.indice)
FROM escuchas AS e
INNER JOIN usuarios as u ON u.internuserid = e.internuserid
INNER JOIN paises as p ON p.interncountryid = u.interncountryid
GROUP BY p.country;

-- RESPUESTA 
 /* 
 NULL, '33796'
'Australia', '6732'
'Brazil', '61193'
'Bulgaria', '15400'
'Canada', '65139'
'Chile', '732'
'Cote D\'Ivoire', '12666'
'Croatia', '6570'
'Finland', '14095'
'Germany', '71082'
'Greece', '4208'
'Italy', '26124'
'Japan', '11950'
'Mexico', '29748'
'Morocco', '18630'
'Peru', '53429'
'Poland', '70394'
'Romania', '8127'
'Russian Federation', '63172'
'Slovakia', '35471'
'Sweden', '46072'
'Turkey', '38973'
'United Kingdom', '110033'
'United States', '196264'
*/

--  7. Obtener las 15 canciones que tienen un mayor número de escuchas de usuarios distintos (muestra el nombre de la canción y el número de usuarios distintos que la han escuchado).
SELECT c.traname, COUNT(DISTINCT u.internuserid) as conteo
FROM canciones as c
INNER JOIN escuchas as e on e.interntraid = c.interntraid 
INNER JOIN usuarios as u ON u.internuserid = e.internuserid
GROUP BY c.traname 
ORDER BY conteo DESC
LIMIT 15;

-- RESPUESTA 
/*
'Intro', '48'
'Breathe', '34'
'Angel', '32'
'All I Need', '32'
'One', '32'
'[Untitled]', '32'
'Lullaby', '31'
'Home', '31'
'Rain', '29'
'I Want You', '29'
'Wake Up', '29'
'Run', '29'
'Interlude', '29'
'Silence', '28'
'Crazy', '28'
*/


-- 8. Obtener el porcentaje de escuchas del total que han realizado los usuarios cuya edad supera la media de edad de todos los usuarios. Para esta consulta, ignora a aquellos usuarios cuya edad es 0 o nula.

SELECT internuserid, 100*conteo/(SELECT SUM(conteo)
								FROM(SELECT internuserid, conteo
FROM (SELECT u.internuserid, COUNT(e.indice) as conteo
FROM usuarios AS u 
INNER JOIN escuchas as e ON e.internuserid = u.internuserid
WHERE u.age > (SELECT AVG(age) 
				FROM usuarios) AND u.age IS NOT NULL
GROUP BY u.internuserid) as sbq) as sb2)
FROM (SELECT internuserid, conteo
FROM (SELECT u.internuserid, COUNT(e.indice) as conteo
FROM usuarios AS u 
INNER JOIN escuchas as e ON e.internuserid = u.internuserid
WHERE u.age > (SELECT AVG(age) 
				FROM usuarios) AND u.age IS NOT NULL
GROUP BY u.internuserid) as sbq) as sb1

-- RESPUESTA 
/*
'12', '20.2185'
'19', '7.7410'
'20', '1.3015'
'21', '19.5434'
'22', '12.4541'
'31', '10.0302'
'34', '5.4041'
'38', '4.0405'
'41', '3.3153'
'43', '2.3327'
'45', '0.2196'
'48', '0.1791'
'53', '3.2460'
'54', '9.9741'
*/

