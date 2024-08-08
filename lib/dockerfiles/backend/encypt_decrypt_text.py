import sys
import os
import random
from collections import defaultdict, Counter

def cryptic(text, process, shifter):
    message = text
    process = process
    shift = shifter
    # print(text, process, shifter)
    while process not in ('encrypt', 'decrypt'):
        process = input("Invalid process. Enter 'encrypt' or 'decrypt': ")
    # shift = int(input("Shift value (1-366) = "))
    while not 1 <= shift <= 366:
        shift = int(input("Invalid value. Enter digit from 1 to 366: "))
    infile = "/home/zamikx/Desktop/sys/zamiks/lib/dockerfiles/backend/txt/story_1.txt"#input("Enter filename with extension: ")
    if not os.path.exists(infile):
        print("File {} not found. Terminating.".format(infile), file=sys.stderr)
        sys.exit(1)        
    text = load_file(infile)
    char_dict = make_dict(text, shift)
    
    if process == 'encrypt':
        ciphertext = encrypt(message, char_dict)
        
        # Run QC protocols and print results.
        if check_for_fail(ciphertext):
            print("\nProblem finding unique keys.", file=sys.stderr)
            print("Try again, change message, or change code book.\n",
                  file=sys.stderr)
            sys.exit()

        print("\nCharacter and number of occurrences in char_dict: \n")      
        print("{: >10}{: >10}{: >10}".format('Character', 'Unicode', 'Count'))
        for key in sorted(char_dict.keys()):
            print('{:>10}{:>10}{:>10}'.format(repr(key)[1:-1],
                                              str(ord(key)),
                                              len(char_dict[key])))
        print('\nNumber of distinct characters: {}'.format(len(char_dict)))
        print("Total number of characters: {:,}\n".format(len(text)))
        
        print("encrypted ciphertext = \n {}\n".format(ciphertext))
        
        # Check the encryption by decrypting the ciphertext.
        print("decrypted plaintext = ")  
        for i in ciphertext:
            print(text[i - shift], end='', flush=True)
        return ciphertext

    elif process == 'decrypt':
        plaintext = decrypt(message, text, shift)
        print("\ndecrypted plaintext = \n {}".format(plaintext))
        return plaintext 
        

def load_file(infile):
    """Read and return text file as a string of lowercase characters."""
    with open(infile) as f:
        loaded_string = f.read().lower()
    return loaded_string

def make_dict(text, shift):
    """Return dictionary of characters as keys and shifted indexes as values."""
    char_dict = defaultdict(list)
    for index, char in enumerate(text):
        char_dict[char].append(index + shift)
    return char_dict

def encrypt(message, char_dict):
    """Return list of indexes representing characters in a message."""
    encrypted = []
    for char in message.lower():
        if len(char_dict[char]) > 1:
            index = random.choice(char_dict[char])
        elif len(char_dict[char]) == 1:  # Random.choice fails if only 1 choice.
            index = char_dict[char][0]
        elif len(char_dict[char]) == 0:
            print("\nCharacter {} not in dictionary.".format(char),
                  file=sys.stderr)
            continue      
        encrypted.append(index)
    return encrypted

def decrypt(message, text, shift):
    """Decrypt ciphertext list and return plaintext string."""
    print(f"shift is {shift}")
    print(message)
    plaintext = ''
    indexes = [s.replace(',', '').replace('[', '').replace(']', '') for s in message.split(',')]
    print("indexes are : ")
    print(indexes)
    for i in indexes:
        print(int(i))
        plaintext += text[int(i) - shift]
    return plaintext

def check_for_fail(ciphertext):
    """Return True if ciphertext contains any duplicate keys."""
    check = [k for k, v in Counter(ciphertext).items() if v > 1]
    if len(check) > 0:
        return True

