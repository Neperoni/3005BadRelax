### Assignment 3 Question 1

# Steps:
First you must setup a postgre sql database
The code is set to connect to a server with the following parameters:
##### 127.0.01:5432
##### username: postgre
##### password: 3005

The server is assumed to be using the schema matching the definition in Students.sql

### if these are not the settings of your database, please change the parameters of the psycopg2 connection



next you just need to run the python code while the server is running

and then you can input 0-4 as the inputs
#### 0: quit
#### 1: get students
#### 2: add student
#### 3: update email
#### 4: delete student

depending on selection it will ask for attributes one at a time
and if any attribute is incorrect, will continue to ask for  the attribute until valid


