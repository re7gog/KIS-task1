import csv
import getpass
import os
import re
import socket
import argparse
import base64


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

if (args.script):
    try:
        with open(args.script) as file:
            for line in file:
                line = line.strip()
                if (line == "exit"):
                    break
                elif (line == ""):
                    continue
                line = substitute_env_vars(line)
                if (line == "ls"):
                    print("ls")
                elif (line == "cd"):
                    print("cd")
                elif (line == "read"):
                    input()
                else:
                    print("Error: unknown command")
                    break
    except FileNotFoundError:
        print(f"Error: File '{args.path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

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
                    str64 = base64.b64decode(row[-1])
                    vhs_matrix.append(str64.decode("utf-8"))
        except FileNotFoundError:
            print(f"Error: File '{args.vhs}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

vhs_reader()

while True:
    line = input(username + "@" + hostname + "$")
    if (line == "exit"):
        break
    elif (line == ""):
        continue
    elif (line == "ls"):
        print("ls")
    elif (line == "cd"):
        print("cd")
    else:
        print("Error: unknown command")
        break
