#!/usr/bin/env python3
###
### PASSWORD CRACKER
###
### Takes in hashed passwords, a minimum length, and a set of possible
### characters, and tries character combinations until the password is
### discovered.
###
### Comp 27: How Systems Fail
### C.R. Calabrese, February 2021
###
### Usage: passwd.py hash_file.txt
###
### Notes: MD5 is the fastest hash algorithm, and isn't very secure.
###        For the purposes of this exercise, we'll start with that,
###        but if we want things to go more slowly, we could rehash
###        our sample passwords using SHA512.
###

import sys, cmd, hashlib, json, time, itertools

min_length     = 0
max_length     = 16
alphabet       = ''
word_list      = {}
out_file       = {}

######## ALPHABET PRE-SETS ########
digits    = "0123456789"
lowercase = "abcdefghijklmnopqrstuvwxyz"
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
symbols1  = "!@#$%^&*., ?-_"
symbols2  = "=+`~()[]|\\\{\};:<>/'\""

# min_length = json.load(open(sys.argv[2]))['min-chars']
# char_set   = ''
# for char in json.load(open(sys.argv[2]))['char-set'] :
#     char_set += char


def main(args):
    if (len(args) < 2) :
        print("USAGE: python3 passwd.py hash_file")
        exit(1)

    setup()

    to_crack = open(args[1], "r")

    for line in to_crack:
        start = time.perf_counter()
        print("cracking: ", line.strip('\n'))
        result = crack_one_password(line.strip('\n'))
        if result != '':
            print("The password is", result, ". Cracked in",
                  time.perf_counter() - start, "seconds.\n")
            if out_file:
                out_file.write(line.strip('\n') + " ==> " + result + '\n')
        else:
            print("Failed to crack the password. The attempt took",
                  time.perf_counter() - start, "seconds.\n")

    return 0

# takes in a hashed (MD5) password and tries combinations until
# it discovers the password.
def crack_one_password(hashed):
    # First, try the word list if they provided one
    if word_list:
        word_list.seek(0)
        print("Trying the passwords in your word list...")
        for line in word_list:
            guess = ''.join(line.strip('\n')).encode('ascii')
            if hashlib.md5(guess).hexdigest() == hashed:
                return guess.decode('ascii')

    # Now try every possible combination
    for passwd_len in range(min_length, max_length + 1):
        print("trying passwords of length ", passwd_len, "...")
        # we'll use itertools product to get all possible combinations
        for guess in itertools.product(alphabet, repeat=passwd_len):
            guess = ''.join(guess).encode('ascii')
            if hashlib.md5(guess).hexdigest() == hashed:
                return guess.decode('ascii')

    return ""

# prompts the user for information about the types of passwords to crack.
def setup():
    global min_length, max_length, alphabet, word_list, out_file
    global digits, lowercase, uppercase, symbols1, symbols2
    print("Welcome to the COMP 27 official password cracker!")
    print("I need some information about the types of passwords you are",
          " trying to crack:")
    print("First, let's build the alphabet of possible characters.")
    print("Do the passwords include...")

    if input("Numbers? [y/n] ") == 'y' :
        alphabet = alphabet + digits
    if input("Lowercase letters? [y/n] ") == 'y' :
        alphabet = alphabet + lowercase
    if input("Uppercase letters? [y/n] ") == 'y' :
        alphabet = alphabet + uppercase
    if input("The following symbols? !@#$%^&*,.?-_ [y/n] ") == 'y':
        alphabet = alphabet + symbols1
    if input("Any other symbols? [y/n] ") == 'y' :
        alphabet = alphabet + symbols2

    ## TO-DO: Add custom alphabet input ##

    print("Great! So, your alphabet is")
    print(alphabet)

    min_length = int(input("Now, what is the minimum length for a password? "))
    max_length = int(input("And the maximum length? "))

    print("We're looking for passwords from", min_length, "to", max_length,
          "characters.")
    print("Do you have a word list you'd like to",
          "use? If so, please type the filepath. If not, please type N/A:")
    word_list_name = input()
    if word_list_name != "N/A" :
        word_list = open(word_list_name, "r")
    print("Finally, would you like the results to be appended to an output",
          "file? If so, please type the filepath. If not, please type N/A:")
    out_file_name = input()
    if out_file_name != "N/A":
        out_file = open(out_file_name, "a")
    print("We're all set! Happy hacking!")


if __name__ == '__main__':
    main(sys.argv)

