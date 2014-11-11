from time import time

def read_into_list():
    """This function reads the file 'big.txt' into a list."""
    everyword = [] #create a empty list to save everyword in the file
    with open("big.txt") as wordbase:
        lines = wordbase.readlines()
        for line in lines:
            words = line.split()
            everyword += words
    if include_extra_words == True:
        with open("word_list.txt") as wordbase_2:
            words_2 = wordbase_2.read().splitlines()
            #for line in lines:
            #    words = line.split()
            everyword += words_2
    return everyword

def removable(char):
    """This function is used to judge whether the character should be removed"""
    return not char.isalpha() and not char == "'"

def remove_characters(word_list):
    """This function remove all non-alphabetical characters of the given word list"""

    for i in range(len(word_list)):
        word_list[i] = word_list[i].lower()
        word_list[i] = "".join(char for char in word_list[i] if char.isalpha())
    #    for j in range(len(word_list[i])):
    #        if word_list[i][j] == "'" and j != -2:
    #            word_list[i] = word_list[:j] + word_list[j+1:]
    return word_list

def create_dict():
    """This function create the finalised word list for autocorrection"""

    word_list = read_into_list()
    global alpha_word_list
    alpha_word_list = remove_characters(word_list)
    unique_words = set(alpha_word_list)
    unique_words.remove("")
    print("There are a total of {:d} words in the dictionary".format(len(unique_words)))
    return unique_words

def count_frequency(word_list):
    """This function counts the word frequency of a given word list."""

    frequency = {} # create a dictionary to map words to their frequency

    for word in word_list:
        if word in frequency:
            frequency[word] += 1
        else:
            frequency[word] = 1

    return frequency

def possible_wrong_characters(word):

    #here I assume the probability of typing a correct character is 80%
    #then a possible_wrong_characters is set as the bound of word_distance
    if len(word) <= 4:
        possible_wrong_characters = min(int(len(word) * 0.1 + 1), 3)
    else:
        possible_wrong_characters = min(int(len(word) * 0.2 + 1), 3)

    return possible_wrong_characters

def word_distance(word_to_correct, word_in_dict, possible_wrong_characters):
    """This function is used to determine the word distance between two words"""

    #Levenshtein distance is used in this function to determine word distance

    #special cases
    #the levenshtein distance is at least the difference in size of the two strings.
    if abs(len(word_to_correct) - len(word_in_dict)) > possible_wrong_characters:
        return possible_wrong_characters + 1
    elif len(word_to_correct) == len(word_in_dict):
        # if the length of the two string are the same
        # we can compute the hamming distance instead
        # of levenshtein distance
        if word_to_correct != word_in_dict:
            hamming_distance = 0
            for char1, char2 in zip(word_to_correct, word_in_dict):
                if char1 != char2:
                    hamming_distance += 1
                else:
                    pass
                if hamming_distance > possible_wrong_characters:
                    return possible_wrong_characters + 1
                    break
                else:
                    pass
            return hamming_distance
        # word distance of two identical strings is 0
        else:
            return 0

    #since none of the words in the dictionary is empty string
    #we may skip the case where len(word_in_dict) == 0
    elif len(word_to_correct) == 0:
        return len(word_in_dict)
    #normal case where we have to compute the word distance
    else:
        #create two lists to store the previous and current rows of distances
        d_prev_row = []
        d_curr_row = []

        #initialize previous row of distances
        d_prev_row = range(len(word_in_dict) + 1)
        #calculate current row of distances from previous row of distances
        for i in range(len(word_to_correct)):
            d_curr_row = [i + 1] #first element in d_curr_row is i + 1

            #complete the current row of distances
            for j in range(len(word_in_dict)):
                if word_to_correct[i] == word_in_dict[j]:
                    cost = 0
                else:
                    cost = 1
                d_curr_row.append(min(d_curr_row[j] + 1, d_prev_row[j + 1] + 1, d_prev_row[j] + cost))
            #skip the word if the word distance is bigger than 3
            #if min(d_curr_row) > possible_wrong_characters:
            #    return possible_wrong_characters + 1
            #print(d_curr_row)
            #move current row of distance to previous row of distance for next iteration
            d_prev_row = d_curr_row

        return d_curr_row[-1]

