"""
Script to create directory structure and files for a new day of Advent of Code.
"""

import argparse
from datetime import datetime
import os
import requests
import sys

from dotenv import dotenv_values
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter


def aoc_new_day(day, year, id, update=False, name=None, submit=False):
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

    # Check if files already exist to avoid overwriting
    if not os.path.exists(template_path):
        os.system(f"cp template.py {template_path}")
        print(f"Created {template_path}")
    else:
        print(f"File {template_path} already exists, skipping...")

    if not os.path.exists(utils_path):
        os.system(f"cp aoc_utils.py {utils_path}")
        print(f"Created {utils_path}")
    else:
        print(f"File {utils_path} already exists, skipping...")

    # Save personal challenge input data
    out_path = f"{path}input.txt"
    if not os.path.exists(out_path):
        url += "/input"
        r = requests.get(url, cookies={"session": id})
        if r.status_code == 200:
            with open(out_path, "w") as f:
                f.write(r.text)
            print(f"Downloaded input to {out_path}")
        else:
            print(f"Status code: {r.status_code}")
            print(f"URL: {url}")
            print("Failed to fetch data")
    else:
        print(f"Input file {out_path} already exists, skipping download...")

    # Create a solutions tracking file
    solutions_path = f"{path}solutions.txt"
    if not os.path.exists(solutions_path):
        with open(solutions_path, "w") as f:
            f.write("Part 1: \nPart 2: \n")
        print(f"Created {solutions_path}")

    # Change into directory and start VS Code
    os.chdir(path)
    if submit:
        print("Opening in VS Code...")
        os.system('open -a "Visual Studio Code" .')

    print(f"Setup complete for Day {day}, {year}!")
    print(f"Working directory: {os.getcwd()}")
    print(
        f"Files created: {name}.py, aoc_utils.py, input.txt, example.txt, README.md, solutions.txt"
    )


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
        action="store_true",
        help="Only update the README.md file with part 2 content. No other files will be created/updated.",
    )
    parser.add_argument(
        "--no-vscode",
        action="store_true",
        help="Don't open VS Code after setup",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate that the session ID is working by testing a request",
    )
    return parser


def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


def validate_session(id, year=None):
    """Validate that the session ID works by making a test request."""
    if year is None:
        year = datetime.now().year

    test_url = f"https://adventofcode.com/{year}/day/1"
    try:
        r = requests.get(test_url, cookies={"session": id})
        if r.status_code == 200 and "Please log in" not in r.text:
            print("✅ Session ID is valid!")
            return True
        else:
            print("❌ Session ID appears to be invalid or expired")
            return False
    except Exception as e:
        print(f"❌ Error validating session: {e}")
        return False


def read_me_and_example(
    url,
    readme_path,
    example_path,
    part=1,
    id=None,
):
    """
    For Advent of Code, fetch the content from the URL and write the relevant part of the challenge description to a markdown file and write the first example data used in the challenge description to a text file.

    Parameters:
        url (str): URL to fetch
        readme_path (str): Path to README.md
        example_path (str): Path to example.txt
        part (int): Part number (1 or 2)
        id (str): Session cookie value

    If id is provided, it will be used to set the session cookie in the request which will allow the user to access the content for the day without logging in.

    If part is 2, the description of part 2 will be appended to the given markdown file.
    """
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
        print("❌ MY_ID not found in .env file")
        print("Please create a .env file with your Advent of Code session ID:")
        print("MY_ID=your_session_id_here")
        sys.exit(1)

    # Validate session if requested
    if args.validate:
        validate_session(id, args.year)
        sys.exit()

    # New day
    try:
        aoc_new_day(args.day, args.year, id, args.update, name, not args.no_vscode)
    except KeyboardInterrupt:
        print("\n⚠️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error during setup: {e}")
        sys.exit(1)
