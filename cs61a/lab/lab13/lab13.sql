.read data.sql


CREATE TABLE bluedog AS
  SELECT color, pet FROM students WHERE color = 'blue' AND pet = 'dog';

CREATE TABLE bluedog_songs AS
  SELECT color, pet, song FROM students WHERE color = 'blue' AND pet = 'dog';


-- Group by organizes the projected tables into groups, the groups have a count, but typically what is displayed is some row from that group, in which only the group in which the expression evaluates to true is shown

CREATE TABLE smallest_int_having AS
  SELECT time, smallest FROM students GROUP BY smallest HAVING count(smallest) = 1;


CREATE TABLE matchmaker AS
  SELECT a.pet, a.song, a.color, b.color FROM students AS a, students AS b WHERE a.pet = b.pet AND a.song = b.song AND a.time <> b.time;


CREATE TABLE sevens AS
  SELECT seven FROM students as a, numbers as b WHERE number = 7 AND b."7" = "True" AND a.time = b.time LIMIT 10;


CREATE TABLE avg_difference AS
  SELECT round(avg(abs(number-smallest)))  FROM students;

