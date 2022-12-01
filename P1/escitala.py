from io import TextIOWrapper
from math import floor
from time import sleep

def file_printing(fileOut, result):
    fileOut.write("\n------------------------------------------------------------------------------\n")
    fileOut.write("------------------------------------------------------------------------------\n")
    fileOut.write("".join(result))
    fileOut.write("\n------------------------------------------------------------------------------\n")
    fileOut.write("------------------------------------------------------------------------------\n")

def normal_printing(result):
    print("\n------------------------------------------------------------------------------\n")
    print("\n------------------------------------------------------------------------------\n")
    print("".join(result))
    print("\n------------------------------------------------------------------------------\n")
    print("\n------------------------------------------------------------------------------\n")

    sleep(3)

# Stack overflow

def encrypt(rows, plaintext):
    assert len(plaintext) % rows == 0
    n = len(plaintext)
    columns = n // rows
    ciphertext = ['-'] * n
    for i in range(n):
        row = i // columns
        col = i % columns
        ciphertext[col * rows + row] = plaintext[i]
    return "".join(ciphertext)

def decrypt(rows, ciphertext):
    try:
        assert len(ciphertext) % rows == 0
        return encrypt(len(ciphertext) // rows, ciphertext)
    except AssertionError:
        return None

# MAIN

fileCr = open('escitala.txt', 'r')
fileOut: TextIOWrapper = open('escitala_out', 'w')
fileOut.flush()

x: str = fileCr.read()
chunks = len(x)

# Algorithm

for j in range(1,1000):

    result = decrypt(j, x)
    if result is not None:
        file_printing(fileOut, result) 
    
fileOut.close()
fileCr.close()
