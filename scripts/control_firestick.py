import os
from commandline_functions import *

def command_connect(ip):
    return f"adb connect {ip}"

def gen_command(prompt):
    command = "adb shell input keyevent "
    if prompt == 'up':
        command += '19'
    elif prompt == 'down':
        command += '20'
    elif prompt == 'left':
        command += '21'
    elif prompt == 'right':
        command += '22'
    elif prompt == 'toggle_play':
        command += '85'
    elif prompt == 'rewind':
        command += '89'
    elif prompt == 'fast_forward':
        command += '90'
    elif prompt == 'select':
        command += '23'
    elif prompt == 'menu':
        command += '82'
    elif prompt == 'voice':
        command += '130'
    elif prompt == 'back':
        command += '4'
    return command

def command_disconnect():
    return "adb disconnect"

def operate_firestick(prompt):
    os.system(gen_command(prompt))

def main():
    import time
    os.system(command_disconnect())
    print(in_yellow("Remember to enable ADB debugging by going into My Fire TV > Developer Options > ADB Debugging > ON"))
    print(in_green("IP Address can be found at My Fire TV > About > Network > IP Address"))
    print(in_yellow("Remember to connect this device and your Fire TV to the same network!"))
    ip_add = input("Enter the IP address of the Fire TV: ")
    os.system(command_connect(ip_add))
    choice = input("Manual (M)/ Automatic (A) Testing: ").lower()
    if choice == 'a':
        commands = ["up", "down", "left", "right", "select", "back"]
        for command in commands:
            print(in_bold(f"Sending the command '{command}' ... "),end='')
            try:
                operate_firestick(command)
                issue_success()
            except:
                issue_failure()
            time.sleep(1)
    else:
        command = " "
        commands = ["up", "down", "left", "right", "toggle_play", "rewind", "fast_forward", "select", "menu", "voice", "back"]
        print(in_bold("Commands: "),end='')
        print(in_green(str(commands)))
        while len(command) != 0 :
            command = input(in_bold("Enter command: "))
            if command in commands:
                print(in_bold(f"Sending the command '{command}' ... "),end='')
                try:
                    operate_firestick(command)
                    issue_success()
                except:
                    issue_failure()
            elif(len(command) != 0):
                print(in_red(f"Command {command} not found!!"))

if __name__ == '__main__':
    main()