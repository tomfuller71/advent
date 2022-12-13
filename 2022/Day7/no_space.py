'''
--- Day 7: No Space Left On Device ---
You can hear birds chirping and raindrops hitting leaves as the expedition proceeds. Occasionally, you can even hear much louder sounds in the distance; how big do the animals get out here, anyway?

The device the Elves gave you has problems with more than just its communication system. You try to run a system update:

$ system-update --please --pretty-please-with-sugar-on-top
Error: No space left on device
Perhaps you can delete some files to make space for the update?

You browse around the filesystem to assess the situation and save the resulting terminal output (your puzzle input). For example:

$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
The filesystem consists of a tree of files (plain data) and directories (which can contain other directories or files). The outermost directory is called /. You can navigate around the filesystem, moving into or out of directories and listing the contents of the directory you're currently in.

Within the terminal output, lines that begin with $ are commands you executed, very much like some modern computers:

cd means change directory. This changes which directory is the current directory, but the specific result depends on the argument:
cd x moves in one level: it looks in the current directory for the directory named x and makes it the current directory.
cd .. moves out one level: it finds the directory that contains the current directory, then makes that directory the current directory.
cd / switches the current directory to the outermost directory, /.
ls means list. It prints out all of the files and directories immediately contained by the current directory:
123 abc means that the current directory contains a file named abc with size 123.
dir xyz means that the current directory contains a directory named xyz.
Given the commands and output in the example above, you can determine that the filesystem looks visually like this:

- / (dir)
  - a (dir)
    - e (dir)
      - i (file, size=584)
    - f (file, size=29116)
    - g (file, size=2557)
    - h.lst (file, size=62596)
  - b.txt (file, size=14848514)
  - c.dat (file, size=8504156)
  - d (dir)
    - j (file, size=4060174)
    - d.log (file, size=8033020)
    - d.ext (file, size=5626152)
    - k (file, size=7214296)
Here, there are four directories: / (the outermost directory), a and d (which are in /), and e (which is in a). These directories also contain files of various sizes.

Since the disk is full, your first step should probably be to find directories that are good candidates for deletion. To do this, you need to determine the total size of each directory. The total size of a directory is the sum of the sizes of the files it contains, directly or indirectly. (Directories themselves do not count as having any intrinsic size.)

The total sizes of the directories above can be found as follows:

The total size of directory e is 584 because it contains a single file i of size 584 and no other directories.
The directory a has total size 94853 because it contains files f (size 29116), g (size 2557), and h.lst (size 62596), plus file i indirectly (a contains e which contains i).
Directory d has total size 24933642.
As the outermost directory, / contains every file. Its total size is 48381165, the sum of the size of every file.
To begin, find all of the directories with a total size of at most 100000, then calculate the sum of their total sizes. In the example above, these directories are a and e; the sum of their total sizes is 95437 (94853 + 584). (As in this example, this process can count files more than once!)

Find all of the directories with a total size of at most 100000. What is the sum of the total sizes of those directories?
'''

import sys
import re
from typing import Optional
from dataclasses import dataclass
from collections import deque


@dataclass
class File:
    name: str
    size: int
    parent: 'Directory'

class Directory:
    def __init__(self, name: str, parent: Optional['Directory']=None) -> None:
        self.name = name
        self.parent: Optional['Directory'] = parent
        self.files: list[File] = []
        self.sub_folders: dict[str, Directory] = {}
        self.size = 0
    
    def add_file(self, file: File) -> None:
        self.files.append(file)
        self.size += file.size
    
    def add_dir(self, name: str) -> None:
        self.sub_folders[name] = Directory(name, self)
    
    def get_size(self) -> int:
        return self.size + sum([folder.get_size() for folder in self.sub_folders.values()])
    
    def list(self, indent: int=0) -> None:
        spaces = '  ' * indent
        print(f'{spaces}- {self.name} (dir, size={self.get_size():,})')
        for folder in self.sub_folders.values():
            folder.list(indent=indent+1)
        for file in self.files:
            print(f'{spaces}  - {file.name} (file, size={file.size:,})')


