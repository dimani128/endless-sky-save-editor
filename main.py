

# TODO
# Add comments to explain code
# Add commands
#   del [number]
#   add [number] [value]
#   copy [number]
#   paste [number]
#   edit [number]

# BUG(s)
# Some colored text is broken:
#   quit message
#   edit sub-item

from errors import EmptyStringError, InvalidFilenameError

import sys

def full_stack():
        import traceback, sys
        exc = sys.exc_info()[0]
        stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
        if exc is not None:  # i.e. an exception is present
            del stack[-1]       # remove call of full_stack, the printed exception
                                # will contain the caught exception caller instead
        trc = 'Traceback (most recent call last):\n'
        stackstr = trc + ''.join(traceback.format_list(stack))
        if exc is not None:
            stackstr += '  ' + traceback.format_exc().lstrip(trc)
        return stackstr

try:
    # Python program to (hopefully) create a Enless Sky (https://endless-sky.github.io/) Save Editor

    VERSION = "0.1"
    VERSION_CHANGELOG = '''
        Added help message.
        Added more error handling.
    '''

    from termcolor import colored
    import colorama as color
    color.init()

    import os
    from pathlib import Path

    def splitByIndentation(data: str):
        indented = False
        prevLine = ''
        currentBlock = []
        output = []

        for line in data.split('\n'):
            if line.startswith('\t') or line.startswith('    '):
                if not indented:
                    currentBlock = [prevLine]
                    indented = True

                currentBlock.append(line)
            else:
                if indented:
                    output.append(currentBlock)
                indented = False
            prevLine = line
        output.append(currentBlock)
        return output

    def printHelpMessage():
        
        helpMessage = f'''
Endless Sky Save Editor v{VERSION}:
    Version changes:
        {VERSION_CHANGELOG}
    Help
        On entry, a prompt will apear to enter the file path to the save you wish to edit.
        Enter the path to the save file you wish to edit.
            (save files are located in C:\\Users\\[YOUR USERNAME]\\AppData\\Roaming\\endless-sky\\saves)
        The program will print out a list of all the properties of the save file in the format of '{color.Fore.GREEN}[0]{color.Fore.WHITE} collapsed outfitter'
        Then the program will ask for the element you want to edit.
            This will be the number in green.
        After you enter the number, the program will print a more detailed version of the element in the format of '{color.Fore.GREEN}[1]{color.Fore.WHITE}     Ammunition'
        Then the program will ask for the sub-element you want to edit.
            This will be the number in green.
        The program will ask for the new value, while providing the old one, eg: '{color.Fore.GREEN}[1]{color.Fore.WHITE} Previously: Ammunition. Enter new value (leave blank to cancel): '
        You can repeat changing values untill you wish to save.
            To save, 
'''
        print(helpMessage)

    index = 0

    def printAvailableItems():
        global index
        for item in items:
            if type(item) == list:
                print(colored(f"[{index}]", 'green'), item[0].replace('\\t', '\t').replace('"', ''))
            elif type(item) == str:
                print(colored(f"[{index}]", 'green'), item.replace('\\t', '\t').replace('"', ''))

            index += 1

    def printSelectedItem(index:int):
        index1 = 0
        item = items[index]
        if type(item) == list:
            for item_ in item:
                if type(item_) == list:
                    print(colored(f"[{index1}]", 'green'), item_[index1].replace('\\t', '\t').replace('"', ''))
                elif type(item_) == str:
                    print(colored(f"[{index1}]", 'green'), item_.replace('\\t', '\t').replace('"', ''))
                index1 += 1
        elif type(item) == str:
            print(colored(f"[{index}]", 'green'), item.replace('\\t', '\t').replace('"', ''))
    
    trying = True
    while trying:
        filename = input("File path to save file (check in %appdata%/roaming/endless-sky/saves): ")
        if not filename:
            continue
        elif filename.lower().strip() == 'exit':
                    quit()
        elif filename.lower().strip() == '?' or filename.lower().strip() == 'help':
            printHelpMessage()
            continue

        try:
            try:
                Path(filename).resolve()
            except (OSError, RuntimeError):
                raise InvalidFilenameError()
            with open(filename, 'r') as f:
                items = splitByIndentation(f.read())
                printAvailableItems()
                trying = False
        except FileNotFoundError:
            print(color.Fore.YELLOW + f"The file {filename} was not found.\n Check you spelling and see if the file exists." + color.Fore.WHITE)
        except InvalidFilenameError:
            print('Invalid filename.')
        except OSError as e:
            try:
                if "Invalid argument:" in str(e):
                    raise InvalidFilenameError()
                else:
                    raise e
            except InvalidFilenameError:
                print('Invalid filename.')
            

    while True:
        trying = True
        while trying:
            try:
                itemIndex = input("Enter an item to edit ('save' to save and exit): ")
                itemIndex = int(itemIndex)
                trying = False
                printSelectedItem(itemIndex)

                itemToEdit = items[itemIndex]

                subItemIndex = int(input("Enter a sub-item to edit: "))
                
                oldVal = itemToEdit[subItemIndex]
                items[itemIndex][subItemIndex] = "\t" + input(colored(f'[{subItemIndex}]', 'green') + f'Previously: {oldVal.strip()}. Enter new value (leave blank to cancel): ').strip()
                
            except (ValueError, IndexError):
                if itemIndex.lower().strip() == 'save':
                    savedFile = ""
                    for item in items:
                        if type(item) == list:
                            for item_ in item:
                                savedFile += item_
                                savedFile += '\n'

                        elif type(item) == str:
                            savedFile += item

                        savedFile += '\n'
                    
                    # print('\n\n\n' + savedFile)

                    trying = True
                    while trying:
                        filename = input("File path to save in: ")
                        filename = filename.strip()
                        try:
                            if filename == '':
                                raise EmptyStringError
                            else:
                                try:
                                    with open(filename, 'w') as f:
                                        end = input(color.Fore.YELLOW + f"{os.path.basename(filename)} already exists. Are you sure you want to overwrite it (y/n)? " + color.Fore.WHITE)
                                        end = end.strip().lower()
                                        if end == 'y' or end == 'yes':
                                            f.write(savedFile)
                                            trying = False
                                except FileNotFoundError:
                                    with open(filename, 'x') as f:
                                        f.write(savedFile)
                                        trying = False
                        except EmptyStringError:
                            print("You must enter a value.")

                    quit()

                elif itemIndex.lower().strip() == 'exit':
                    quit()

                elif itemIndex.lower().strip() == '?' or itemIndex.lower().strip() == 'help':
                    printHelpMessage()
                    continue

                # itemIndex = int(input("Enter a valid indeger of an item to edit: "))
                print('Invalid item.')

except KeyboardInterrupt:
    try:
        from termcolor import colored
        import colorama as color
        color.reinit()
        print()
        end = input(f"{color.Fore.RED}Are you sure you want to quit (y/n)? {color.Fore.WHITE}")
        end = end.strip().lower()
        if end == 'y' or end == 'yes':
            quit()
        # else:
        #     pass
    except KeyboardInterrupt as e:
        quit()
    except BaseException as e:
        print(color.Fore.RED + f"\n\nFATAL ERROR DETECTED!\n Please report this error to https://github.com/newDan1/endless-sky-save-editor/issues:\n{full_stack()}\n\n")
        quit()
except SystemExit as e:
    sys.exit(e)
except BaseException as e:
    print(color.Fore.RED + f"\n\nFATAL ERROR DETECTED!\n Please report this error to https://github.com/newDan1/endless-sky-save-editor/issues:\n{full_stack()}\n\n")
    quit()