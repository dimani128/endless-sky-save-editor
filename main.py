

# TODO
# Add comments to explain code

# BUG(s)
# Some colored text is broken:
#   quit message
#   edit sub-item

from msilib.schema import File


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

    from termcolor import colored
    import colorama as color
    color.init()

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
        try:
            with open(filename, 'r') as f:
                items = splitByIndentation(f.read())
                printAvailableItems()
                trying = False
        except FileNotFoundError:
            print(color.Fore.YELLOW + f"The file {filename} was not found.\n Check you spelling and see if the file exists." + color.Fore.WHITE)

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
                                savedFile += item
                        elif type(item) == str:
                            savedFile += item

                # itemIndex = int(input("Enter a valid indeger of an item to edit: "))
                print('Invalid item.')

except KeyboardInterrupt:
    from termcolor import colored
    import colorama as color
    color.reinit()
    print()
    end = input(color.Fore.RED + "Are you sure you want to quit (y/n)? " + color.Fore.WHITE)
    end = end.strip().lower()
    if end == 'y' or end == 'yes':
        exit(0)
    # else:
    #     pass
except BaseException as e:
    print(color.Fore.RED + f"FATAL ERROR DETECTED!\n Please report this error to https://github.com/newDan1/endless-sky-save-editor/issues:\n{full_stack()}")
    exit()