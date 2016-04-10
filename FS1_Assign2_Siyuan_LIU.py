############################
#   CZ 1003 Assignment 2   #
#        Autocorrect       #
#                          #
#  Written by Liu Siyuan   #
#  From group FS1          #
############################

from time import time
import string

# set the translation table to use with .translate method later
# all digits will be replaced by white spaces and all uppercase
# letters will be replaced by lowercase letters
translation_table = str.maketrans(string.digits+string.ascii_uppercase,
                                  " "*len(string.digits)+string.ascii_lowercase)

def display_time():
    """This function enables the time display feature"""

    global display_time_used
    display_time_used = True

def not_display_time():
    """This function disables the time display feature"""

    global display_time_used
    display_time_used = False

def read_into_list():
    """This function reads the file 'big.txt' into a list"""

    with open("big.txt") as wordbase:
        text      = wordbase.read().translate(translation_table) # translate the text using the translation table
        everyword = [word.strip(string.punctuation) for word in text.split()] # strip punctuation at both sides

    return everyword

def add_extra_words():
    """This function is used to add extra words to the unique word list"""

    global unique_words, old_unique_words, new_words, word_frequency, old_word_frequency

    with open("word_list.txt") as wordbase_2:
            new_words = set(wordbase_2.read().split())

    old_unique_words   = unique_words # save a copy of old unique word list
    unique_words       = unique_words | new_words # add extra words to the previous unique word list

    old_word_frequency = word_frequency # save a copy of old word frequency
    word_frequency.update(count_frequency(new_words)) # update the word frequency after extra words are added

    print("Extra words are added to the word list")

def remove_extra_words():
    """This function is used to remove the extra words added"""

    global unique_words, word_frequency

    unique_words   = old_unique_words # recover the old unique word list
    word_frequency = old_word_frequency # recover the old word frequency

    print("Extra words are removed from the word list")

def create_dict():
    """This function create the finalised word list for autocorrection"""

    global word_list

    word_list    = read_into_list() # first read every word into a word list
    unique_words = set(word_list) # convert the list to a set so that duplicate words are removed
    unique_words.remove("") # remove the empty string inside the set
    # remove all single letters in the word list
    for letter in string.ascii_lowercase:
        unique_words.remove(letter)

    return unique_words

def count_frequency(word_list):
    """This function counts the word frequency of a given word list"""

    frequency = {} # create a dictionary to map words to their frequency

    # everytime the a word appears, its frequency increase by 1
    for word in word_list:
        if word in frequency:
            frequency[word] += 1
        # if the word appears for the first time, we create that key in the dictionary and set its frequency to 1
        else:
            frequency[word] = 1

    return frequency

def possible_wrong_characters(word):
    """This function is used to calculate the upper limit for word distance"""

    # this is just my own way of defining the largest word distance that can be accpeted
    # possible_wrong_characters is set as the bound of word_distance
    if len(word) <= 4:
        possible_wrong_characters = 1
    else:
        possible_wrong_characters = min(int(len(word) * 0.2 + 1), 3)

    return possible_wrong_characters

def levenshtein_distance(word_to_correct, word_in_dict, possible_wrong_characters):
    """This function computes the levenshtein distance between two given words"""

    #initialize previous row of distances
    d_prev_row = range(len(word_in_dict) + 1)

    #calculate current row of distances from previous row of distances
    for i in range(len(word_to_correct)):

        #initialize currect row of distances
        d_curr_row = [i + 1] #first element in d_curr_row is i + 1

        #complete the current row of distances
        for j in range(len(word_in_dict)):
            if word_to_correct[i] == word_in_dict[j]:
                cost = 0
            else:
                cost = 1
            d_curr_row.append(min(d_curr_row[j] + 1, d_prev_row[j + 1] + 1, d_prev_row[j] + cost))
        # if the minimum distance of current row is larger than upper bound, skip the word
        if min(d_curr_row) > possible_wrong_characters:
            return possible_wrong_characters + 1
        else:
            pass
        #move current row of distance to previous row of distance for next iteration
        d_prev_row = d_curr_row

    return d_curr_row[-1]

def word_distance(word_to_correct, word_in_dict, possible_wrong_characters):
    """This function is used to determine the word distance between two words"""

    # Levenshtein distance and Hamming distance is used in this function to determine word distance

    # special cases:
    #
    # the levenshtein distance is at least the difference in size of the two strings.
    # we can use this to filter most of the words in word list which have different
    # length with the word to corrected
    if abs(len(word_to_correct) - len(word_in_dict)) > possible_wrong_characters:
        return possible_wrong_characters + 1
    elif len(word_to_correct) == len(word_in_dict):
        if word_to_correct != word_in_dict:
            return levenshtein_distance(word_to_correct, word_in_dict, possible_wrong_characters)
        else:
            return 0 # levenshtein distance of two identical strings is 0
    # since none of the words in the dictionary is empty string
    # we may skip the case where len(word_in_dict) == 0
    elif len(word_to_correct) == 0:
        return len(word_in_dict)
    # normal case where we have to compute the word distance
    else:
        len_a, len_b = len(word_to_correct), len(word_in_dict)
        if len_a > len_b:
            # make sure that the word to be compared is shorter so that the computation is memory efficient
            word_to_correct, word_in_dict = word_in_dict, word_to_correct
        return levenshtein_distance(word_to_correct, word_in_dict, possible_wrong_characters)

def add_word(word):
    """This fuction is used to add custom words"""

    global unique_words

    unique_words |= {word} # add custom word to the unique word list