def add_word(word):
    """This fuction is used to add custom words"""

    global unique_words
    unique_words |= {word} # add custom word to the unique word list

def mostlikely(possible_words):
    """This function computes the most likely word in possible autocorrection word list."""

    mostlikely_word   = []
    highest_frequency = 0

    for word in possible_words:
        if word_frequency[word] >= highest_frequency:
            highest_frequency = word_frequency[word]
            mostlikely_word.append(word)
        else:
            pass

    return mostlikely_word[-1]

def print_results(is_correct, possible_words):
    """This function is used to print out the results of autocorrection."""

    #print possible results
    if is_correct:
        print("Your spelling is correct.")
    elif len(possible_words) != 0:
        print("Did you mean: ", end="")
        for i in range(len(possible_words)):
            if i == len(possible_words) - 1:
                print(possible_words[i] + "?")
            elif i == len(possible_words) - 2:
                print(possible_words[i] + ", or ", end="")
            else:
                print(possible_words[i] + ", ", end="")
        # print the most likely word
        if len(possible_words) > 1:
            print("Most likely word is: {:s}".format(mostlikely(possible_words)))
        else:
            pass
    else:
        print("No similar words found.")

def autocorrect(word_to_correct):
    """This function is used to autocorrect given word"""

    time_a          = time()
    word_to_correct = word_to_correct.lower() # change the word to lowercase word
    is_correct      = False # to see whether the word is in the dictionary
    possible_words  = [] # create a list to store possible correction
    typo_limit      = possible_wrong_characters(word_to_correct) # set a upper bound for autocorrection
    if len(word_to_correct) > 4:
        if len(word_to_correct) <= 5:
            for word in unique_words:
                if 0 <= word_distance(word_to_correct[:4], word[:4], typo_limit) <= typo_limit:
                    if 1 <= word_distance(word_to_correct, word, typo_limit) <= typo_limit:
                        possible_words.append(word)
                    elif word_distance(word_to_correct, word, typo_limit) == 0:
                        is_correct = True
                        break
                    else:
                        pass
        else:
            for word in unique_words:
                if 0 <= word_distance(word_to_correct[:4], word[:4], typo_limit) <= possible_wrong_characters(word_to_correct):
                    if 0 <= word_distance(word_to_correct[:5], word[:5], typo_limit) <= typo_limit:
                        if 1 <= word_distance(word_to_correct, word, typo_limit) <= typo_limit:
                            possible_words.append(word)
                        elif word_distance(word_to_correct, word, typo_limit) == 0:
                            is_correct = True
                            break
                        else:
                            pass

    else:
        for word in unique_words:
            if 1 <= word_distance(word_to_correct, word, typo_limit) <= typo_limit:
                possible_words.append(word)
            elif word_distance(word_to_correct, word, typo_limit) == 0:
                is_correct = True
                break
            else:
                pass

    time_b = time() - time_a

    print_results(is_correct, possible_words) # print out the results

    #calculate time used to run the python script
    print("It took {:0.3f} sec to autocorrect".format(time_b))

# codes to be excuted when imported
welcome = """Hi, you are using my autocorrection system!
Before you do anything, let me ask you a question."""

usage = """1. Use autocorrect(\"word\") to autocorrect the word
2. Use add_word(\"word\") to add your own words"""

print("*" * 50)
print(welcome)
print()
print("Do you want to include an extra word list?")
include_extra_words = bool(input("Please input \"yes\" or press <Enter> to skip > "))
print()
print("Ok, that's all I need to know.")
print()
print("=" * 23 + "USAGE" + "=" * 22)
print(usage)
print("=" * 50)
print()

start_Time     = time() # time before the word list is created

unique_words   = create_dict() # create the word dictionary for autocorrection
word_frequency = count_frequency(alpha_word_list) # compute word frequency

medium_time    = time() - start_Time # time used to create the unique-words list
print("The program took {:0.3f} to set it up".format(medium_time))
print("*" * 50)
