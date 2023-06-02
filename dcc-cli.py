#!/usr/bin/env python
"""A simple cmd2 application."""
import cmd2
from cmd2 import with_argument_list
import argparse
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich import print
from rich.markdown import Markdown
import json
import re
import random
from datetime import datetime

console = Console()

# Path to the JSON file
SYSTEM_TABLES_FILE_PATH = "system/dcc/tables.json"
# File path for the ASCII art
ASCII_ART_FILE = "system/dcc/ascii_art.txt"

# Load ASCII art from file
def load_ascii_art():
    with open(ASCII_ART_FILE, "r") as file:
        ascii_art = file.read()
    return ascii_art
def display_welcome():
    print(" ")
    print("[black on violet] +++++++++++++++++++++++++++++++++++++++++++++ [/black on violet]")
    print("[black on violet] Welcome the DCC Quickstart Command Line Tool! [/black on violet]")
    print("[black on violet] +++++++++++++++++++++++++++++++++++++++++++++ [/black on violet]")
    print(" ")
    print("Some commands write to a text file in the current folder.")
    print("type 'tail -f dcc-log.md' in another terminal window to follow it.")
def display_instructions():
    """Display the initial instructions with available commands."""
    print(" ")
    print("Available commands: [yellow]help[/yellow], [red]table[/red], [violet]roll[/violet], [blue]rolltable[/blue], [green]zero[/green], [yellow]headline[/yellow], [red]timestamp[/red], [violet]note[/violet], [blue]quit[/blue]")
    print(" ")