def sort_possible_words(possible_words):
    """This function computes possible words in order of word distance and frequency"""

    for key in possible_words:
        # use insertion algorithm to sort the possible words dictionary
        for position in range(1, len(possible_words[key])):
            index = position
            word_frequency_index = word_frequency[possible_words[key][index]]
            word_frequency_prev_index = word_frequency[possible_words[key][index - 1]]
            while word_frequency_prev_index < word_frequency_index and index > 0:
                possible_words[key][index], possible_words[key][index - 1] = \
                possible_words[key][index - 1], possible_words[key][index]
                index -= 1

    return possible_words

def print_results(is_correct, possible_words):
    """This function is used to print out the results of autocorrection"""

    length_of_possible_words = len(possible_words)

    if is_correct:
        print("Your spelling is correct.")
    elif length_of_possible_words != 0: # if there is at least one possible word
        possible_word           = sort_possible_words(possible_words) # we need to sort the dictionary for later use
        smallest_word_distance  = min(possible_words) # find the smallest word distance among possible words
        range_of_possible_words = [key for key in possible_words] # all word distances for possible words
        range_of_possible_words.sort()
        # initialize two counter before print
        words_printed   = 0
        number_of_words = 0
        # count the number of words in this dictionary
        for key in possible_words:
            for value in possible_words[key]:
                number_of_words += 1
        # print out all possible words
        # the maximum number of words to be displayed is 6
        print("Did you mean: ", end="")
        if number_of_words > 6:
            for key in range_of_possible_words:
                for value in possible_words[key]:
                    if words_printed == 5:
                        print(value + "?")
                        words_printed += 1
                    elif words_printed == 4:
                        print(value + ", or ", end="")
                        words_printed += 1
                    elif 0 <= words_printed <= 3:
                        print(value + ", ", end="")
                        words_printed += 1
                    else:
                        break
                if words_printed == 6:
                    break
        else:
            for key in range_of_possible_words:
                for value in possible_words[key]:
                    if words_printed == number_of_words - 1:
                        print(value + "?")
                    elif words_printed == number_of_words - 2:
                        print(value + ", or ", end="")
                        words_printed += 1
                    elif 0 <= words_printed <= number_of_words - 3:
                        print(value + ", ", end="")
                        words_printed += 1
                    else:
                        pass
        # print out the most likely word if there is more than one possible word
        if number_of_words > 1:
            print("Most likely word is: {:s}".format(possible_words[smallest_word_distance][0]))
        else:
            pass
    else:
        print("No similar word found.")

def autocorrect(word_to_correct):
    """This function is used to autocorrect given word"""

    time_begin      = time() # set the start time
    word_to_correct = word_to_correct.lower() # change the word to lowercase word
    is_correct      = False # to see whether the word is in the dictionary
    typo_limit      = possible_wrong_characters(word_to_correct) # set a upper bound for autocorrection
    possible_words  = {} # create a dictionary to store possible corrections with their word distance

    # if the length of the word is longer than 4, then we compute word distance of part of the word first
    if len(word_to_correct) > 4:
        for word in unique_words:
            if 0 <= word_distance(word_to_correct[:4], word[:4], typo_limit) <= typo_limit:
                # for those which have small enough word distance, we compute the who string
                word_distance_of_word = word_distance(word_to_correct, word, typo_limit)
                if 1 <= word_distance_of_word <= typo_limit:
                    # if that key is not in the dictionary, create it first
                    if word_distance_of_word not in possible_words:
                        possible_words[word_distance_of_word] = []
                    # link the word to its corresponding word distance
                    possible_words[word_distance_of_word].append(word)
                elif word_distance_of_word == 0:
                    is_correct = True
                    break
                else:
                    pass
            else:
                pass
    # if the string is short enough, we compute the word distance directly
    else:
        for word in unique_words:
            word_distance_of_word = word_distance(word_to_correct, word, typo_limit)
            if 1 <= word_distance_of_word <= typo_limit:
                # if that key is not in the dictionary, create it first
                if word_distance_of_word not in possible_words:
                        possible_words[word_distance_of_word] = []
                # link the word to its corresponding word distance
                possible_words[word_distance_of_word].append(word)
            elif word_distance_of_word == 0:
                is_correct = True
                break
            else:
                pass

    time_used = time() - time_begin # time used to autocorrect

    print_results(is_correct, possible_words) # print out the results

    # print out the time used if user want to
    # this feature is enabled by default
    if display_time_used:
        print("It took {:0.3f} sec to autocorrect".format(time_used))

# codes to be excuted when imported

welcome = """Hi, you are using my autocorrection system!
"""

usage = """1. Use autocorrect(\"word\") to autocorrect the word
2. Use add_word(\"word\") to add your own words
3. Use add_extra_words() to extend the word list
4. Use remove_extra_words() to remove extra words
5. Use display_time() to display time consumption
6. Use not_display_time() to disable time display"""

notification = """
Please be notified that it may take a slightly
longer time for some words to autocorrect after
extra words are added
"""

print("*" * 50)
print(welcome)
print("=" * 23 + "USAGE" + "=" * 22)
print(usage)
print("=" * 50)
print(notification)

start_Time        = time() # time before the word list is created
unique_words      = create_dict() # create the word dictionary for autocorrection
word_frequency    = count_frequency(word_list) # compute word frequency
display_time_used = True # enable time display feature
medium_time       = time() - start_Time # time used to create the unique-words list

print("The program took {:0.3f} sec to set it up".format(medium_time))
print("*" * 50)
