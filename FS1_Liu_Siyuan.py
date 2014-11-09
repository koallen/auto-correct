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
    print("There are a total of {:d}".format(number_of_words))

read_into_list()

#calculate time used to run the python script
net_Time = time() - start_Time
print("It took {:0.3f} sec".format(net_Time))
