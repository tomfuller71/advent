import requests
import sys
import argparse
import os
from dotenv import dotenv_values
import datetime


config = dotenv_values(".env")
current_year = datetime.datetime.now().year


def create_directory_structure(day, year):
    if not os.path.exists(f'{year}'):
        os.mkdir(str(year))
    path = f"{year}/Day{day}/"
    try:
        os.mkdir(path)
    except FileExistsError:
        pass


def create_standard_example_file(day, year):
    path = f"{year}/Day{day}/example.txt"
    with open(path, "w") as f:
        f.write("")


def copy_boilerplate_py_file(day, name, year):
    path = f"{year}/Day{day}/{name}.py"
    os.system(f"cp boilerplate.py {path}")


def save_data(day, year):
    out_path = f"{year}/Day{day}/input.txt"
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    id = config.get("MY_ID")
    if not id:
        print("MY_ID not found in .env file")
        sys.exit(1)
    cookies = {"session": id}
    r = requests.get(url, cookies=cookies)
    with open(out_path, "w") as f:
        f.write(r.text)


def create_template_files(day, name, year):
    create_directory_structure(day, year)
    create_standard_example_file(day, year)
    copy_boilerplate_py_file(day, name, year)
    save_data(day, year)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="setup.py",
        description="Create new folder and template files for a new day of Advent of Code",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("day", type=int, help="Advent of Code day")
    parser.add_argument("-y", "--year", type=int, default=current_year, 
                        help="Year of the challenge")
    parser.add_argument("-n", "--name", type=str, default='day_{day}', help="Name of the file")
    args = parser.parse_args()

    if args.name == "day_{day}":
        args.name = f"day_{args.day}"

    create_template_files(args.day, args.name, args.year)
