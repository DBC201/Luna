import argparse
import json
import sys
import os


def return_parser():
    parser = argparse.ArgumentParser(description="Show how many of the coins are up after given ms")
    parser.add_argument("src_path", type=str, help="directory which contains trades")
    return parser


args = return_parser().parse_args(sys.argv[1:])
FOLDER = args.src_path

if not os.path.isdir(FOLDER):
    print("folder does not exist")
    sys.exit()

up = 0
down = 0

for filename in os.listdir(FOLDER):
    with open(FOLDER + "/" + filename) as f:
        data = json.load(f)
        opening_price = float(data[0]["price"])
        closing_price = float(data[-1]["price"])
        print(closing_price - opening_price)
        if closing_price > opening_price:
            up += 1
        else:
            down += 1
print("UP: " + str(up))
print("DOWN: " + str(down))
