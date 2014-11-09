from time import time

start_Time = time()

def read_into_list():
    """This function reads the file 'big.txt' into a list."""
    everyword = [] #create a empty list to save everyword in the file
    number_of_words = 0
    with open("big.txt") as wordbase:
        lines = wordbase.readlines()
        for line in lines:
            words = line.split()
            everyword += words
            number_of_words += len(words)
    print("There are a total of {:d} words".format(number_of_words))
    return everyword

def remove_characters(word_list):
    """This function remove all non-alphabetical characters of the given word list"""
    for word in word_list:
        word = word.lower()
        word = "".join(char for char in word if char.isalpha())
    return word_list

word_list = read_into_list()
alpha_word_list = remove_characters(word_list)
unique_words = set(alpha_word_list)
print(len(unique_words))
print("" in unique_words)

#calculate time used to run the python script
net_Time = time() - start_Time
print("It took {:0.3f} sec".format(net_Time))