class FirstApp(cmd2.Cmd):
    def __init__(self):
        # self.debug = True
        # shortcuts = cmd2.DEFAULT_SHORTCUTS
        # shortcuts.update({'&': 'roll'})
        # # shortcuts.update({'t': 'tables'})
        super().__init__()
        self.prompt = ":>>>"
        # self.prompt = u'\u2713'

        # Make maxrepeats settable at runtime
        # self.maxrepeats = 3
        # self.add_settable(cmd2.Settable('maxrepeats', int, 'max repetitions for speak command', self))
        ascii_art = load_ascii_art()
        # print(ascii_art)
        text = Text(ascii_art)
        text.stylize("yellow")
        console.print(text)
        display_welcome()
        display_instructions()

    """A simple cmd2 application."""
    roll_parser = cmd2.Cmd2ArgumentParser()
    # roll_parser.add_argument('-p', '--piglatin', action='store_true', help='atinLay')
    # roll_parser.add_argument('-s', '--shout', action='store_true', help='N00B EMULATION MODE')
    # roll_parser.add_argument('-r', '--repeat', type=int, help='output [n] times')
    roll_parser.add_argument('dice', nargs='+', help='Dice to roll (e.g. 3d6)')
    @cmd2.with_argparser(roll_parser)
    def do_roll(self, args):
        """Rolls the dice you enter (3d6)."""
        # takes in a a list of rolls like: d20 3d6 1d4
        total = 0
        with open('dcc-log.md', 'a') as f:
            f.write('\n')
            for dieroll in args.dice: # loops through each argument
                roll = roll_multiple(dieroll) # sends the roll to roll_multiple()
                # making a definition list in rolls of the dice the put in and the rolled value
                total += roll # adds to the total
                print(f"[yellow]{dieroll}:[/yellow][yellow][/yellow]\t[red]{roll}[/red]") # prints roll
                f.write(f"{dieroll}:\t{roll}\n") # prints roll
            if len(args.dice) > 1:
                print(f"Total\t{total}") #prints total
                f.write(f"Total\t{total}\n") #prints total
        # self.poutput(' '.join(rolls))

    headline_content = cmd2.Cmd2ArgumentParser()
    headline_content.add_argument('headline', nargs='+', help='Headline to add to log')
    @cmd2.with_argparser(headline_content)
    def do_headline(self, args):
        """Text 'in quotes' written after the command will be a headline in the log file."""
        print(f"[bold]{args.headline[0]}[/bold]")
        with open('dcc-log.md', 'a') as f:
            f.write('\n')
            f.write(f"# {args.headline[0]}\n")

    time = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(time)
    def do_time(self, args):
        """Add a time stamp to the log file."""
        print(f"[bold blue]{datetime.now().strftime('%d %B, %Y (%H:%M)')}[/bold blue]   ")
        with open('dcc-log.md', 'a') as f:
            f.write('\n')
            f.write(f"**{datetime.now().strftime('%d %B, %Y (%H:%M)')}**  ")

    note_content = cmd2.Cmd2ArgumentParser()
    note_content.add_argument('note', nargs='+', help='Note to add to log')
    @cmd2.with_argparser(note_content)
    def do_note(self, args):
        """Text 'in quotes' written after the command will be a paragraph in the log file."""
        print(f"{args.note[0]}") #prints note
        with open('dcc-log.md', 'a') as f:
            f.write('\n')
            f.write(f"{args.note[0]}   \n")

    zero = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(zero)
    def do_zero(self, args):
        """Generate zero levels"""
        tables = load_tables()
        char = {}
        occupation_data = []
        roll = random.randint(1, 100)
        # find 'roll' in ranges of rows
        for i in range(1, len(tables['Table 1-3: Occupation']['table'])):
            if '-' in tables['Table 1-3: Occupation']['table'][i][0]:
                numbers = tables['Table 1-3: Occupation']['table'][i][0].split('-')
                if roll in range(int(numbers[0]),int(numbers[1])+1):
                    occupation_data = tables['Table 1-3: Occupation']['table'][i]
                    break
            elif int(tables['Table 1-3: Occupation']['table'][i][0]) == roll:
                occupation_data = tables['Table 1-3: Occupation']['table'][i]
                break
        # types of farmers/carts
        if roll in range(39,48):
            occupation_data[3] = occupation_data[3].strip('*')
            farmers = ['Potato','Wheat','Turnip','Corn','Rice','Parsnip','Radish','Rutabaga']
            occupation_data[1] = farmers[random.randint(0,7)] + " " + occupation_data[1]
            farm_animals = ['Hen','Sheep','Goat','Cow','duck','Goose','Mule']
            occupation_data[3] = farm_animals[random.randint(0,6)]
        if roll == 95:
            occupation_data[3] = occupation_data[3].strip('*')
            cart_load = ['Tomatoes','Nothing','Straw','Your dead','Dirt','Rocks']
            occupation_data[3] = occupation_data[3] + ' of ' + cart_load[random.randint(0,5)]
        char['Occupation'] = occupation_data[1]
        char['Strength'] = roll_multiple('3d6')
        char['Agility'] = roll_multiple('3d6')
        char['Stamina'] = roll_multiple('3d6')
        char['Personality'] = roll_multiple('3d6')
        char['Intelligence'] = roll_multiple('3d6')
        char['Luck'] = roll_multiple('3d6')
        for i in tables['Table 1-1: Ability Score Modifiers']['table']:
            if i[0] == str(char['Strength']):
                if i[1] == 'None':
                    i[1] = '0'
                char['Strength Modifier'] = int(i[1])
            if i[0] == str(char['Agility']):
                if i[1] == 'None':
                    i[1] = '0'
                char['Agility Modifier'] = int(i[1])
            if i[0] == str(char['Stamina']):
                if i[1] == 'None':
                    i[1] = '0'
                char['Stamina Modifier'] = int(i[1])
            if i[0] == str(char['Personality']):
                if i[1] == 'None':
                    i[1] = '0'
                char['Personality Modifier'] = int(i[1])
            if i[0] == str(char['Intelligence']):
                if i[1] == 'None':
                    i[1] = '0'
                char['Intelligence Modifier'] = int(i[1])
            if i[0] == str(char['Luck']):
                if i[1] == 'None':
                    i[1] = '0'
                char['Luck Modifier'] = int(i[1])
        char['AC'] = 10
        if char['Agility Modifier'] != 0:
            char['AC'] += int(char['Agility Modifier'])
        char['HP'] = random.randint(1,4)
        if char['Stamina Modifier'] != 0:
            char['HP'] += int(char['Stamina Modifier'])
            if char['HP'] < 1:
                char['HP'] = 1
        char['Trained Weapon'] = occupation_data[2]
        roll = random.randint(1,24)
        char['Equipment'] = tables['Table 3-4: Equipment']['table'][roll][1]
        char['Trade Goods'] = occupation_data[3]
        if 'Dwarven' in char['Occupation'] or 'Halfling' in char['Occupation']:
            char['Speed'] = 20
        else:
            char['Speed'] = 30
        char['Initiative'] = 0
        if char['Agility Modifier'] != '':
            char['Initiative'] = char['Agility Modifier']
        char['Reflex'] = char['Agility Modifier']
        char['Fortitude'] = char['Stamina Modifier']
        char['Will'] = char['Personality Modifier']
        char['Treasure'] = {}
        char['Treasure']['cp'] = roll_multiple('5d12')
        birth_auger_roll = random.randint(1,30)
        num_lang = 0
        char['Birth Auger'] = tables['Table 1-2: Luck Score']['table'][birth_auger_roll][1]
        if char['Luck Modifier'] != 0:
            char['Birth Auger'] += f" ({char['Luck Modifier']:+})"
            if birth_auger_roll == 30:
                char['Speed'] += int(char['Luck Modifier']) * 5
            elif birth_auger_roll == 29:
                print('bird song languages')
                num_lang += int(char['Luck Modifier'])
            elif birth_auger_roll == 25:
                char['HP'] += int(char['Luck Modifier'])
                if char['HP'] < 1:
                    char['HP'] = 1
            elif birth_auger_roll == 24:
                char['Initiative'] += int(char['Luck Modifier'])
            elif birth_auger_roll == 23:
                char['AC'] += int(char['Luck Modifier'])
            elif birth_auger_roll == 22:
                char['Will'] += int(char['Luck Modifier'])
            elif birth_auger_roll == 21:
                char['Fortitude'] += int(char['Luck Modifier'])
            elif birth_auger_roll == 20:
                char['Reflex'] += int(char['Luck Modifier'])
            elif birth_auger_roll == 17:
                char['Reflex'] += int(char['Luck Modifier'])
                char['Fortitude'] += int(char['Luck Modifier'])
                char['Will'] += int(char['Luck Modifier'])
        # language
        char['Languages'] = ["Common"]
        num_lang += int(char['Intelligence Modifier'])
        if 'Halfling' in char['Occupation']:
            lang_col = 2
            char['Languages'].append('Halfling')
        elif 'Elven' in char['Occupation']:
            lang_col = 3
            char['Languages'].append('Elf')
        elif 'Dwarven' in char['Occupation']:
            lang_col = 4
            char['Languages'].append('Dwarf')
        else:
            lang_col = 1
        n = 0
        while n < num_lang:
            roll = random.randint(1, 100)
            for i in range(1, len(tables['Languages']['table'])):
                if tables['Languages']['table'][i][lang_col] != '-':
                    numbers = tables['Languages']['table'][i][lang_col].split('-')
                    if len(numbers) == 1:
                        numbers.append(numbers[0])
                    if roll in range(int(numbers[0]),int(numbers[1])+1):
                        if tables['Languages']['table'][i][0] in char['Languages']:
                            break
                        else:
                            char['Languages'].append(tables['Languages']['table'][i][0])
                            n += 1
                            # break
        #             elif int(tables['Languages']['table'][i][lang_col]) == roll:
        #                 print(f"single {tables['Languages']['table'][i][1]}")
        #                 char['Languages'].append(tables['Languages']['table'][i][0])
        #                 break
        # #     for i in range(1, len(tables['Languages']['table'])):
        #         if tables['Languages']['table'][i][lang_col] != '-':
        #             if '-' in tables['Languages']['table'][i][lang_col]:
        #                 numbers = tables['Languages']['table'][i][lang_col].split('-')
        #                 print(f"numbers {numbers}")
        #                 if roll in range(int(numbers[0]),int(numbers[1])+1):
        #                     char['Languages'].append(tables['Languages']['table'][i][0])
        #                     break
        #             elif int(tables['Languages']['table'][i][lang_col]) == roll:
        #                 print(f"single {tables['Languages']['table'][i][1]}")
        #                 char['Languages'].append(tables['Languages']['table'][i][0])
        #                 break
        # # end language
        with open('dcc-log.md', 'a') as f:
            f.write('\n')
            f.write('\n')
            f.write('-------------------------------------------\n')
            f.write('__Peasant Created__\n')
            f.write(f"Occupation: {char['Occupation']}   \n")
            f.write(f"Strength: {char['Strength']} ({char['Strength Modifier']:+})   \n")
            f.write(f"Agility: {char['Agility']} ({char['Agility Modifier']:+})   \n")
            f.write(f"Stamina: {char['Stamina']} ({char['Stamina Modifier']:+})   \n")
            f.write(f"Personality: {char['Personality']} ({char['Personality Modifier']:+})   \n")
            f.write(f"Intelligence: {char['Intelligence']} ({char['Intelligence Modifier']:+})   \n")
            f.write(f"Luck: {char['Luck']} ({char['Luck Modifier']:+})   \n")
            f.write('   \n')
            f.write(f"AC: {char['AC']}; HP:{char['HP']}   \n")
            f.write(f"Weapon: {char['Trained Weapon']}   \n")
            f.write(f"Speed: {char['Speed']}; Init:{char['Initiative']}; Ref: {char['Reflex']:+}; Fort: {char['Fortitude']:+}; Will: {char['Will']:+}   \n")
            f.write('   \n')
            f.write(f"Equipment: {char['Equipment']}   \n")
            f.write(f"Trade good: {char['Trade Goods']}   \n")
            f.write(f"Starting Funds: {char['Treasure']['cp']} cp   \n")
            f.write(f"Lucky sign: {char['Birth Auger']}   \n")
            f.write(f"Languages: {char['Languages']}   \n")
            f.write('-------------------------------------------\n')
        print()
        table = Table(title="Peasant", show_header=False, show_lines=True, show_edge=False, title_justify="left", title_style="red on white")
        table.add_column("one", justify="right", style="cyan", no_wrap=True)
        table.add_column("two", style="yellow")
        for i in char:
            table.add_row(f"{i}",f"{str(char[i])}")
        console.print(table)
        display_instructions()

    # roll_table = cmd2.Cmd2ArgumentParser()
    # roll_parser.add_argument('-p', '--piglatin', action='store_true', help='atinLay')
    # roll_parser.add_argument('-s', '--shout', action='store_true', help='N00B EMULATION MODE')
    # roll_parser.add_argument('-r', '--repeat', type=int, help='output [n] times')
    # roll_table.add_argument('dice', help='Dice to roll (e.g. 3d6)')
    # @cmd2.with_argparser(roll_table)
    @with_argument_list
    def do_rolltable(self, args):
        """Roll on a table. You can add a dice roll to the command but it rolls on the rows of the table which may be different then the entries."""
        table_data = view_tables()
        if table_data != "cancel":
            print("")
            if 'meta' in table_data[2][table_data[0]].keys():
                startRow = int(table_data[2][table_data[0]]['meta']['Start at'])
            else:
                startRow = 0
            if len(args) == 0:
                roll = random.randint(1, len(table_data[1])-startRow-1)
                print( f"Rolling (1-{len(table_data[1])-startRow-1}): {roll}" )
            else:
                roll = roll_multiple(args[0])+startRow
            print("")
            table = Table(title= table_data[0], show_header=True, show_lines=True, show_edge=False, title_justify="left", title_style="black on violet")
            for n in table_data[1][0]:
                table.add_column(n)
            if type(table_data[1][0]) is list:
                table.add_row(*table_data[1][roll])
                # print( f"Rolling ({args[0]}): {roll}" )
            elif type(table_data[1][0]) is dict:
                # roll = random.randint(0, len(table_data[1])-1)
                table.add_row(*table_data[1][roll-1].values())
            console.print(table)
            with open('dcc-log.md', 'a') as f:
                f.write('\n')
                f.write(f"{table_data[0]}\tRoll: {roll}\n")
                if type(table_data[1][0]) is list:
                    f.write(f"{table_data[1][roll]}")
                elif type(table_data[1][0]) is dict:
                    for i in table_data[1][0]:
                        f.write(i)
                        f.write(': ')
                        f.write(table_data[1][roll][i])
                        f.write('\t')
                f.write('\n')

    table_parser = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(table_parser)
    def do_table(self, args):
        """View a table."""
        table_data = view_tables()
        if table_data != "cancel":
            display_table(table_data[0], table_data[1], table_data[2])

