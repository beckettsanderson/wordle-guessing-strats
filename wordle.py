# -*- coding: utf-8 -*-
"""
Homework 4:
    Creating a wordle strategy comparison

@author: Beckett Sanderson
"""

import matplotlib.pyplot as plt
import random
import numpy as np

WORDS = "five_letter_words.txt"
LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
           "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
EXPERIMENTS = 1000
TRIALS = 500

def read_file(filename):
    """
    Reads in a file to create a data frame

    Parameters
    ----------
    filename : string
        the location of the file to read in data from.

    Returns
    -------
    file_data : list
        the data contained in the txt file as a list.

    """
    file_data = []
    
    # opens input file
    with open(filename, "r") as file:
        
        # loops through file line by line and appends to the list
        for line in file:
            
            file_data.append(line.strip())
    
    return file_data


def get_top_n(words_list, pos_int, num_lett = 26, LETTERS = LETTERS):
    """
    Creates a dictionary of the number of occurences of certain letters in 
    certain positions from all words in a list

    Parameters
    ----------
    words_list : list
        list of all the words we're going over.
    pos_int : int
        the index position in the word we care about.
    num_lett : int
        the number of letters we care about.
    LETTERS : list, constant
        a list of all the letters in the alphabet.

    Returns
    -------
    lett_dict : dict
        dictionary denoting the frequency of a letter's occurence in the spot.

    """
    lett_dict = {}
    
    # loops through every word in the word list
    for word in words_list:
        
        # checks if the letter of the word is in the dictionary already
        if word[pos_int] not in lett_dict:
            
            # creates letter entry if not in the dictionary
            lett_dict[word[pos_int]] = 1
        
        # if in the dictionary adds to the letter count
        else:
            
            lett_dict[word[pos_int]] += 1

    # loops through each letter in the letters list
    for letter in LETTERS:
        
        # checks if enough letters are in the dictionary
        if len(lett_dict) >= num_lett:
            
            # breaks the loop once dictionary is required length
            break
        
        # checks if the letter is already in the dictionary
        elif letter not in lett_dict:
            
            # adds the letter to dictionary if not already a part of it
            lett_dict[letter] = 0
    
    return lett_dict


def find_min(lett_dict):
    """
    Find the letter with the lowest frequency in a dictionary

    Parameters
    ----------
    lett_dict : dictionary
        dictionary containing letters and their corresponding frequency.

    Returns
    -------
    min_lett : string
        letter with the lowest frequency in the input dictionary.

    """
    min_lett = None
    
    # loops through each letter in the letter dictionary
    for letter in lett_dict:
        
        # check if min lett has a val or if the current letter has a lower val
        if min_lett == None or lett_dict[letter] < lett_dict[min_lett]:
            
            # resets min_lett to the current letter
            min_lett = letter
            
    return min_lett


def top_five(words_list, pos_idx):
    """
    Returns the top 5 letters at a specific index

    Parameters
    ----------
    words_list : list
        list of all the words we're going over.
    pos_idx : int
        the index position in the word we care about.

    Returns
    -------
    top_five : dictionary
        dictionary containing only the top 5 letters for the index 
        and their frequencies.

    """
    top_five = {}
    
    # gets the full dictionary of letters and their corresponding frequencies
    full_dict = get_top_n(words_list, pos_idx)
    
    # loops through each letter in the dictionary
    for letter in full_dict:
        
        # checks if the top five is full of values yet
        if len(top_five) < 5:
            
            # adds letter value to top five if not full
            top_five[letter] = full_dict[letter]
            
        else:
            
            # finds the letter with the lowest value in the current top five
            min_lett = find_min(top_five)
            
            # checks if the current letter has a higher frequency than the min
            if full_dict[letter] > top_five[min_lett]:
                
                # replaces the lowest letter with the current letter
                del top_five[min_lett]
                top_five[letter] = full_dict[letter]
    
    return top_five


