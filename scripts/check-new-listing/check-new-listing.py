import requests

last_listing = input()

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

if last_listing != current_listing:
    print("New listing!!")
