create database test;
use test;
select test;
-- 제약조건 없는 user1 테이블 생성성
-- CHAR: 글자수만큼 storage 미리 할당
-- VCHAR: 필요한 만큼만 storage 할당
-- TEXT: 큰 문자열 저장
create table user1(
    user_id INT, 
    name Varchar(20),
    email Varchar(30),
    age INT(3),
    rdate DATE
    );

-- 제약조건 있는 user2 테이블 생성
create table user2(
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL,
    email VARCHAR(30) UNIQUE NOT NULL,
    age INT(3) DEFAULT '30',
    rdate TIMESTAMP
    );
-- ALTER
-- 문자열 인코딩 변경
-- 현재 문자열 인코딩 확인
show variables like "character_set_database";

-- test 데이터 베이스의 문자열 인코딩을 utf8로 변경
ALTER DATABASE test CHARACTER SET = utf8;

-- 문자열 인코딩 변경 결과 확인
show variables like "character_set_database";

-- ADD: tmp column (data type: text)
ALTER TABLE user2 ADD tmp TEXT;

-- MODIFY
ALTER TABLE user2 MODIFY COLUMN tmp INT(3);

-- DROP
ALTER TABLE user2 DROP tmp;

CREATE DATABASE tmp;
USE tmp;
CREATE TABLE tmp(id INT);
DROP TABLE tmp;
SHOW DATABASES;
DROP DATABASE tmp;

-- INSERT
CREATE TABLE user (
    user_id int(11) UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(30) DEFAULT NULL,
    PRIMARY KEY(user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE addr (
    id int(11) unsigned NOT NULL AUTO_INCREMENT,
    addr VARCHAR(30) DEFAULT NULL,
    user_id int(11) DEFAULT NULL,
    PRIMARY KEY(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO user(name)
VALUES("jin"), ("po"), ("alice"), ("petter");

INSERT INTO addr(addr, user_id)
VALUES ("seoul", 1), ("pusan", 2), ("deajeon", 3), 
("deagu", 5), ("seoul", 6);

-- 그냥 조인 -> M * N
select id, user.name, addr.addr
from user
join addr;

-- INNER JOIN: 공통키값 row만 출력
select id, user.name, addr.addr
from user
join addr
on user.user_id = addr.user_id;

-- LEFT JOIN
-- FROM 기준 좌우, 좌를 살림
SELECT id, user.name, addr.addr
FROM user
LEFT JOIN addr
ON user.user_id = addr.user_id;

-- RIGHT JOIN
-- FROM 기준 좌우, 우를 살림
SELECT id, user.name, addr.addr
FROM user
RIGHT JOIN addr
ON user.user_id = addr.user_id;

-- UNION
-- column 중복제거하고 위아래로 합치기
select name
from user
union 
select addr
from addr;

-- UNION ALL
-- 중복 제거안함
select name, user_id
from user
UNION ALL
select addr, user_id
from addr;

-- FULL OUTER JOIN
select id, user.name, addr.addr
from user
left join addr
on user.user_id = addr.user_id
UNION
select id, user.name, addr.addr
from user
right join addr
on user.user_id = addr.user_id;

-- sub_query
-- 전체 나라수, 도시수, 언어수 출력
use world;
select
    (select count(name) From city) as total_city,
    (select count(name) From country) as total_country ,
    (select count(DISTINCT(language)) From countrylanguage) as total_language 
from dual;

-- 800만 이상 도시 국가코드, 이름, 도시인구수 출력
select *
from 
    (select countrycode, name, population 
    from city
    where population > 8000000) as city
join
    (select code, name
    from country) as country
on city.CountryCode = country.code;

select code, name, headofstate
from country
where code in(
    select DISTINCT(countrycode) from city where population > 8000000
    );
