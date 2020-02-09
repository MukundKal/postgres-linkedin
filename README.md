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
