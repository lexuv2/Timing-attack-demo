import psycopg2
import random
from tqdm import tqdm
import config
from torch import rand
n_good_users = 50
n_bad_users = 100
drop = True
percent_usernames = 0.5

create = """CREATE TABLE IF NOT EXISTS "users" (
  "id" SERIAL PRIMARY KEY,
  "username" VARCHAR(255) NOT NULL,
  "password" VARCHAR(255) NOT NULL,
  "email" VARCHAR(255) NOT NULL,
  "description" VARCHAR(255) NOT NULL
);"""

conn = psycopg2.connect(dbname=config.dbname, user=config.db_user, password=config.db_password, host=config.db_host, port=config.db_port)
curr = conn.cursor()

if drop:
    curr.execute("DROP TABLE IF EXISTS users;")
    conn.commit()
    curr.execute(create)
    conn.commit()

usernames_file = open('usernames.txt', 'r')
passwords_file = open('passwords.txt', 'r')

usernames_to_add = usernames_file.readlines()
passwords = passwords_file.readlines()
usernames = random.sample(usernames_to_add, int(len(usernames_to_add) * percent_usernames))





for x in tqdm(usernames):
    username = x.strip()
    password = random.choice(passwords).strip()
    curr.execute(f"INSERT INTO users (username, password, email, description) VALUES ('{username}', '{password}', 'emailtest' , 'description');")
conn.commit()


#get users count from db
curr.execute("SELECT COUNT(*) FROM users")
users_count = curr.fetchone()[0]
print(f"Users count: {users_count}")


file = open("usernames_to_test.txt", "w")
for username in random.sample(usernames, n_good_users):
    file.write(username)

with open("usernames.txt","r") as basefile:
    all_usernames = basefile.readlines()
    for i in range(n_bad_users):
        bad_name = random.choice(all_usernames)
        while bad_name in usernames:
            bad_name = random.choice(all_usernames)
        file.write(bad_name)
file.close()

#shuffle usernames_to_test
with open("usernames_to_test.txt","r") as file:
    lines = file.readlines()
    random.shuffle(lines)
    file.close()
with open("usernames_to_test.txt","w") as file:
    file.writelines(lines)
    file.close()