class NoShellApp(cmd2.Cmd):
    delattr(cmd2.Cmd, 'do_shell')
class NoEdit(cmd2.Cmd):
    delattr(cmd2.Cmd, 'do_edit')
class Norun_pyscriptApp(cmd2.Cmd):
    delattr(cmd2.Cmd, 'do_run_pyscript')
class Norun_scriptApp(cmd2.Cmd):
    delattr(cmd2.Cmd, 'do_run_script')
def load_tables():
    try:
        with open(SYSTEM_TABLES_FILE_PATH) as file:
            tables = json.load(file)

        # table_names = list(tables.keys())
        return tables
        # print('table_names', table_names)

        if not table_names:
            print("No tables found.")
            return

    except FileNotFoundError:
        print(f"Table file not found: {SYSTEM_TABLES_FILE_PATH}")

def view_tables():
    tables = load_tables()
    table_names = list(tables.keys())
    print()
    print("[bold] Available tables:[/bold]")
    for index, table_name in enumerate(table_names, start=1):
        print(f"{index}. {table_name}")

    while True:
        try:
            choice = int(input("Enter the table number to display: "))
            if choice < 1 or choice > len(table_names):
                print("Invalid choice. Try again.")
            else:
                table_name = table_names[choice - 1]
                return table_name, tables[table_name]['table'], tables
                # print(table_name)
                break
        except ValueError:
            print("[red]Cancel[/red]")
            return "cancel"