class FileSystem:
    def __init__(self, max_capacity: int = 70_000_000) -> None:
        self.root = Directory('/')
        self.current_dir = self.root
        self.max = max_capacity
    
    def change_directory(self, name: str) -> None:
        if name == '/':
            self.current_dir = self.root
        elif name == '..':
            self.current_dir = self.current_dir.parent if self.current_dir.parent else self.current_dir
        else:
            self.current_dir = self.current_dir.sub_folders[name]
    
    def list_current_directory(self) -> None:
        self.current_dir.list()

    def list_all_directories(self) -> None:
        self.root.list()
    
    def add_file(self, name: str, size: int) -> None:
        self.current_dir.add_file(File(name, size, self.current_dir))
    
    def add_dir(self, name: str) -> None:
        self.current_dir.add_dir(name)
    
    def get_size(self) -> int:
        return self.root.get_size()
    
    def available_space(self) -> int:
        return self.max - self.get_size()
    
    def get_sub_folders_sizes(self) ->list[tuple[str, int]]:
        found_names_and_sizes = []
        directory_queue = deque([self.root])
        while directory_queue:
            current = directory_queue.popleft()
            for folder in current.sub_folders.values():
                found_names_and_sizes.append((folder.name, folder.get_size()))
            directory_queue.extend(current.sub_folders.values())

        return found_names_and_sizes
    
    def sum_sub_folders_sizes_under(self, limit: int) -> int:
        return sum([size for _, size in self.get_sub_folders_sizes() if size <= limit])
    
    def get_smallest_dir_gt(self, limit: int) -> int:
        return min([size for _, size in self.get_sub_folders_sizes() if size > limit])
    
    def delete_size_to_fit(self, size: int) -> int:
        limit = size - self.available_space()
        return self.get_smallest_dir_gt(limit)


class LogParser:
    def __init__(self, log: str) -> None:
        self.file_system = FileSystem()
        self.log = log
    
    def is_cd_command(self, line: str) -> bool:
        return line.startswith('$ cd')

    def is_file(self, line: str) -> bool:
        return re.match(r'\d+ .+', line) is not None

    def is_dir(self, line: str) -> bool:
        return re.match(r'dir .+', line) is not None

    def parse_line(self, line: str) -> None:
        if self.is_cd_command(line):
            command = line.split(' ')[2]
            self.file_system.change_directory(command)
        elif self.is_file(line):
            size, name = line.split(' ')
            self.file_system.add_file(name, int(size))
        elif self.is_dir(line):
            name = line.split(' ')[1]
            self.file_system.add_dir(name)
        elif line.startswith('$ ls'):
            pass
        else:
            raise ValueError(f'Unknown command: {line}')
    
    def parse(self) -> None:
        for line in self.log.splitlines():
            self.parse_line(line)


'''
--- Part Two ---
Now, you're ready to choose a directory to delete.

The total disk space available to the filesystem is 70000000. To run the update, you need unused space of at least 30000000. You need to find a directory you can delete that will free up enough space to run the update.

In the example above, the total size of the outermost directory (and thus the total amount of used space) is 48381165; this means that the size of the unused space must currently be 21618835, which isn't quite the 30000000 required by the update. Therefore, the update still requires a directory with total size of at least 8381165 to be deleted before it can run.

To achieve this, you have the following options:

Delete directory e, which would increase unused space by 584.
Delete directory a, which would increase unused space by 94853.
Delete directory d, which would increase unused space by 24933642.
Delete directory /, which would increase unused space by 48381165.
Directories e and a are both too small; deleting them would not free up enough space. However, directories d and / are both big enough! Between these, choose the smallest: d, increasing unused space by 24933642.

Find the smallest directory that, if deleted, would free up enough space on the filesystem to run the update. What is the total size of that directory?
'''


def main(data: str):
    parser = LogParser(data)
    parser.parse()

    print('Part 1:')
    sum_of_folders = parser.file_system.sum_sub_folders_sizes_under(100000)
    print(f'    Sum of folders <= 100,000: {sum_of_folders:,}')

    print('\nPart 2:')
    size = parser.file_system.get_size()
    available = parser.file_system.available_space()
    needed = 30_000_000
    to_free = needed - available
    smallest = parser.file_system.delete_size_to_fit(needed)
    print(f'    Filesystem current size: {size:,}')
    print(f'    Available: {available:,}')
    print(f'    Need to free: {to_free:,}')
    print(f'    Smallest suitable folder: {smallest:,}\n')

    parser.file_system.list_all_directories()


if __name__ == '__main__':
    datafile = 'example.txt'
    if len(sys.argv) > 1 and sys.argv[1].endswith('.txt'):
        datafile = sys.argv[1]

    with open(datafile) as f:
        data = f.read()

    main(data)