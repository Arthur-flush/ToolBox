#!/bin/python3
import time as t
import random as r
import sys,tty,termios
import colorama

text = """
   ▄████████ ▀█████████▄   ▄██████▄      ███     
  ███    ███   ███    ███ ███    ███ ▀█████████▄ 
  ███    ███   ███    ███ ███    ███    ▀███▀▀██ 
  ███    ███  ▄███▄▄▄██▀  ███    ███     ███   ▀ 
▀███████████ ▀▀███▀▀▀██▄  ███    ███     ███     
  ███    ███   ███    ██▄ ███    ███     ███     
  ███    ███   ███    ███ ███    ███     ███     
  ███    █▀  ▄█████████▀   ▀██████▀     ▄████▀   
                                                 
                                                 
                                                 """
                                                 

class _Getch:       
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch                                       

def slowprint(text):
    for l in text.split("\n"):
        print(l)
        t.sleep(0.05)

commands = [] # list of commands executed, max size = 100

def execute(command):
    print('\n' + command)
    t.sleep(0.05)
    commands.append(command)
    if len(commands) > 100:
        commands.pop(0)
    
def uparrow():
    global command, command_pos, cursor_pos
    command_pos += 1
    if command_pos > len(commands):
        command_pos = 0
    if command_pos == 0:
        command = ""
    else:
        command = commands[len(commands)-command_pos]
    
    
    # replace the command in the command line
    print("\033[2K", end="\r")
    print("[ABot]>>> ", end="")
    print(command, end="", flush=True)
    
    cursor_pos = len(command)

def downarrow():
    global command, command_pos, cursor_pos
    command_pos -= 1
    if command_pos < 0:
        command_pos = 0
    if command_pos == 0:
        command = ""
    else:
        command = commands[len(commands)-command_pos]
    
    
    
    # replace the command in the command line
    print("\033[2K", end="\r")
    print("[ABot]>>> ", end="")
    print(command, end="", flush=True)
    
    cursor_pos = len(command)
    
def leftarrow(): # moves the cursor left
    global command, cursor_pos
    if cursor_pos > 0:
        cursor_pos -= 1
        print("\033[D", end="", flush=True)
        

def rightarrow(): # moves the cursor right
    global command, cursor_pos
    if cursor_pos < len(command):
        cursor_pos += 1
        print("\033[C", end="", flush=True)

def backspace(): # deletes the character to the left of the cursor
    global command, cursor_pos
    if cursor_pos > 0:
        print("\b", end="")
        command = command[:cursor_pos-1] + command[cursor_pos:]
        cursor_pos -= 1
        
        # replace the command in the command line
        print("\033[2K", end="\r")
        print("[ABot]>>> ", end="")
        print(command, end="")
        
        # move the cursor back to the correct position
        print("\033[D" * len(command[cursor_pos:]), end="", flush=True)
        
def delete(): # deletes the character to the right of the cursor
    #TODO
    pass


slowprint(text)
command = ""
command_pos = 0
cursor_pos = 0
inkey = _Getch()
print("[ABot]>>> ", end="", flush=True)
while True:
    try:
        while 1:
            k = inkey()
            if k != '':
                break
            t.sleep(0.01)
        
        if k == '\x1b':
            key1 = inkey()
            key2 = inkey()
            if (key1 == '[') and (key2 == 'A'):
                uparrow()
                
            elif (key1 == '[') and (key2 == 'B'):
                downarrow()
                
            elif (key1 == '[') and (key2 == 'C'):
                rightarrow()
                
            elif (key1 == '[') and (key2 == 'D'):
                leftarrow()
                
            continue
        
        # if ctrl+c is pressed, exit
        if k == '\x03':
            raise KeyboardInterrupt

        # if ctrl+z is pressed, exit
        if k == '\x1a':
            raise EOFError
    
        # if ctrl+d is pressed, exit
        if k == '\x04':
            raise EOFError
    
        # if backspace is pressed, remove last character
        #if k == '\x7f':
        #    backspace()
        #    continue
        
        elif k == '\n' or k == '\r' or ord(k) == 13:
            execute(command)
            print("[ABot]>>> ", end="", flush=True)
            command = ""
            command_pos = 0
            cursor_pos = 0
            continue
        
        # test if control 
        #elif k == ';':
        #    if inkey() == '5': # + arrow is pressed
        #        pass
        
        elif k.isprintable():
            # insert char k to command at cursor_pos and move cursor right
            command = command[:cursor_pos] + k + command[cursor_pos:]
            
            
            # replace the command in the command line
            print("\033[2K", end="\r")
            print("[ABot]>>> ", end="")
            print(command, end="")
            
            cursor_pos += 1
            
            # move the cursor back to the correct position
            print("\033[D" * len(command[cursor_pos:]), end="", flush=True)
            
            
            
            
            
            
            
    
    except (KeyboardInterrupt, EOFError):
        print("\n[ABot]>>> Exiting...")
        break
    