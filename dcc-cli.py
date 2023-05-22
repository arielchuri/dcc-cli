#!/usr/bin/env python
"""A simple cmd2 application."""
import cmd2
import argparse
from rich.console import Console
from rich.text import Text
from rich.table import Table
from rich import print
import json
import re
import random

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
def display_instructions():
    """Display the initial instructions with available commands."""
    print(" ")
    print("Available commands: [yellow]help[/yellow], [blue]rolltable[/blue], [red]tables[/red], [violet]roll[/violet], [green]quit[/green]")
    print(" ")

class FirstApp(cmd2.Cmd):
    def __init__(self):
        self.debug = True
        shortcuts = cmd2.DEFAULT_SHORTCUTS
        shortcuts.update({'&': 'roll'})
        # shortcuts.update({'t': 'tables'})
        super().__init__()

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
        for dieroll in args.dice: # loops through each argument
            roll = roll_multiple(dieroll) # sends the roll to roll_multiple()
            # making a definition list in rolls of the dice the put in and the rolled value
            total += roll # adds to the total
            print(f"[yellow]{dieroll}:[/yellow][yellow][/yellow]\t[red]{roll}[/red]") # prints roll
        print(f"Total\t{total}") #prints total
        # self.poutput(' '.join(rolls))

    zero = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(zero)
    def do_zero(self, args):
        """Generate zero levels"""
        tables = load_tables()
        char = {}
        occupation_data = []
        roll = random.randint(1, 100)
        print(roll)
        for i in range(1, len(tables['Table 1-3: Occupation']['table'])):
            if '-' in tables['Table 1-3: Occupation']['table'][i][0]:
                numbers = tables['Table 1-3: Occupation']['table'][i][0].split('-')
                if roll in range(int(numbers[0]),int(numbers[1])+1):
                    occupation_data = tables['Table 1-3: Occupation']['table'][i]
                    break
            elif int(tables['Table 1-3: Occupation']['table'][i][0]) == roll:
                occupation_data = tables['Table 1-3: Occupation']['table'][i]
                break
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
                    i[1] = ''
                char['Strength Modifier'] = i[1]
            if i[0] == str(char['Agility']):
                if i[1] == 'None':
                    i[1] = ''
                char['Agility Modifier'] = i[1]
            if i[0] == str(char['Stamina']):
                if i[1] == 'None':
                    i[1] = ''
                char['Stamina Modifier'] = i[1]
            if i[0] == str(char['Personality']):
                if i[1] == 'None':
                    i[1] = ''
                char['Personality Modifier'] = i[1]
            if i[0] == str(char['Intelligence']):
                if i[1] == 'None':
                    i[1] = ''
                char['Intelligence Modifier'] = i[1]
            if i[0] == str(char['Luck']):
                if i[1] == 'None':
                    i[1] = ''
                char['Luck Modifier'] = i[1]
        char['AC'] = 10
        if char['Agility Modifier'] != '':
            char['AC'] += int(char['Agility Modifier'])
        char['HP'] = random.randint(1,4)
        if char['Stamina Modifier'] != '':
            char['HP'] += int(char['Stamina Modifier'])
            if char['HP'] < 1:
                char['HP'] = 1
        char['Trained Weapon'] = occupation_data[2]
        char['Trade Goods'] = occupation_data[3]
        if 'Dwarven' in char['Occupation'] or 'Halfling' in char['Occupation']:
            char['Speed'] = '20'
        else:
            char['Speed'] = '30'
        char['Initiative'] = '0'
        if char['Agility Modifier'] != '':
            char['Initiative'] = char['Agility Modifier']
        char['Reflex'] = char['Agility Modifier']
        char['Fortitude'] = char['Stamina Modifier']
        char['Will'] = char['Personality Modifier']
        char['Treasure'] = {}
        char['Treasure']['cp'] = roll_multiple('5d12')
        print(tables['Table 1-2: Luck Score']['table'][1])
        char['Birth Auger'] = tables['Table 1-2: Luck Score']['table'][random.randint(1,30)][1]
        if char['Luck Modifier'] != '':
            print(char['Luck Modifier'])
            char['Birth Auger'] += " " + char['Luck Modifier']
        print(char)
        teststr = 'hello'
        with open('chartest.md', 'w') as f:
            for i in char:
                f.write(i)
                f.write(' :\t\t\t')
                f.write(str(char[i]))
                f.write('\n')

    roll_table = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(roll_table)
    def do_rolltable(self, args):
        """Roll on a table."""
        table_data = view_tables()
        table = Table(show_header=True, header_style="bold green")
        for n in table_data[1][0]:
            table.add_column(n)
        if type(table_data[1][0]) is list:
            roll = random.randint(1, len(table_data[1])-1)
            table.add_row(*table_data[1][roll])
        elif type(table_data[1][0]) is dict:
            roll = random.randint(0, len(table_data[1])-1)
            table.add_row(*table_data[1][roll].values())
        if table_data != "cancel":
            print()
            print(f"[black on violet bold]  {table_data[0]}  [/black on violet bold]")
            print()
            console.print(table)

    table_parser = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(table_parser)
    def do_tables(self, args):
        """View a table."""
        table_data = view_tables()
        if table_data != "cancel":
            display_table(table_data[0], table_data[1], table_data[2])

class NoShellApp(cmd2.Cmd):
    delattr(cmd2.Cmd, 'do_shell')
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
                # print(tables[table_name]["table"])
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
    print(f"[black on yellow bold]  {table_name}  [/black on yellow bold]")
    print()
# print('tablename: ',table_name,'\ntable_data: ',table_data,'\ntables: ',tables)
    table = Table(show_header=True, header_style="bold magenta")
    for n in table_data[0]:
        table.add_column(n)
    # for i in table_data:
    for i in range(1, len(table_data)):
        if isinstance(table_data[0], list):
            table.add_row(*table_data[i])
        elif isinstance(table_data[0], dict):
            table.add_row(*table_data[i].values())
    console.print(table)
    # Display footnotes
    if "footnotes" in tables[table_name]:
    # if table_name in tables and "footnotes" in tables[table_name]:
        footnotes = tables[table_name]["footnotes"]
        if footnotes:
            for footnote in footnotes:
                print(f"{footnote}")
    display_instructions()

if __name__ == '__main__':
    import sys
    c = FirstApp()
    sys.exit(c.cmdloop())
