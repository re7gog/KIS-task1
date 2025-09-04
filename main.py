import csv
import getpass
import os
import re
import socket
import argparse
import base64
from datetime import datetime

help_note = """
exit - exit from shell
ls - list files in current directory
tree - print tree of files
cd [path] - change current directory
rmdir [dir] - remove directory
history - history of entered commands
date - current datetime
help - this command
"""

username = getpass.getuser()
hostname = socket.gethostname()

parser = argparse.ArgumentParser()
parser.add_argument("--vhs", type=str, help="Path to VFS")
parser.add_argument("--script", type=str, help="Path to start script")
args = parser.parse_args()

print("Path to VHS:", args.vhs)
print("Path to start script:", args.script)

def substitute_env_vars(s):
  # Создаёт захватывающую группу с именем переменной находя знак $ и буквы после него
  pattern = r'\$(\w+)'

  # Функция для обработки каждого совпадения
  def replace_match(match):
    var_name = match.group(1) # Содержимое группы (имя переменной)
    return os.environ.get(var_name, match.group(0))  # Получить значение, или если не получилось, вернуть название

  # Обработка регулярным выражением
  return re.sub(pattern, replace_match, s)

vhs_matrix = []
def vhs_reader():
    if (args.vhs):
        try:
            with open(args.vhs) as file:
                csv_reader = csv.reader(file)
                try:
                    header_row = next(csv_reader)
                    column_count = len(header_row)
                except StopIteration:
                    print("Error: The CSV file is empty.")
                    return
                if column_count != 3:
                    print(f"Error: The file does not have 3 columns. Found {column_count} columns.")
                    return
                vhs_matrix.append(header_row)
                for row in csv_reader:
                    if(row[-1] != '~'):
                        str64 = base64.b64decode(row[-1])
                        row12 = row[:-1]
                        row12.append(str64.decode("utf-8"))
                        vhs_matrix.append(row12)
                    else:
                        vhs_matrix.append(row)
        except FileNotFoundError:
            print(f"Error: File '{args.vhs}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

vhs_reader()

curr_dir = ""
cmd_history = []

if (args.script):
    try:
        with open(args.script) as file:
            for line in file:
                line = line.strip()
                line = substitute_env_vars(line)
                line_spl = line.split()
                if (line == "exit"):
                    break
                elif (line == ""):
                    continue
                elif (line == "ls"):
                    for l in vhs_matrix:
                        full_path, ftype, data = l
                        splitted_path = full_path.split("/")
                        dir = "/".join(splitted_path[:-1])
                        filename = splitted_path[-1]
                        if (dir == curr_dir):
                            print(filename)
                    cmd_history.append(line)
                elif (line == "tree"):
                    sorted_matrix = sorted(vhs_matrix, key=lambda i: str(i[0].count("/")) + i[1] + i[0].split("/")[-1])
                    for l in sorted_matrix:
                        full_path, ftype, data = l
                        splitted_path = full_path.split("/")
                        dir_tab = "--" * len(splitted_path[:-1])
                        filename = splitted_path[-1]
                        if (ftype == "2"):
                            filename += ":"
                        print(dir_tab + filename)
                    cmd_history.append(line)
                elif (line_spl[0] == "cd"):
                    move_to = line_spl[1]
                    if (move_to == ".."):
                        curr_dir = "/".join(curr_dir.split("/")[:-1])
                    else:
                        for l in vhs_matrix:
                            full_path, ftype, data = l
                            if (ftype == "2"):
                                dirname = full_path.split("/")[-1]
                                if (dirname == move_to):
                                    curr_dir += "/" + dirname
                                    break
                    cmd_history.append(line)
                elif (line == "history"):
                    for cmd in cmd_history:
                        print(cmd)
                    cmd_history.append(line)
                elif (line == "date"):
                    current_datetime = datetime.now()
                    print(current_datetime)
                elif (line == "read"):
                    input()
                else:
                    print("Error: unknown command")
                    break
    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

while True:
    line = input(username + "@" + hostname + "$")
    line = substitute_env_vars(line)
    line_spl = line.split()
    if (line == "exit"):
        break
    elif (line == ""):
        continue
    elif (line == "ls"):
        for l in vhs_matrix:
            full_path, ftype, data = l
            splitted_path = full_path.split("/")
            dir = "/".join(splitted_path[:-1])
            filename = splitted_path[-1]
            if (dir == curr_dir):
                print(filename)
        cmd_history.append(line)
    elif (line == "tree"):
        sorted_matrix = sorted(vhs_matrix, key=lambda i: str(i[0].count("/")) + i[1] + i[0].split("/")[-1])
        for l in sorted_matrix:
            full_path, ftype, data = l
            splitted_path = full_path.split("/")
            dir_tab = "--" * len(splitted_path[:-1])
            filename = splitted_path[-1]
            if (ftype == "2"):
                filename += ":"
            print(dir_tab + filename)
        cmd_history.append(line)
    elif (line_spl[0] == "cd"):
        move_to = line_spl[1]
        if (move_to == ".."):
            curr_dir = "/".join(curr_dir.split("/")[:-1])
        else:
            for l in vhs_matrix:
                full_path, ftype, data = l
                if (ftype == "2"):
                    dirname = full_path.split("/")[-1]
                    if (dirname == move_to):
                        curr_dir += "/" + dirname
                        break
        cmd_history.append(line)
    elif (line_spl[0] == "rmdir"):
        to_remove = curr_dir + "/" + line_spl[1]
        new_matrix = []
        for i in vhs_matrix:
            full_path, ftype, data = i
            if(not full_path.startswith(to_remove)):
                new_matrix.append(i)
        vhs_matrix = new_matrix
        cmd_history.append(line)
    elif (line == "history"):
        for cmd in cmd_history:
            print(cmd)
        cmd_history.append(line)
    elif (line == "date"):
        current_datetime = datetime.now()
        print(current_datetime)
    elif (line == "help"):
        print(help_note)
    else:
        print("Error: unknown command")
