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



#Cursor
cursor=connection.cursor()


#query execute
cursor.execute("set search_path to <DB_NAME>")



#-----------------------------------------------------------------

def q1():
    cursor.execute(" SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema' AND schemaname= 'linkedin' ")
    records =  cursor.fetchall()
    x=[]
    for r in records:
        x.append(r)

    t = Texttable()
    t.add_rows(x,header=False)
    print(t.draw())

def q2():
    print('Popular Posts from a particular Year: \n')
    date = input("Please enter Year: ")
    print(date)
    orderby = input("Please enter order of likes(ASC/DESC): ")
    print(orderby)
    limit = int(input('Number of Results Required: '))
    cursor.execute(" select first_name, likes from posts natural join members where extract(year from date_posted) \
                        = '{}' order by likes {} Limit {}".format(date,orderby, limit))
    records =  cursor.fetchall()
    x=[]
    x.append(['firat_name', 'likes'])
    for r in records:
        x.append(r)

    t = Texttable()
    t.add_rows(x,header=True)
    print(t.draw())

def q3():
    print('GEOGRAPHIC JOB SEARCH: \n')
    city = input("Please enter City: ")
    print(city)
    role = input("Please enter Role(software developer/ web developer/ etc): ")
    print(role)
    experience_required =  input("Please enter least experience (in #YEARS): ")
    cursor.execute("select first_name, email from job_openings join members on (members.member_id= job_openings.recruiter_id) \
                        where role = '{}' and job_openings.city = '{}' and experience_required = {}".format(role,city,experience_required) )   
    records =  cursor.fetchall()
    x=[]
    x.append(['Recruitor Name', 'Contact Email'])
    for r in records:
        x.append(r)

    t = Texttable()
    t.add_rows(x,header=True)
    print(t.draw())



def q4():
    print('MEMBER SEARCH: Search for other members with required skills: \n')
    n = int(input("Please enter number of skills to match (1 or 2): "))

    if n==1:
        skillname = input("Please enter skill name: ")
        cursor.execute("select distinct u1.member_id as mem_id, first_name from             \
                        (user_skills as u1 join user_skills as u2                  \
                         on (u1.member_id=u2.member_id))                           \
                         join members on u1.member_id=members.member_id            \
                        where u1.skill_name='{}' ".format(skillname))
        print('Searching for skill: '+ skillname)
    elif n==2:
        skillname1 = input("Please enter skill name 1: ")
        skillname2 = input("Please enter skill name 2: ")
        cursor.execute("select distinct u1.member_id as mem_id, first_name from             \
                        (user_skills as u1 join user_skills as u2                  \
                         on (u1.member_id=u2.member_id))                           \
                         join members on u1.member_id=members.member_id            \
                        where u1.skill_name='{}' and u2.skill_name='{}' ".format(skillname1,skillname2))
    
        print('Searching for skill: '+skillname1 +' and '+ skillname2)
        time.sleep(1)

    
    records =  cursor.fetchall()
    x=[]
    x.append(['Member ID', 'Name'])
    for r in records:
        x.append(r)

    t = Texttable()
    t.add_rows(x,header=True)
    print(t.draw())





def q5():
    print('SIMILAR MEMBERS Search: Find other members with your interest category/genre group: \n')
    cat = input("Please enter Group Category/Genre (educational / coding / science / sports etc) : ")
    print('Seaching for Category: ' + cat )
    cursor.execute("select first_name from (group_members natural join groups)   \
                      join members on (members.member_id=group_members_id)         \
                      where group_category = '{}';".format(cat) )   
    records =  cursor.fetchall()
    x=[]
    x.append(['Group Name'])
    for r in records:
        x.append(r)

    t = Texttable()
    t.add_rows(x,header=True)
    print(t.draw())
    return

def q6():
    print('MEMBERSHIPS and their PERCENTAGES: \n')
    memtype = input("Please enter Membership type (Normal / VIP / Premium) : ")
    
    cursor.execute("select count(membership_type)  ,  ( count(membership_type) * 100.00 / ( select count(*) from members )   ) as score                               \
                      from members                                                                                                                     \
                      where membership_type= '{}';".format(memtype) )   
    records =  cursor.fetchall()
    x=[]
    x.append(['Number of Members','Percentage of # Members (%)'])
    for r in records:
        x.append(r)

    t = Texttable()
    t.add_rows(x,header=True)
    print(t.draw())
    return
    
    
def q7():
    print("UNEMPLOYED GEOGRAPHIC member SEARCH: \n")
    skillname = input("Please enter skill name to check for unemployment: ")
    city = input("Please enter city where unemployed member with above skill resides: ")
    
    cursor.execute("select first_name                                                          \
                    from members natural join user_skills                                        \
                    where skill_name ='{}'                                                       \
                    and working_organization_id is NULL and city = '{}'".format(skillname,city) )                     
    records =  cursor.fetchall()
    x=[]
    x.append(['Members (Unemployed)'])
    for r in records:
        x.append(r)

    t = Texttable()
    t.add_rows(x,header=True)
    print(t.draw())
    return


