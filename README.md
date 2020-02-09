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
![](https://github.com/MukundKal/postgres-linkedin/blob/master/img/schema.PNG)

# ER Diagram
![](https://raw.githubusercontent.com/MukundKal/postgres-linkedin/master/img/final%20schema.jpeg)



## Console 


1.==Connection Request==
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

*Console Functional Queries*
![]()