def parse_numbers(input_string):
    # Find all occurrences of one or more digits in the input string
    numbers = re.findall(r'\d+', input_string)
    # If only one number is found, return it as an integer
    if len(numbers) == 1:
        return 1, int(numbers[0])
    # If two numbers are found, return a tuple of two integers
    elif len(numbers) == 2:
        return int(numbers[0]), int(numbers[1])
    # If no numbers are found, return 0
    else:
        return 0
def roll_single(sides):
    return random.randint(1,int(sides))
def roll_multiple(dice): # takes a roll like 3d6
    rolls = 0
    for n in range(0,parse_numbers(dice)[0]): # parse_numbers turns 3d6 into [3,6]
        rolls += roll_single(parse_numbers(dice)[1]) # sends the second number in parse_numbers and gets a random
    return rolls
def display_table(table_name, table_data, tables):
    print()
# print('tablename: ',table_name,'\ntable_data: ',table_data,'\ntables: ',tables)
    table = Table(title= table_name, show_header=True, show_lines=True, show_edge=False, title_justify="left", title_style="black on violet")
    for n in table_data[0]:
        table.add_column(n)
    # for i in table_data:
    for i in range(0, len(table_data)):
        if isinstance(table_data[0], list):
            if i != 0:
                table.add_row(*table_data[i])
        elif isinstance(table_data[0], dict):
            table.add_row(*table_data[i].values())
    console.print(table)
    # Display footnotes
    if "footnotes" in tables[table_name]:
    # if table_name in tables and "footnotes" in tables[table_name]:
        footnotes = tables[table_name]["footnotes"]
        if footnotes:
            print()
            for footnote in footnotes:
                print(f"{footnote}")
    display_instructions()

if __name__ == '__main__':
    import sys
    c = FirstApp()
    sys.exit(c.cmdloop())
