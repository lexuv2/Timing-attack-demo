
import random

max_lines = 1000

username_file = open('usernames.txt', 'r')
usernames = username_file.readlines()
username_file.close()
new_usernames = []
if len(usernames) > max_lines:
    new_usernames = random.sample(usernames, max_lines)
    file = open('usernames.txt', 'w')
    for username in new_usernames:
        file.write(username)
    file.close()