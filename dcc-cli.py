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

def display_instructions():
    """Display the initial instructions with available commands."""
    print("[black on violet] +++++++++++++++++++++++++++++++++++++++++++++ [/black on violet]")
    print("[black on violet] Welcome the DCC Quickstart Command Line Tool! [/black on violet]")
    print("[black on violet] +++++++++++++++++++++++++++++++++++++++++++++ [/black on violet]")
    print(" ")
    print("Available commands: [yellow]help[/yellow], [blue]rolltable[/blue], [red]tables[/red], [violet]roll[/violet], [green]quit[/green]")

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

    roll_table = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(roll_table)
    def do_rolltable(self, args):
        """Roll on a table."""
        print(self)

    table_parser = cmd2.Cmd2ArgumentParser()
    @cmd2.with_argparser(table_parser)
    def do_tables(self, args):
        """View a table."""
        print(args)
        table_data = view_tables()
        display_table(table_data[0], table_data[1], table_data[2])
        # display_table(table_name, tables[table_name]['table'], tables)

class NoShellApp(cmd2.Cmd):
    delattr(cmd2.Cmd, 'do_shell')
class Norun_pyscriptApp(cmd2.Cmd):
    delattr(cmd2.Cmd, 'do_run_pyscript')
class Norun_scriptApp(cmd2.Cmd):
    delattr(cmd2.Cmd, 'do_run_script')
def view_tables():
    try:
        with open(SYSTEM_TABLES_FILE_PATH) as file:
            tables = json.load(file)

        table_names = list(tables.keys())
        # print('table_names', table_names)

        if not table_names:
            print("No tables found.")
            return

        print("Available tables:")
        for index, table_name in enumerate(table_names, start=1):
            print(f"{index}. {table_name}")

        while True:
            try:
                choice = int(input("Enter the table number to display: "))
                if choice < 1 or choice > len(table_names):
                    print("Invalid choice. Try again.")
                else:
                    # table_name = table_names[choice - 1]
                    return table_name, tables[table_name]['table'], tables
                    # print(tables[table_name]["table"])
                    break
            except ValueError:
                print("[red]Cancel[/red]")
                return

    except FileNotFoundError:
        print(f"Table file not found: {SYSTEM_TABLES_FILE_PATH}")

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
    # print('tablename: ',table_name,'\ntable_data: ',table_data,'\ntables: ',tables)
    table = Table(show_header=True, header_style="bold magenta")
    for n in table_data[0]:
        table.add_column(n)
    for i in table_data:
        if isinstance(table_data[0], list):
            table.add_row(*i)
        elif isinstance(table_data[0], dict):
            table.add_row(*i.values())
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
