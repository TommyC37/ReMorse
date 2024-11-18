'''
DEV NOTES:
- Functions that should be accessible to users must begin with `cmd_` per the dynamically constructed `commands` dictionary
- BEWARE of creating functions that start with `cmd_` as it could potentially expose harmful functionality to end users
'''

import inspect
import encoder
import random
import curses

RED = "\033[91m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RESET = "\033[0m"

def cmd_help():
    # Get command functions
    functions = [
        name[4:] for name, obj in globals().items()
        if inspect.isfunction(obj) and name.startswith('cmd_')
    ]

    # Display command functions
    response = '\nHere is a list of available commands:\n'
    for i, f in enumerate(functions): response += (f'{i + 1}. {f.replace("_", " ").capitalize()}\n')
    print(response)

    return

def cmd_train():
    training = True
    alphabet = [chr(i) for i in range(65, 91)]
    while training:
        # Display welcome message and instructions
        encoder.type_text("Welcome to Training Mode.\n\nType 'quit' to quit")
        print('\n\n')

        while alphabet:
            testing = True
            test = alphabet.pop(alphabet.index(random.choice(alphabet)))
            
            while testing:
                print(encoder.encode_text(test))
                raw_input = input("Translate the character: ").strip().lower()
                if raw_input.lower() == 'quit':
                    testing = False
                    training = False
                    print_logo()
                    return
                elif raw_input == test.lower():
                    print(GREEN + 'Correct!' + RESET, flush=True)
                    testing = False
                else:
                    print(RED + 'WRONG!' + RESET, flush=True)
        if not alphabet:
            print('\n' + GREEN + 'Congratulations!' + RESET)
            training = False
            
            print_logo()
            return
                     
def cmd_quit():
    print('Goodbye!')
    return 'quit'

# Dynamically build dictionary of commands by retrieving all functions starting with `cmd_` in the global symbol table
commands = {
    name[4:]: func
    for name, func in globals().items()
    if inspect.isfunction(func) and name.startswith("cmd_")
}   

def print_logo():
    read_logo_name_file = open("data\\eager-gest-name.txt", "r")
    print(read_logo_name_file.read())
    print("\nWelcome to Eager Gest's ReMorse!\n\nType 'help' to see a list of commands.\n")

def game():
    running = True
    # Display logo and welcome message
    print_logo()

    # Game loop
    while running:
        result = ''
        # Get input from the user
        raw_input = input("Enter a command: ").strip().lower()
        parsed_input = raw_input.split(" ")

        # Check for quit condition
        if parsed_input[0] in commands:
            if len(parsed_input) > 1:
                print(len(parsed_input[1:]))
                try:
                    result = commands[parsed_input[0]](parsed_input[1:])
                except IndexError as e:
                    print(f'\nAn error occurred: {e}')
                    print('Commands with spaces treat each word after the first as distinct parameter.')
                    print('\nTry executing that command with fewer parameters.')
                except TypeError as e:
                    if "takes 0" in e:
                        print(f'\nAn error occurred: {e}')
                        print('Commands with spaces treat each word after the first as distinct parameter.')
                        print('\nTry executing that command with ZERO parameters (just type the first word!).')
                    else:
                        print('test')
            else:
                try:
                    result = commands[parsed_input[0]]()
                except IndexError as e:
                    print(e)
        else:
            print("Unknown command. Try typing 'help' for more options.")
        if result and result == 'quit':
                        running = False

# Start the game

game()