from time import time

def read_into_list():
    """This function reads the file 'big.txt' into a list."""
    everyword = [] #create a empty list to save everyword in the file
    with open("big.txt") as wordbase:
        lines = wordbase.readlines()
        for line in lines:
            words = line.split()
            everyword += words
    with open("word_list.txt") as wordbase_2:
        lines = wordbase_2.readlines()
        for line in lines:
            words = line.split()
            everyword += words
    return everyword

def remove_characters(word_list):
    """This function remove all non-alphabetical characters of the given word list"""
    for i in range(len(word_list)):
        word_list[i] = word_list[i].lower()
        word_list[i] = "".join(char for char in word_list[i] if char.isalpha())
    return word_list

def create_dict():
    """This function create the finalised word list for autocorrection"""
    word_list = read_into_list()
    alpha_word_list = remove_characters(word_list)
    unique_words = set(alpha_word_list)
    unique_words.remove("")
    return unique_words

def autocorrect(word_to_correct):
    start_Time = time()
    unique_words = create_dict()
    net_Time = time() - start_Time
    possible_words = []
    if word_to_correct in unique_words:
        print("Your spelling is correct.")
    else:
        for word in unique_words:
            if word[:2] == word_to_correct[:2]:
                if abs(len(word) - len(word_to_correct)) <= 2:
                    possible_words.append(word)
        print("Do you mean ", end="")
        for word in possible_words:
            print(word + ", ", end="")
    #calculate time used to run the python script
    print("It took {:0.3f} sec".format(net_Time))
