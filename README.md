# LinkedIn App Database
Design and implemention of a database system for a Linkedin-inspired social network.


## Introduction

--------------------------------------------------------------

### Scope of Database
It involves keeping records of a LinkedIn Database. It includes user profiles, recruiters and
the information related to them. For users, we have the records for their Name, Age
(Birthdate), current organisation in the main relation and their related information in other
relations for the functioning of a ​LinkedIn Social Networking App​. The data includes
information about connections, groups, addresses and recommendations etc as well as
app users information like username, password, email etc.


### Descriptions
The database of Linkedin is used to allow registered users to establish and document
networks of people who want to connect with each other professionally. It keeps track of
the people who are working in the industry, their skills etc. This in turn helps the
companies in their hiring process and also people who are looking for jobs according to
their interests. 

Groups of people with similar interest can also be created which in turn can help people
with similar interests to connect with each other and grow together.
The companies can input their requirements into the database and also contact people
who have the skills which they demand. Also people can contact the companies regarding
the same

# Schema
![](https://raw.githubusercontent.com/MukundKal/postgres-linkedin/master/img/schema.PNG)

# ER Diagram
![](https://raw.githubusercontent.com/MukundKal/postgres-linkedin/master/img/final%20schema.jpeg)


-----------------------
> **App Structure**
------------------------


# Front-end structure
--------------------------------------------------------------------------------------------------------------------------------------
## >1.Connection Request
```python
import psycopg2
from texttable import Texttable
import time

try:
    connection=psycopg2.connect(
                            host="POSTGRES_SERVER_IP",
                            port="POSTGRES_P_NUMBER",
                            user="USERNAME",
                            password="PASSWORD",
                            database="DB_NAME"
                            )

except psycopg2.OperationalError as e:
    print('Unable to connect!\n{0}').format(e)
    sys.exit(1)
finally:
#connect to db 
    print("You are connected to database")

```
After the connection is succesfully established, user is presented with *pre-configured queries* that are suitable for out *social network*.


## >2.Console Functional Queries
![](https://raw.githubusercontent.com/MukundKal/postgres-linkedin/master/img/console.PNG)




# Back-end structure
-------------------------------------------------------------------------------------------------------------

## 1>Organising the data and DB

We have to develop our DB with all our tables (the schema) and then populate the tables with data. The former are the *DDL statements* where we describe the tables and the latter is *Data Insert statements* where the actual data is put in. Below is a snipped from the **DDL_Script.txt** for creating table **member**.
```sql
create schema linkedin;

create table member(
first_name varchar(50),
last_name varchar(50),
date_of_birth date,
gender char,
member_id int Primary key,
pswrd varchar(20),
age int,
email varchar(50),
membership_type varchar(50),
card_no int,
city varchar(50),
street_no varchar(50),
pincode int,
house_no varchar(50),
organization_id int,
isRecruiter boolean,
Foreign Key(membership_type) references membership_details(membership_type),
Foreign Key(organization_id) references currently_working_at(organization_id));

```

## 2>Data Entry
Entering data for testing our design was definately time consuming and manwork, a snippet for data addition into a table **connections** from the **Data_insert_statements.txt** is shown below.

```sql

INSERT INTO linkedin.connections VALUES (101, 102, '2010-05-13');
INSERT INTO linkedin.connections VALUES (101, 118, '2001-06-03');
INSERT INTO linkedin.connections VALUES (102, 101, '2010-05-13');
INSERT INTO linkedin.connections VALUES (102, 113, '2001-08-15');
INSERT INTO linkedin.connections VALUES (102, 119, '2001-12-12');
INSERT INTO linkedin.connections VALUES (102, 133, '2013-11-04');
INSERT INTO linkedin.connections VALUES (103, 106, '2013-01-04');
INSERT INTO linkedin.connections VALUES (104, 117, '2003-04-05');
INSERT INTO linkedin.connections VALUES (104, 125, '2001-10-08');
INSERT INTO linkedin.connections VALUES (104, 130, '2005-04-13');
INSERT INTO linkedin.connections VALUES (106, 103, '2013-01-04');
INSERT INTO linkedin.connections VALUES (106, 111, '2010-09-03');
INSERT INTO linkedin.connections VALUES (107, 110, '1999-12-09');

.
.
.
.


INSERT INTO linkedin.currently_working_at VALUES ('amazon', 101, 'software developer', 'mumbai');
INSERT INTO linkedin.currently_working_at VALUES ('google', 102, 'front-end developer', 'delhi');
INSERT INTO linkedin.currently_working_at VALUES ('microsoft', 103, 'back-end developer', 'delhi');
INSERT INTO linkedin.currently_working_at VALUES ('facebook', 104, 'web developer', 'chennai');
INSERT INTO linkedin.currently_working_at VALUES ('oracle', 105, 'front-end developer', 'pune');
INSERT INTO linkedin.currently_working_at VALUES ('uber', 106, 'software developer', 'bangalore');
INSERT INTO linkedin.currently_working_at VALUES ('flipkart', 107, 'business analyst', 'hyderabad');
INSERT INTO linkedin.currently_working_at VALUES ('twitter', 108, 'web developer', 'pune');
INSERT INTO linkedin.currently_working_at VALUES ('deutsche bank', 109, 'business analyst', 'hyderabad');
INSERT INTO linkedin.currently_working_at VALUES ('tesla', 110, 'software developer', 'mumbai');
INSERT INTO linkedin.currently_working_at VALUES ('motorola', 111, 'software developer', 'chennai');


.
.
.
.
.

```

For more information, refer the src **Data_insert_statements.txt**


### Demo SQL Queries to best show app and DB complexity and capability

```sql

--Queries
--1)Find the member who posted the post with the maximum number of likes.	

	 select first_name 
   from members natural join posts 
   where likes=(select max(likes) 
		       from posts);
--2) Find the course name,duration which have courses with more than 1 instructor

 select course_name,course_duration
  from linkedin_learning_courses natural join instructors
  group by course_id
  having count(*)>1  

--3) Find the name of companies which have job openings whose skills match with the skills of member having id 116

	select first_name from ((skills_required  join user_skills
   on (skill_name=skills)) 
   natural join job_openings)
   join members on 
   (members.member_id= job_openings.recruiter_id)
   where user_skills.member_id=116;

--4) Find the names of companies who have job openings of software developer role in Pune.

	select first_name from 
   job_openings join members 
   on (members.member_id= job_openings.recruiter_id)
   where role = 'software developer' 
   and job_openings.city = 'pune';

--5) Find member id and name of the members who have both c++ and java in their skills. 	

	select u1.member_id as mem_id, first_name from 
   (user_skills as u1 join user_skills as u2
    on (u1.member_id=u2.member_id))
    join members on u1.member_id=members.member_id
    where u1.skill_name='c++' 
    and u2.skill_name='java';

--6) Find the name of the members who are part of educational groups

	select first_name from 
   (group_members natural join groups)
   join members
   on (members.member_id=group_members_id)
   where group_category = 'educational';

7) Find the number of VIP members in the database

	select count(membership_type)
   from members
   where membership_type='vip';

--8) Find the list of members who are currently unemployed and have ruby as a skill

	select first_name,last_name
   from members natural join user_skills
   where skill_name ='ruby'
   and working_organization_id is NULL;

--9)Find the members who have the maximum number of connections
	select member1_id,count(member2_id)
from connections 
group by member1_id 
order by count desc limit 1;

--10) Find the members who are currently unemployed and have done courses which have duration more than 90 days

	select distinct first_name,last_name, course_name,age 
   from ((members natural join member_courses)
   natural join linkedin_learning_courses )
   where working_organization_id is NULL
   and course_duration>90;

--11) Find the two most active groups which have liked the most number of posts

	select group_id, sum(likes)  
    from posts join group_members
    on member_id=group_members_id 
    group by group_id 
    order by sum
    desc limit 2;

--12) Find the name of the members who have completed the course soft skills after given date and 

	select first_name, date_completed from 
    (members natural join member_courses)
    natural join linkedin_learning_courses
    where date_completed > '2018-01-01'
    and course_name ='soft skills';

--13) 	Find the details of suitable candidates for the role of web developer offered by different companies by matching their skills
	
	select  distinct member_recommended_id as m1, 
    (select first_name from members where members.member_id=member_recommended_id ),
    (select email from members where members.member_id=member_recommended_id ) from 
    (skills_required natural join job_openings)
    join members on (member_id = recruiter_id)
    natural join skills_recommended
    where experience_required > 1
    and role = 'web developer'
    and first_name='microsoft';

--14) 	Find how popular different skills are among the users
	select skill_name, (count(skill_name)*100.0)/(select count(*) from user_skills) as cntpercent
    from user_skills 
    group by skill_name
    order by (count(skill_name)*100.0)/(select count(*) from user_skills) desc;

--15) Find the company,roles,skills required of the jobs in pune which require experience less than 3
	select first_name,role,skills
    from (job_openings join members 
	  on (members.member_id = job_openings.recruiter_id)
	  natural join skills_required )
	  where job_openings.city = 'bangalore'
	  and experience_required<3;

--16) Find the details of users who have done course of c++ and have got feedback better tha 2 out of 5
	select first_name,certificate_number,member_id,skill_name
    from (member_courses natural join members)
    natural join linkedin_learning_courses
    natural join user_skills
    where skill_provided ='c++'
    and feedback>2
    
```

## Functions 
Functions in postgresql are pretty much like any function implementation and can practically be used to implement any shortcut or functionality. Below are the implementations of functions in the app.

1. **top_skills()** - returns the top skills for a particular member 

2. **trending_posts()** - returns trending posts from the posts table using the following formula:
```python
trpt = r.likes + (r.comments*3) + (r.shares*5)
```

```sql
set search_path to linkedin;

CREATE OR REPLACE FUNCTION top_skills()
RETURNS integer AS $BODY$

DECLARE
skpt integer;
a integer;
r record;
r1 record;

BEGIN
a=1;

for r in select skill_name,count(member_id) as skillpt from user_skills group by skill_name order by skillpt desc

loop

update skill_table set skill_points = r.skillpt where skill_table.skills = r.skill_name;
update skill_table set top_skill_no = a where skill_table.skills = r.skill_name;
a = a+1;
end loop;

RETURN 1;

END;

$BODY$ LANGUAGE plpgsql;

------------------------------------------------------------------------------
set search_path to linkedin;

CREATE OR REPLACE FUNCTION trending_posts()
RETURNS integer AS $BODY$
DECLARE
trpt integer;
trno integer;
likes integer;
comm integer;
shar integer;
a integer;
r record;
BEGIN



for r in select * from posts
loop
--SELECT r.likes into likes FROM posts;
--SELECT r.comments into comm FROM posts;
--SELECT r.shares into shar FROM posts;
trpt = r.likes + (r.comments*3) + (r.shares*5);
update posts set trending_pt = trpt where r.post_id = posts.post_id;

end loop;

a = 1;

for r in select * from posts order by trending_pt desc
loop



update posts set trending_no = a where r.post_id = posts.post_id;
a = a+1;
end loop;

RETURN 1;

END;


$BODY$ LANGUAGE plpgsql;

```

## Triggers
Triggers are basically functions that are automatically executed when a specified event occurs. This can be used in a variety of applications to update a table if a change happens in another table. 

Below are the implemented triggers w/ our linkedin DB:
1. **on_liking_post()**  - this trigger updates the number of likes when a post is liked (automatically).
2. **add_skills()** - this trigger pretty much updates skills when members finish new courses from our linkedin learning courses.

```sql

set search_path to linkedin;

create or replace function on_liking_post()
returns trigger as $body$

declare 
r record;	
a integer;
begin
for r in select * from posts

loop
a = r.likes;
if (tg_op = 'insert') then 
update posts set likes = a+1 where r.post_id = new.post_id ;
end if;
end loop;
return new;
end;
$body$ language plpgsql;

create trigger post_is_liked
after insert or update or delete on likes_post
	for each row execute procedure on_liking_post();


-----------------------------------------------------
 
 
 set search_path to linkedin;

create or replace function add_skills()
returns trigger as $body$

declare 
r record;	
a varchar;
begin

for r in select * from (member_courses natural join linkedin_learning_courses) as new_table

loop
a = r.skill_provided;
if (tg_op = 'insert') then 
update user_skills set skill_name = a where r.member_id = new.member_id ;
end if;
end loop;
return new;
end;
$body$ language plpgsql;

create trigger course_is_completed
after insert or update or delete on member_courses
	for each row execute procedure add_skills();
```
