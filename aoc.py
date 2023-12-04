import argparse
import datetime
import os
import requests
import sys

from dotenv import dotenv_values


# Load configuration
config = dotenv_values(".env")

# Create argument parser
parser = argparse.ArgumentParser(
    description="Create template files for a new day of Advent of Code",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("day", type=int, help="Advent of Code day")
parser.add_argument(
    "-y",
    "--year",
    type=int,
    default=datetime.datetime.now().year,
    help="Year of the challenge",
)
parser.add_argument("-n", "--name", type=str, default=None, help="Name of the file")

# Parse arguments
args = parser.parse_args()

# Set default name if not provided
if args.name is None:
    args.name = f"day_{args.day}"

day = args.day
name = args.name
year = args.year

# Create directory structure
year_dir = str(year)
if not os.path.exists(year_dir):
    os.mkdir(year_dir)

day_dir = f"{year_dir}/Day{day}/"
os.makedirs(day_dir, exist_ok=True)

# Create standard example file
example_file_path = f"{day_dir}example.txt"
with open(example_file_path, "w") as f:
    f.write("")

# Copy boilerplate.py file
boilerplate_path = f"{day_dir}{name}.py"
os.system(f"cp boilerplate.py {boilerplate_path}")

# Save data
out_path = f"{day_dir}input.txt"
url = f"https://adventofcode.com/{year}/day/{day}/input"
id = config.get("MY_ID")
if not id:
    print("MY_ID not found in .env file")
    sys.exit(1)

cookies = {"session": id}
r = requests.get(url, cookies=cookies)
if r.status_code == 200:
    with open(out_path, "w") as f:
        f.write(r.text)
else:
    print(f"Status code: {r.status_code}")
    print(f"URL: {url}")
    print("Failed to fetch data")

# Change into directory and start VS Code
os.chdir(f"{year}/Day{day}")
os.system('open -a "Visual Studio Code" .')
