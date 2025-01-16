
# Wolt Roulette

## Introduction

*Wolt Roulette* is a python based application that removes the stress of having to choose where to order from. Simply enter a location, and *Wolt Roulette* immediately gives you a restaurant to order from. Remove the stress from your life, one food-based decision at a time.

## Workflow
The workflow for the application is as follows:
### 1. User input
- The application starts by prompting the user to enter a location, and food preferences/restrictions (if any). 
### 2: Data processing
* The program then retrieves the geographical coordinates of that location, and uses them to retrieve a list of restaurants that currently deliver to that area
* The program filters according to the criteria.
* The program then randomly chooses a restaurant from that list.
### 3: Output
* The user is presented with a Wolt link to the restaurant

## Running the program

The program can be run from the command line as follows:

`python wolt_roulette.py`

The program will prompt the user for all required inputs.


## Requirements

The program will utilize the `requests` library to facilitate communication with the Wolt API