def get_best_letters(words_list):
    """
    Finds the 5 best letters for each slot in a 5 letter word and creates
    a dictionary describing the info

    Parameters
    ----------
    words_list : list
        list of all the words we're going over.
    
    Returns
    -------
    best_letters : dictionary
        a dictionary describing the 5 best letters for each letter slot.

    """
    first_slot = top_five(words_list, 0)
    second_slot = top_five(words_list, 1)
    third_slot = top_five(words_list, 2)
    fourth_slot = top_five(words_list, 3)
    fifth_slot = top_five(words_list, 4)

    best_letters = {"first": first_slot, "second": second_slot, 
                    "third": third_slot, "fourth": fourth_slot, 
                    "fifth": fifth_slot}
    
    return best_letters


def num_matches(target, guess):
    """
    Returns the number of letter with the same place and value in two words

    Parameters
    ----------
    target : string
        the word the guess word is trying to guess.
    guess : string
        the guessed attempt word.

    Returns
    -------
    exact_letters : int
        the number of letters that are the same in the two words.

    """
    exact_letters = 0
    
    # loops through the indices for the target word
    for i in range(len(target)):
        
        # checks if the letter of the index is the same
        if guess[i] == target[i]:
            
            # adds to the counter if the letters are the same
            exact_letters += 1 
    
    return exact_letters


def run_experiment(words_list, experiments = EXPERIMENTS):
    """
    Run a comparison experiment a certain number of times

    Parameters
    ----------
    words_list : list
        list of all the words we're going over.
    experiments : int, optional
        number of experiments to run. The default is EXPERIMENTS.

    Returns
    -------
    felix_pts : list
        list containing the numbers of points for felix.
    laney_pts : list
        list containing the numbers of points for laney.

    """
    # choose words to check (technically coaes is better by 93 points, but 
    # cores is a real word so I wanted to use that
    felix_word = "cores"
    laney_word = random.choice(words_list)
    
    # initialize lists
    felix_pts = []
    laney_pts = []
    
    # loop through number of experiments to run
    for i in range(experiments):
        
        # intializes a new word to check
        wordle_word = random.choice(words_list)
        
        # appends the comparison results to the lists
        felix_pts.append(num_matches(wordle_word, felix_word))
        laney_pts.append(num_matches(wordle_word, laney_word))
        
    return felix_pts, laney_pts
        

def run_trials(words_list, trials = TRIALS):
    """
    Run a number of trials containing the experiments and return the avgs

    Parameters
    ----------
    words_list : list
        list of all words we're going over.
    trials : int, optional
        the number of trials to run. The default is TRIALS.

    Returns
    -------
    felix_avgs : list
        a list containing the avg results for felix from the experiments.
    laney_avgs : list
        a list containing the avg results for felix from the experiments.

    """
    felix_avgs = []
    laney_avgs = []
    
    # runs the loop for the number of trials requested
    for i in range(trials):
        
        # run the experiment and return the list oo results
        felix_pts, laney_pts = run_experiment(words_list)
    
        # append the avg of list of results to the avg list
        felix_avgs.append(np.mean(felix_pts))
        laney_avgs.append(np.mean(laney_pts))
        
    return felix_avgs, laney_avgs


def Main():
    
    # open the words file
    words = read_file(WORDS)
    print(words[0:25], "\n")
    print("Number of words:", len(words), "\n")
    
    # gets the best letters for each of the slots
    best_letters = get_best_letters(words)
    print(best_letters)
    
    # run trails for word prediction
    felix_avgs, laney_avgs = run_trials(words)
    
    # plot the data from the two different strategies
    plt.hist(felix_avgs, bins = 5, label = "Felix", color = "darkorchid", 
             alpha = 0.7, edgecolor = "black")
    plt.hist(laney_avgs, bins = 10, label = "Laney", color = "seagreen", 
             alpha = 0.7, edgecolor = "black")
    
    # graph organization
    plt.title("Wordle Guessing Strategies")
    plt.xlabel("Number of Letters Correct")
    plt.ylabel("Number of Experiments")
    plt.legend()
    plt.show()
    

if __name__ == "__main__":
    
    Main()
