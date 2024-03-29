import subprocess
import os

def in_bold(message):
    return '\033[1m' + message + '\033[0m'

def in_italics(message):
    return '\033[3m' + message + '\033[0m'

def underline_this(message):
    return '\033[4m' + message + '\033[0m'

def in_red(message):
    return '\033[31m' + message + '\033[0m'

def in_green(message):
    return '\033[32m' + message + '\033[0m'

def in_yellow(message):
    return '\033[33m' + message + '\033[0m'

def success():
    import time
    time.sleep(1)
    try:
        print("✅", end='\b\b')
        message = "✅"
    except:
        message = in_bold(in_green("SUCCESS"))
    return message

def warning():
    import time
    time.sleep(1)
    try:
        print("⚠️", end='\b\b')
        message = "⚠️"
    except:
        message = in_bold(in_yellow("WARNING"))
    return message

def failure():
    import time
    time.sleep(2)
    try:
        print("❌", end='\b\b')
        message = "❌"
    except:
        message = in_bold(in_red("FAILURE"))
    return message

def run_command(commands):
    command = commands[0]
    if len(commands) > 1:
        for c in commands:
            command += ' && ' + c
    proc = subprocess.Popen(command, shell="True", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result_code = proc.wait()
    return result_code

def run_command_and_show_output(commands):
    command = commands[0]
    if len(commands) > 1:
        for c in commands:
            command += ' && ' + c
    proc = subprocess.Popen(command, shell="True", stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while proc.poll() is None:
        line = str(proc.stdout.readline()).strip()
        if line != "b''":
            print(in_italics(line))
    result_code = proc.wait()
    return result_code

def file_exist(file_name, show_output=True):
    if show_output:
        print(f"Checking {file_name} ... ", end='')
    if os.path.isfile(file_name):
        if show_output:
            print(success())
        else:
            return True
    else:
        if show_output:
            print(failure())
            print(in_bold(in_yellow(f"Cannot find {file_name}.")))
        else:
            return False

def folder_exist(folder_name, show_output=True):
    if show_output:
        print(f"Checking existence of {folder_name} ... ",end='')
    if os.path.isdir(folder_name):
        if show_output:
            print(success())
        return True
    else:
        if show_output:
            print(failure())
            print(in_bold(in_red(f"Cannot find {folder_name}.")))
        return False

def is_dir_empty(dir_path):
    dir = os.listdir(dir_path)
    if len(dir) == 0:
        return True, None
    else:
        return False, dir