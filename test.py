from c import *
import string

test_str = ["pxcture", "dunno", "flyy", "comerphenxion", "orginizatin", "infomation",\
            "improv", "hello", "wolrd", "calculu", "thx", "publica", "probbly", "addd"\
            "idex", "errror", "diatance", "coode", "sherlcok", "resset", "prant", "ab"\
            "postture", "wox", "vely", "tcip", "abut"]

with open("old.txt") as wordbase:
    text = wordbase.read()
    words = [word.strip(string.punctuation) for word in text.split()]

test_str += words

total_time = []

for word in test_str:
    time_used = autocorrect(word)
    total_time.append(time_used)

average_time = sum(total_time) / len(test_str)
total_time.sort()
min_time = total_time[0]
max_time = total_time[-1]

print("{:d} words have been tested".format(len(test_str)))
print("min {:f}, avg {:f}, max {:f}".format(min_time, average_time, max_time))
