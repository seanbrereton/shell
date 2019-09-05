#!/usr/bin/python3

import os
import subprocess
import sys
from cmd import Cmd

class MyShell(Cmd):

    def default(self, args):
        #any other command line input is passed to this function
        tokens = args.split()
        try:
            #loop checking if output redirection is needed
            for i in range(0, len(tokens) + 1):
                if tokens[i] == '>':
                    #tries to run command as a background process using Popen
                    #overwrites output to given file and breaks
                    try:
                        with open(tokens[i+1], 'w') as f:
                            subprocess.Popen(tokens[:i], stdout=f)
                        break
                    except:
                        print('Error: No file given')
                        break

                elif tokens[i] == '>>':
                    #tries to run command as a background process using Popen
                    #appends output to given file and breaks
                    try:
                        with open(tokens[i+1], 'a') as f:
                            subprocess.Popen(tokens[:i], stdout=f)
                        break
                    except:
                        print('Error: No file given')
                        break
        except IndexError:
            #if no output redirection is needed, args is checked for an '&'
            try:
                #tries to run command as a background process
                if tokens[-1] == '&':
                    subprocess.Popen(tokens[:-1])
                #runs the command normally
                else:
                    subprocess.run(tokens)
            except:
                #Invalid command
                print(f'Invalid command: command "{args}" not found!')

    def do_cd(self, args):
        #Changes current directory to the directory passed as an argument
        try:
            if args == "":
                #If no arguments are given the current working directory is returned
                print("The CWD is: " + os.getcwd())
            else:
                #try to change directory to the directory passed in as an argument
                os.chdir(args)
                prompt.prompt = user + "@myshell~" + os.getcwd() + "> "
        except:
            #os.chdir() fails if an invalid directory is passed.
            print("This directory does not exist!")

    def do_clr(self, args):
        #Calls the unix command clear
        os.system("clear")

    def do_dir(self, args):
        #Lists files in a given directory
        tokens = args.split()
        try:
            #os.listdir creates a list of the directory(tokens[0]) and joins them with newline characters
            files = os.listdir(tokens[0])
            output = '\n'.join(files)
            if tokens[1] == '>':
                #Tries to overwrite output to the given file tokens[2]
                #If no file is given it will error
                try:
                    overwrite_file(tokens[2], output)
                except:
                    print('Error: No file given')
            elif tokens[1] == '>>':
                #Tries to append output to the file tokens[2]
                try:
                    add_file(tokens[2], output)
                except:
                    print('Error no file given')
        except:
            #No I/O redirection is needed
            #Tries to print files to the terminal screen
            try:
                files = os.listdir(args)
                output = '\n'.join(files)
                print(output)
            except:
                #Fails if args is not a valid directory
                print('Invalid directory')

    def do_environ(self, args):
        #Lists all the environment strings
        tokens = args.split()
        #os.environ gets all the environment strings as a dictionary
        env = os.environ
        env_list = []
        #Appends keys and values to a list
        for k, v in env.items():
            env_list.append(k + ' = ' + v)
        try:
            if tokens[0] == '>':
                #Tries to overwrite if the file tokens[1] is given.
                #If no file is given the try gives an IndexError
                try:
                    overwrite_file(tokens[1], '\n'.join(env_list))
                except:
                    print('Error: No file given')
            elif tokens[0] == '>>':
                #Tries to append to the file.
                try:
                    add_file(tokens[1], '\n'.join(env_list))
                except:
                    print('Error: No file given')
        except IndexError:
            #if no args given display environment strings on the screen
            print('\n'.join(env_list))

    def do_echo(self,args):
        #prints args as a string
        tokens = args.split()
        try:
            #loops through args to see if output redirection is needed
            for i in range(0, len(tokens) + 1):
                if tokens[i] == '>':
                    #tries overwite and breaks the loop
                    try:
                        overwrite_file(tokens[i+1], ' '.join(tokens[:i]))
                        break
                    except:
                        print('Error: No file given')
                        break

                elif tokens[i] == '>>':
                    #tries append and breaks the loop
                    try:
                        add_file(tokens[i+1], ' '.join(tokens[:i]))
                        break
                    except:
                        print('Error: No file given')
                        break
        except IndexError:
            #if no output redirection is needed, print args to terminal screen
            print(args)

    def do_help(self, args):
        #Dictionary with description of all commands
        cmd_help = {
            'cd': 'Usage: cd <directory>. Changes the current default directory to <directory>. If no argument is given it reports the current directory',
            'clr': 'Clears the terminal screen.',
            'dir': 'Usage: dir <directory>. Lists contents of <directory>',
            'environ': 'Lists all the environment strings',
            'echo': 'Usage: echo <comment>. Returns a string of the argument given.',
            'help': 'Shows usage of a given command.',
            'pause': 'Pauses the shell untin the "Enter" key is pressed.',
            'quit': 'This exits the shell.',
            }

        tokens = args.split()
        try:
            #appends dictionary items to list
            help_list = []
            for k, v in cmd_help.items():
                help_list.append(k + ' : ' + v)

            if args == '':
                #If no arguments are given the manual is displayed 20 lines at a time
                x = 0
                y = 20
                #opens manual and stores contents as a list in output
                with open('readme', 'r') as f:
                    output = f.readlines()
                #while there is still output, displays 20 lines at a time and waits for enter to be pressed
                while x < len(output):
                    print(' '.join(output[x:y]))
                    x += 20
                    y += 20
                    input('Press enter to display more.... ')

            elif tokens[0] == '>':
                #tries to overwrite help list to a given file
                try:
                    overwrite_file(tokens[1], '\n'.join(help_list))
                except:
                    print('No file given')
            elif tokens[0] == '>>':
                #tries to append help list to a given file
                try:
                    add_file(tokens[1], '\n'.join(help_list))
                except:
                    print('No file given')
            else:
                #If a specific command is given e.g echo , help for that command is given
                print(cmd_help[args])
        except KeyError:
            #If command is not found
            print(f'No help for {args}. ')

    def do_pause(self,args):
        #The shell waits for input to accept the enter key
        input("Press 'Enter' to continue... ")

    def do_quit(self, args):
        #raises SystemExit to exit the shell
        print("Quitting...")
        raise SystemExit

def overwrite_file(filename, output):
    #Used for overwriting files for '>' output redirection
    #'w' deletes any existing text in a file before writing to it
    with open(filename, 'w') as f:
        f.write(output + '\n')
        f.close()

def add_file(filename, output):
    #Used for appending to files in '>>' output redirection
    #'a' keeps any existing text and adds to it
    with open(filename, 'a') as f:
        f.write(output + '\n')
        f.close()

if __name__ == '__main__':
    #try / except to check for batchfile in command line input
    try:
        #try open batchfile
        with open(sys.argv[1], 'r') as f:
            prompt = MyShell()
            #reads in commands from file and adds a quit command to the end
            commands = f.readlines()
            commands.append('quit' + '\n')
            #Adds commands to the command queue and starts the shell
            prompt.cmdqueue = commands
            prompt.cmdloop()
    except IndexError:
        #If no batchfile is given commandline prompt is set up
        prompt = MyShell()
        #Command line prompt displays username and current working directory
        user = os.environ.get("USERNAME")
        prompt.prompt = user + "@myshell~" + os.getcwd() + "> "
        #Shell is started and waits for input
        prompt.cmdloop("Starting shell...")
