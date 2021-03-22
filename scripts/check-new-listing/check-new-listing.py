import requests
import os
import time
import send_mail


def get_last_listing():
    tag = "1ej4hfo"
    target = 5

    r = requests.get('https://www.binance.com/en/support/announcement/c-48')

    stack = []
    tags_seen = 0

    current_listing = ""

    for c in str(r.content):
        if tags_seen == target:
            if c == '"' or c == ">":
                continue
            if c == "<":
                break
            current_listing += c
        for i in range(len(tag)):
            if len(stack) == i and c == tag[i]:
                stack.append(c)
                if i == len(tag) - 1:
                    tags_seen += 1
                    stack.clear()
                break
            if i >= len(stack):
                stack.clear()
                break
    return current_listing


def write_to_file(file_name, content):
    f = open(file_name, "w")
    f.write(content)
    f.close()


THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
my_file = os.path.join(THIS_FOLDER, "last-new-listing.txt")
f = open(my_file, "r")
last_listing = f.read()
f.close()

if last_listing == "":
    last_listing = get_last_listing()
    write_to_file(my_file, last_listing)

while True:
    current_listing = get_last_listing()
    if current_listing != last_listing:
        message = "Subject: " + current_listing
        send_mail.send("turkmenatilla522@gmail.com", message)
        send_mail.send("denizbcakiroglu@gmail.com", message)
        write_to_file(my_file, current_listing)
    time.sleep(60)