def q8():
    print('---------------- COMPANY INITIATED JOB-OPENING AND MEMBER MATCH ---------------------')
    company = input("Please Enter Your Company: ")
    rolename = input("Please enter role name to be matched: ")
    experience_required = int(input("Please enter miniumum number of experience years: "))

    
    cursor.execute("select  distinct member_recommended_id as m1, \
                    (select first_name from members where members.member_id=member_recommended_id ), \
                     (select email from members where members.member_id=member_recommended_id )from  \
                    (skills_required natural join job_openings)                                      \
                    join members on (member_id = recruiter_id)                                        \
                    natural join skills_recommended                                                   \
                    where experience_required > {}                                                     \
                    and role = '{}'                                                         \
                    and first_name='{}' ".format(experience_required,rolename, company) )                     
    records =  cursor.fetchall()
    x=[]
    print('')
    print(" ----------------- COMPANY MATCH INITIATED : MATCHING " + company+ ' with MEMBERS -----------' )
    time.sleep(1)
    print('')

    x.append(['Member ID', 'Member Name', 'Contact Email'])
    for r in records:
        x.append(r)

    t = Texttable()
    t.add_rows(x,header=True)
    print(t.draw())
    return    



def q9():
    print('--------------------- MEMBER INITIATED JOB SEARCH -------------------------')
    member_id = input("Please enter member_id to search for matched job/openings: ")
    
    
    cursor.execute("  select distinct first_name, role, email                                                                   \
                      from ((skills_required  join user_skills on (skill_name=skills))                   \
                      natural join job_openings)                                                           \
                      join members on (members.member_id= job_openings.recruiter_id)                       \
                      where user_skills.member_id='{}'".format(member_id) )                       
    
    records =  cursor.fetchall()
    x=[]
    print('')
    print(" ----------- JOB MATCH INITIATED : MATCHING MEMBER_ID " + member_id +" with COMPANIES --------------")
    time.sleep(1)
    print('')

    x.append([ 'Company Matched with', 'Role Matched', 'Contact Email'])
    for r in records:
        x.append(r)

    t = Texttable()
    t.add_rows(x,header=True)
    print(t.draw())
    return    

def q10():
    print("FIND the TOP n POPULAR GROUPS: \n")
    n = input("Please enter the number of groups: ")
    
    cursor.execute(   "select group_id, sum(likes)  \
                       from posts join group_members\
                       on member_id=group_members_id \
                       group by group_id                \
                       order by sum                  \
                       desc limit {}".format(n) )                     
    records =  cursor.fetchall()
    x=[]
    x.append(['Group ID', 'Likes(Total)'])
    for r in records:
        x.append(r)

    t = Texttable()
    t.add_rows(x,header=True)
    print(t.draw())
    return


def q11():
    print("FIND the members who completed your course after a certain date: \n")

    course_name = input("Please enter the name of your course: ")
    date = input("Please enter the a date after which you want to see the results of (YYYY-MM-DD): ")
    
    cursor.execute(   " select first_name, date_completed from \
                            (members natural join member_courses) \
                            natural join linkedin_learning_courses \
                            where date_completed > '{}'   \
                            and course_name ='{}' ".format(date,course_name) )                     
    records =  cursor.fetchall()
    x=[]
    x.append(['Member Name', 'Course Complete On'])
    for r in records:
        x.append(r)

    t = Texttable()
    t.add_rows(x,header=True)
    print(t.draw())
    return


    
def command(choice): 
    if choice=='1':
        q1()
    elif choice=='2':
        q2()
    elif choice=='3':
        q3()
    elif choice=='4':
        q4()
    elif choice=='5':
        q5()
    elif choice=='6':
        q6()
    elif choice=='7':
        q7()
    elif choice=='8':
        q8()
    elif choice=='9':
        q9()
    elif choice=='10':
        q10()
    elif choice=='11':
        q11()
    else:
        print("Invalid choice: ENTER choice AGAIN to continue. Enter 'quit' to exit.")
    return
     
     



while True:
    # Queries 
    print("--------------------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------------------")
    print('')
    print('QUERIES:  ')
    print('')
    print('')
    print("1. ALL TABLES:: Show all Tables in Database LINKEDIN")
    print('')
    print("2. POSTS:: Display Names of members with posts in the year ____ sorted by _____ (ASC/DESC) Order in #Likes")
    print('')
    print("3. GEOGRAPHIC JOB SEARCH:: Job Openings in ____ City for ____ Role w/ experience >= ____")
    print('')
    print("4. MEMBER SEARCH:: Other members having ____ Skill(s)")
    print('')
    print("5. MEMBERS WITH SIMILAR GROUP INTEREST:: All Members in _____ group category")
    print('')
    print("6. MEMBERSHIP RATIOS:: Number of members in ______ Membership Type and _____ overall %")
    print('')
    print("7. UNEMPLOYED SEARCH:: Members having ______ skill who are currently Unemployed living in _____ City")
    print('')
    print("8. COMPANY INITIATED JOB-OPENING AND MEMBER MATCHING:: Members that are have recommended skill(s) for Opening Role ____\
                                                                  with required experience ________ in company ______ " )
    print('')
    print("9. MEMBER INITIATED JOB SEARCH:: Job Opening that match your recommended skill(s), Personalised Matching") 
    print('')    
    print("10. POPULAR GROUPS:: Find the Top _____ Groups based on user interaction like number of likes")
    print('')
    print("11. COURSE INSTRUCTOR ACCESS: Find members who have completed your course ______ after a certain date ______")

    print("--->Type 'quit' to end session")
    print("--------------------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------------------")
    print("--------------------------------------------------------------------------------------------------")
    print('')
    print('')
    choice=input("-------------->Enter Your Choice: ")
    if choice=='quit':
        break
    command(choice)
    _ = input('-------------------Press Any Key To Continue: ')


if(connection):
    #close the cursor 
    cursor.close()
    #Close connection
    connection.close()
    print("Connection closed to linkedin")
