'''
Script to create directory structure and files for a new day of Advent of Code.
'''
import argparse
from datetime import datetime
import os
import requests
import sys

from dotenv import dotenv_values
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter


def aoc_new_day(day, year, id, update=False, name=None):
    # Create directory structure if needed
    path = f"{year}/Day{day}/"
    if not os.path.exists(path):
        print(f"Creating directory: {path}")
        os.makedirs(path, exist_ok=True)

    # Get and write / update README.md and example.txt
    url = f"https://adventofcode.com/{year}/day/{day}"
    read_me_and_example(
        url,
        f"{path}README.md",
        f"{path}example.txt",
        part=(2 if update else 1),
        id=id,
    )

    # Exit if only updating README.md
    if update:
        sys.exit()

    # Copy boilerplate.py and aoc_utils.py file
    template_path = f"{path}{name}.py"
    utils_path = f"{path}aoc_utils.py"
    os.system(f"cp template.py {template_path}")
    os.system(f"cp aoc_utils.py {utils_path}")

    # Save personal challenge input data
    out_path = f"{path}input.txt"
    url += "/input"
    r = requests.get(url, cookies={"session": id})
    if r.status_code == 200:
        with open(out_path, "w") as f:
            f.write(r.text)
    else:
        print(f"Status code: {r.status_code}")
        print(f"URL: {url}")
        print("Failed to fetch data")

    # Change into directory and start VS Code
    os.chdir(path)
    os.system('open -a "Visual Studio Code" .')


def create_arg_parser():
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
        default=datetime.now().year,
        help="Year of the challenge",
    )
    parser.add_argument("-n", "--name", type=str, default=None, help="Name of the file")

    parser.add_argument(
        "-u",
        "--update",
        type=bool,
        default=False,
        action="store",
        help="If update is set to true then only the README.md file will be updated for the content of the challenge.  No other files will be updated.  This is useful if you have already created the files for the day and just want to update the README.md file.",
    )
    return parser


def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


def read_me_and_example(
    url,
    readme_path,
    example_path,
    part=1,
    id=None,
):
    '''
    For Advent of Code, fetch the content from the URL and write the relevant part of the challenge description to a markdown file and write the first example data used in the challenge description to a text file.
    
    Parameters:
        url (str): URL to fetch
        readme_path (str): Path to README.md
        example_path (str): Path to example.txt
        part (int): Part number (1 or 2)
        id (str): Session cookie value
    
    If id is provided, it will be used to set the session cookie in the request which will allow the user to access the content for the day without logging in.
    
    If part is 2, the description of part 2 will be appended to the given markdown file.'''
    try:
        # Set up session cookie if provided
        cookies = {"session": id} if id else None

        # Fetch the content from the URL
        response = requests.get(url, cookies=cookies)
        response.raise_for_status()

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the <article> elements with class "day-desc"
        articles = soup.find_all("article", class_="day-desc")

        if not articles or len(articles) < part:
            print(f"No article for part {part} found.")
            return

        # Select the specified part
        article = articles[part - 1]

        # Determine file mode (append for Part 2, write otherwise)
        file_mode = "a" if part == 2 else "w"

        # Write the article content to README.md converting to Markdown
        with open(readme_path, file_mode) as f:
            f.write("\n")
            f.write(md(article))
            print(f"Article content for part {part} written to {readme_path}")

        # Find the first <pre><code> within the <article>
        code_block = article.find("pre")
        if code_block:
            code_text = code_block.get_text(strip=True)

            # Write code text to example.txt
            with open(example_path, "w", encoding="utf-8") as file:
                file.write(code_text)
                print(f"Code content written to {example_path}")
        else:
            print("No <pre><code> block found.")


    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Get command line arguments and id from .env file
    parser = create_arg_parser()
    args = parser.parse_args()
    id = dotenv_values(".env").get("MY_ID")
    name = args.name if args.name else f"day_{args.day}"

    # Exit if MY_ID not found in .env file
    if not id:
        print("MY_ID not found in .env file")
        sys.exit()

    # New day
    aoc_new_day(args.day, args.year, id, args.update, name)
