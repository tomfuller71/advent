import requests
import sys

myId  = "53616c7465645f5fd74d50fb964653fc91b8db2cbf8ad39add4b3b79f4a469f1f056098883b1eaa34da9d0fc27ad0c40d42758fdc6f2ed9f42cb282f841643e4"

def save_data(day, outfile_name):
    out_path = f"Day{day}/{outfile_name}.txt"
    url = f"https://adventofcode.com/2022/day/{day}/input"
    cookies = {"session": myId}
    r = requests.get(url, cookies=cookies)
    with open(out_path, "w") as f:
        f.write(r.text)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2:
        print("Usage: python save_advent_data.py day outfile_name")
        sys.exit(1)
    
    day, outfile_name = args
    save_data(day, outfile_name)