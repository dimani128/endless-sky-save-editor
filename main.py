

# TODO
# Add comments to explain code

# BUG(s)
# Some colored text is broken:
#   quit message
#   edit sub-item


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

    filename = input("File path to save file (check in %appdata%/roaming/endless-sky/saves): ")
    with open(filename, 'r') as f:
        items = splitByIndentation(f.read())
        printAvailableItems()

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
                
                # itemIndex = int(input("Enter a valid indeger of an item to edit: "))
                print('Invalid item.')

except KeyboardInterrupt:
    from termcolor import colored
    import colorama as color
    color.init()
    print()
    end = input(colored("Are you sure you want to quit (y/n)? ", 'red'))
    end = end.strip().lower()
    if end == 'y' or end == 'yes':
        exit(0)
    # else:
    #     pass