import psycopg2
import random

import config

conn = psycopg2.connect(dbname=config.dbname, user=config.db_user, password=config.db_password, host=config.db_host, port=config.db_port)
curr = conn.cursor()








curr.execute("SELECT * FROM users")
users = curr.fetchall()
usernames = []
for user in users:
    usernames.append(user[1])
#remove duplicates
all_usernames = list(set(usernames))
print(usernames)


file = open("usernames_to_test.txt", "r")
usernames_to_test = file.readlines()
file.close()

##find intersection
common_usernames = []
for username in usernames_to_test:
    if username.strip() in all_usernames:
        common_usernames.append(username.strip())
print("Common usernames:")        
print(common_usernames)

file = open("common_usernames.txt", "w")
for username in common_usernames:
    file.write(username + "\n")
file.close()

##print one user and his password
print()
print("One user:")
curr.execute("SELECT * FROM users LIMIT 1")
print(curr.fetchone())

