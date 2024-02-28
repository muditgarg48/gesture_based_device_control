import os
from global_variables import logger_folder_name

def launch_tensorboard_monitor():
    os.system('ls' if os.name == 'nt' else 'dir')
    os.system(f'cd {logger_folder_name}')
    os.system('cd train')
    os.system('tensorboard --logdir=.')

def main():
    launch_tensorboard_monitor()

if __name__ == '__main__':
    main()