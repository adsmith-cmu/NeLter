# NeLter <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Description](#description)
- [Installation](#installation)
- [Shortcut Commands](#shortcut-commands)

## Description

NeLter is computer tool designed to help amatuer players improve at No Limit Texas Hold 'em.
It features a full fledged simulation game where the user can test their abilities against any number of computer opponents that employ a range analysis algorithm and basic strategy to mimic a real life opponent.

## Installation

This project requires python3, pillow, and requests to be installed in order to run. Python3 can be downloaded [here](https://www.python.org/downloads/). Once downloaded run the code below ([sourced here](https://www.kosbie.net/cmu/fall-19/15-112/notes/notes-animations-part2.html#installingModules)) for your respective operating system in a python file, and run the output in a terminal or command prompt instance.

MacOSX/Linux:

    import sys
    print(f'sudo "{sys.executable}" -m pip install pillow')
    print(f'sudo "{sys.executable}" -m pip install requests')

Windows:

    import sys
    print(f'"{sys.executable}" -m pip install pillow')
    print(f'"{sys.executable}" -m pip install requests')

Now to start the application run the **nelter.py** file with python. If you encounter errors ensure all of the python files and resources folder are present in the same directory as the driver file.

## Shortcut Commands

The following methods can be used to manually perform the named action as the player who has action on them:

    texas_holdem.hand.bet(amount=0)
    texas_holdem.hand.call()
    texas_holdem.hand.fold()

The following method will advance the game by one betting round manually:

    texas_holdem.hand.progress_game()

The following method will trigger an immediate showdown:

    texas_holdem.hand.showdown()
