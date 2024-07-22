#!/usr/bin/python

# Chunis Deng (chunchengfh@gmail.com)

import cmds
from interface import SPILink
from middleware import *
from utils import bytes2hexstr
from callbacks import *


cmd_dict = {}
cmd_name_list = []
for cmd, val in cmds.__dict__.items():
    if cmd.startswith('CMD_'):
        cmd_dict[cmd] = val
        cmd_name_list.append(cmd[4:].lower())


def callback_help(cstr):
    cmd = 'CMD_' + cstr.upper()
    if cmd in cmd_dict:
        cmd_dict[cmd][cmds_idx_help]()
    else:
        print("Not a valid command; type 'help' for the list of available commands")


def callback(radio, cstr, args = []):
    cmd = 'CMD_' + cstr.upper()
    if cmd in cmd_dict:
        cmd_dict[cmd][cmds_idx_func](radio, cmd_dict[cmd], args)
    else:
        print("Not a valid command; type 'help' for the list of available commands")


def process_line(radio, line):
    if not line: return

    items = line.split()
    if len(items) == 1:
        callback(radio, items[0], [])
        return

    # check if need to call help() for the specific command
    if items[1] == '-h' or items[1] == '--help':
        callback_help(items[0])
        return

    cmd, args = items[0], items[1:]
    callback(radio, cmd, args)


def help():
    print("arguments are seperated by whitespace.")
    print("\nAvailable commands are:")
    for cmd in sorted(cmd_name_list):
        print(cmd)
    print()


print('\nWelcome to use Wi-Fi Listener based on Modem-E v1.x')
print("Input 'help' for help.\n")

radio = SPILink()
while True:
    line = input('>> ').strip().lower()
    if not line:
        continue
    elif line == 'help':
        help()
    else:
        process_line(radio, line)
