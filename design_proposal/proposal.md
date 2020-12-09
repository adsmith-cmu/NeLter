# NeLter <!-- omit in toc -->

## Table of Contents <!-- omit in toc -->

- [Description](#description)
- [Competitive Analysis](#competitive-analysis)
- [Structure](#structure)
- [Algorithmic Plan](#algorithmic-plan)
- [Timeline](#timeline)
- [Version Control](#version-control)
- [Module List](#module-list)
- [TP2 Updates](#tp2-updates)
- [TP3 Updates](#tp3-updates)

## Description

NeLter is computer tool designed to help amatuer players improve at No Limit Texas Hold 'em.
It features a full fledged simulation game where the user can test their abilities against any number of computer opponents that employ a range analysis algorithm and basic strategy to mimic a real life opponent.

## Competitive Analysis

There are countless paid applications on the internet dedicated to helping the user improve at No Limit Texas Hold 'em. This game is extremely complex due to how abstract it is, and infact it was only a year ago that computers (developed in part by CMU) were able to beat the top humans in six-player games. Due to this complexity at the highest level, most of these tools only focus giving the user a very indepth understanding of one part of their game. This can be very effective for helping a veteran player sharpen one side of their game, but can leave a beginner feeling rather confused and unguided.

There are also lots of free utilities for specifc jobs like calculating equity, pot odds, fold equity, etc., but it is up to the user to decipher what these concepts are and why they should care about them. The goal of NeLter is to fill this gap. It will provide a comprehensive user experience where they will experience many different poker concepts through playing in an easy to digest manor, so that they can implement them into their own game, and practice against the computer.

## Structure

The NeLter framework contains several files which implement the GUI for the entire application, the files which implement training modes, and the main game. 

- The GUI has a main file that is executed, as well as some helper modules which are imported into that main file.
- The main game is composed of several helper modules and a driver file. Each player, hand, and computer are implemented as objects and are constructed by the driver file that runs the game. The computer algorithm to play the game involves principles from basic strategy, but ultimatly analyzes its opponents expected range based on previous moves to decide its own moves.

## Algorithmic Plan

The most algorithmically complex part of this tool is the computer algorithm that plays the game. The way this algorithm will work is by trying to guess the opponents' holdings and act according to various well established poker principles. This will be done through a range analysis algorithm where the computer will try to narrow down possible enemy hands based on a variety of factors that will start at a default, and be narrowed down by monitoring the opponents' play over time and trying to establish habitual behaviors.

## Timeline

During the first week of working on this project I have nearly completed the framework for playing and manipulating the game. During the second week I plan to write the GUI for the app, write a preliminary computer algorithm using mostly basic poker principles. Finally, in the last week I plan on refining the user interface and experience as well as trying improving the computer algorithm to utilize past play analysis to make more informed decisions.

## Version Control

Version control for this project is handled through Git and GitHub. See image in directory.

## Module List

- Pillow
- Tkinter
- ~~Pickle~~

## TP2 Updates

None.

## TP3 Updates

Due to time constraints I spent the last week of this project working on refining the user interface and improving the computer algorithm and didn't have time to implement trainning modes like I wanted, but the principles still remain in the algorithm. Moreover, I wasn't able to implement pickle in the way that I wanted to so I've updated the [Module List](#module-list) to reflect that. I think I will do this in my own time after the project as a passion project since I am very interested in this area and would like to use this as a something to display on my resumé. 
