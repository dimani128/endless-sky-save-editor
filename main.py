# endless-sky-save-editor/main.py

# TODO
# Add commands
#   del [number]
#   add [number] [value]
#   copy [number]
#   paste [number]

# BUG(s)
# No known bugs right now

try:    # main try statement for handling:
        #   - SystemExit
        #   - KeyboardInterrupt
        #   - Other unhandled exceptions

    from tkinter import filedialog as tkfd
    from tkinter import messagebox as tkmsg
    
    from errors import EmptyStringError, InvalidFilenameError

    # Unnescesarry b/c all refrences have import beforehand. Saves loading time.
    # import sys # for sys.exit() and getting stacktrace

    def full_stack(): # returns last stacktrace (error)
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

    # Python program to to edit Enless Sky (https://endless-sky.github.io/) save files

    VERSION = "0.2.5"         # Version
    VERSION_CHANGELOG = '''
    Changed file select to tk.filedialogue.
    Added clear command.
    '''                     # Changes in this version

    from termcolor import colored   # For colored text
    import colorama as color        # For colored text
    color.init()                    # Initialize colorama

    import os                       # File operations

    def cls():
        """Clears the console."""
        os.system('cls' if os.name=='nt' else 'clear')

    from pathlib import Path        # Checking if path is valid

    def splitByIndentation(data: str):
        '''Splits a multi-line string into groups of indented blocks (\t or quadruple-space)'''
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
        '''Prints the help message and version changelog'''
        
        helpMessage = f'''
Endless Sky Save Editor v{VERSION}:
    Version changes:
        {VERSION_CHANGELOG}
    Help
        On entry, a prompt will apear to enter the file path to the save you wish to edit.
        Enter the path to the save file you wish to edit.
            (save files are located in C:\\Users\\[YOUR USERNAME]\\AppData\\Roaming\\endless-sky\\saves)
        The program will print out a list of all the properties of the save file in the format of '{color.Fore.GREEN}[0]{color.Fore.WHITE} collapsed outfitter'
        Then the program will ask for a command.
            This will be the number in green.
        After you enter the number, the program will print a more detailed version of the element in the format of '{color.Fore.GREEN}[1]{color.Fore.WHITE}     Ammunition'
        Then the program will ask for the sub-element you want to edit.
            This will be the number in green.
        The program will ask for the new value, while providing the old one, eg: '{color.Fore.GREEN}[1]{color.Fore.WHITE} Previously: Ammunition. Enter new value (leave blank to cancel): '
        You can repeat changing values untill you wish to save.
            To save, enter 'save'.
'''
        print(helpMessage)

    index = 0
    subItemIndex = 0
    changed = False

    def printAvailableItems():
        '''Prints list of items in the opened save file.'''
        global index
        index = 0
        for item in items:
            if type(item) == list:
                print(colored(f"[{index}]", 'green'), item[0].replace('\\t', '\t').replace('"', ''))
            elif type(item) == str:
                print(colored(f"[{index}]", 'green'), item.replace('\\t', '\t').replace('"', ''))

            index += 1

    def printSelectedItem(index:int):
        '''Prints details about the selected item.'''
        try:
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
        except TypeError:
            pass

    trying = True
    while trying:   # Loops untill response is 'exit' or a valid filepath
        # filename = input("File path to save file (check in %appdata%\\endless-sky\\saves): ") # Asks runner for file to open
        filename = tkfd.askopenfilename(initialdir = os.environ["appdata"] + '\\endless-sky\\saves', title= "Please select a file:", filetypes=(('Endless Sky Save Files', '*.txt'),('All files', '*.*'),))

        filename = filename.strip('"\'') # remove quotes on ends (file explorer 'copy as path' adds double quotes to ends)

        if not filename: # check if path is blank
            continue
        elif filename.lower().strip() == 'exit': # check if path is 'exit'
                    quit()
        elif filename.lower().strip() == '?' or filename.lower().strip() == 'help': # check if path is 'help' or '?'
            printHelpMessage()
            continue

        try:
            try: # check if path is valid
                Path(filename).resolve()
            except (OSError, RuntimeError):
                raise InvalidFilenameError()
            with open(filename, 'r') as f: # open the file
                try:
                    if not filename.lower().strip().endswith(".txt"): # check if ends in .txt
                        print(colored(f"{filename} does not end with the Endless Sky save file format (.txt). \n\tAre you sure you want to continue (y/n)? ", 'yellow'), end='')
                        confirm = input('')
                        confirm = confirm.strip().lower()
                        if confirm == 'y' or confirm == 'yes':
                            pass
                        else:
                            continue
                    items = splitByIndentation(f.read()) # split the file by indentation
                except (IndexError, UnicodeDecodeError): # IndexError: Empty file, UnicodeDecodeError: Non-text file
                    print(colored(f"The file '{filename}' is not a valid Endless Sky save file. Please choose a valid Endless Sky save file.", 'red'))
                    continue
                trying = False
        except FileNotFoundError: # File doesn't exist
            print(color.Fore.YELLOW + f"The file {filename} was not found.\n Check you spelling and see if the file exists." + color.Fore.WHITE)
        except InvalidFilenameError: # Invalid filename
            print(colored('Invalid filename.', 'red'))
        except OSError as e: # OSerror: could be many things
            try:
                if "Invalid argument:" in str(e): # Check if error is 'OSError: [Errno 22] Invalid argument: ...'
                    raise InvalidFilenameError()  # Means that the filename provided has forbidden characters
                else:
                    raise e                       # Re-raise OSError
            except InvalidFilenameError: # Invalid filename
                print(colored('Invalid filename.', 'red'))
            

    while True: # Item edit loop
        command = False
        trying = True

        while trying:
            try:
                printAvailableItems()                # print save file items
                if not command:
                    itemIndex = input("Enter an command or an id of an item:\n\t('save' to save, 'exit' to exit, 'clear' to clear the screen, or '?' or 'help' to print help text): ")
                                                        # /\ /\ get an item to edit
                    itemIndex = int(itemIndex)          # and convert to int
                    
                prevItemIndex = itemIndex

                trying = False # If there are no errors, continue

                command = False
                
                printSelectedItem(itemIndex) # Print details about the selected item
                itemToEdit = items[itemIndex]
                
                trying = True

                while trying:
                    subItemIndex = input("Enter a sub-item to edit: ") # Ask user for sub-item to edit

                    if not subItemIndex:
                        continue

                    subItemIndex_ = int(subItemIndex)
                
                    oldVal = itemToEdit[subItemIndex_]

                    # Ask for new value
                    print(colored(f'[{subItemIndex_}]', 'green'), end='')
                    oldValFormmatted = oldVal.replace('\t', '', 1)
                    newVal = "\t" + input(f'Previously: {oldValFormmatted}. Enter new value (leave blank to cancel): ')
                    if newVal: # check if not blank
                        items[itemIndex][subItemIndex_] = newVal # set new value
                        changed = True # mark as changed
                    
                    trying = False
                
            except (ValueError, IndexError): # input is not integer or is not inside item bounds
                try:
                    if itemIndex.lower().strip() == 'save': # check if input is 'save'
                        savedFile = ""
                        for item in items:
                            # append each element to the save file
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
                            # get save path
                            saveFilename = input("File path to save in (press enter without entering any path to use the same path): ")
                            saveFilename = saveFilename.strip("\"' ")
                            try:
                                if saveFilename == '':
                                    saveFilename = filename
                                
                                try:
                                    with open(saveFilename, 'w') as f: # if succeeds, file already exists
                                        # confirm override
                                        print(color.Fore.YELLOW + f"{os.path.basename(saveFilename)} already exists. Are you sure you want to overwrite it (y/n)? " + color.Fore.WHITE)
                                        end = input('')
                                        end = end.strip().lower()
                                        if end == 'y' or end == 'yes':
                                            f.write(savedFile)
                                            trying = False
                                except FileNotFoundError: # file doesn't exist
                                    with open(saveFilename, 'x') as f: # create and write to new file
                                        f.write(savedFile)
                                        trying = False
                            except EmptyStringError:
                                print("You must enter a value.")

                        # quit()
                        changed = False

                    elif itemIndex.lower().strip() == 'exit': # check if input is 'exit'
                        if changed: # user has made changes
                            # confirm exit without save
                            print(colored(f"You have made unsaved changes. \n\tAre you sure you want to exit (y/n)? ", 'yellow'), end='')
                            confirm = input('')
                            confirm = confirm.strip().lower()
                            if confirm == 'y' or confirm == 'yes':
                                quit()
                            else:
                                continue
                        else:
                            quit()

                    elif itemIndex.lower().strip() == 'clear': # check if input is 'exit'
                        cls()
                        continue

                    elif itemIndex.lower().strip().startswith('edit'): # check if input is 'edit'
                        command = True
                        itemIndex = itemIndex.lower().replace('edit', '').strip()
                        try:
                            itemIndex = int(itemIndex)
                        except ValueError:
                            print(colored('Usage: edit [number of item to edit]', 'red'))
                        continue

                    elif itemIndex.lower().strip() == '?' or itemIndex.lower().strip() == 'help': # check if input is 'help' or '?'
                        printHelpMessage()
                        continue

                    elif itemIndex.lower().strip().startswith('del') or itemIndex.lower().strip().startswith('delete'): # check if input is 'delete' or 'del'
                        try:
                            del items[int(itemIndex.replace('del ', '').replace('delete ', ''))]
                        except IndexError:
                            print(colored('Invalid item number', 'red'))
                    
                        changed = True
                        continue


                except AttributeError:
                    try:
                        if subItemIndex.lower().strip() == 'save': # check if input is 'save'
                            savedFile = ""
                            for item in items:
                                # append each element to the save file
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
                                # get save path
                                filename = input("File path to save in: ")
                                filename = filename.strip()
                                try:
                                    if filename == '':
                                        raise EmptyStringError
                                    else:
                                        try:
                                            with open(filename, 'w') as f: # if succeeds, file already exists
                                                # confirm override
                                                print(color.Fore.YELLOW + f"{os.path.basename(filename)} already exists. Are you sure you want to overwrite it (y/n)? " + color.Fore.WHITE)
                                                end = input('')
                                                end = end.strip().lower()
                                                if end == 'y' or end == 'yes':
                                                    f.write(savedFile)
                                                    trying = False
                                        except FileNotFoundError: # file doesn't exist
                                            with open(filename, 'x') as f: # create and write to new file
                                                f.write(savedFile)
                                                trying = False
                                except EmptyStringError:
                                    print("You must enter a value.")

                            # quit()
                            changed = False

                        elif subItemIndex.lower().strip() == 'exit': # check if input is 'exit'
                            if changed: # user has made changes
                                # confirm exit without save
                                print(colored(f"You have made unsaved changes. \n\tAre you sure you want to exit (y/n)? ", 'yellow'), end='')
                                confirm = input('')
                                confirm = confirm.strip().lower()
                                if confirm == 'y' or confirm == 'yes':
                                    quit()
                                else:
                                    continue
                            else:
                                quit()

                        elif subItemIndex.lower().strip() == '?' or subItemIndex.lower().strip() == 'help': # check if input is 'help' or '?'
                            printHelpMessage()
                            continue
                        elif subItemIndex.lower().strip().startswith('del') or subItemIndex.lower().strip().startswith('delete'): # check if input is 'delete' or 'del'
                            # print('hello')
                            try:
                                del items[prevItemIndex][int(subItemIndex.replace('del ', '').replace('delete ', ''))]
                            except IndexError:
                                print(colored('Invalid item number', 'red'))
                            except BaseException as e: # unhandled error
                                print(color.Fore.RED + f"\n\nFATAL ERROR DETECTED!\n Please report this error to https://github.com/newDan1/endless-sky-save-editor/issues:\n{full_stack()}\n\n")
                                quit()

                            changed = True
                            
                            continue

                    except AttributeError:
                        pass

                # itemIndex = int(input("Enter a valid indeger of an item to edit: "))
                print(colored(f'Invalid item: {itemIndex}.'), 'red')
            # except TypeError:
            #     print(colored('Invalid command.', 'red'))

except KeyboardInterrupt: # ctrl + c
    try: # confirm exit
        from termcolor import colored
        import colorama as color
        color.reinit()
        print(f'\n{color.Fore.RED}Are you sure you want to quit (y/n)? {color.Fore.WHITE}', end='')
        end = input('')
        end = end.strip().lower()
        if end == 'y' or end == 'yes':
            quit()
        # else:
        #     pass
    except KeyboardInterrupt as e: # ctrl + c when confirming exit
        quit()
    except SystemExit as e: # raised by quit()
        import sys
        sys.exit(e) # exits silently
    except BaseException as e: # unhandled error
        print(color.Fore.RED + f"\n\nFATAL ERROR DETECTED!\n Please report this error to https://github.com/newDan1/endless-sky-save-editor/issues:\n{full_stack()}\n\n")
        quit()
except SystemExit as e: # raised by quit()
    import sys
    sys.exit(e) # exits silently
except BaseException as e: # unhandled error
    print(color.Fore.RED + f"\n\nFATAL ERROR DETECTED!\n Please report this error to https://github.com/newDan1/endless-sky-save-editor/issues:\n{full_stack()}\n\n")
    quit()