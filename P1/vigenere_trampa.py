
import numpy as np

if __name__ == '__main__':
    fileCr = open('perm.txt')
    contentCr = fileCr.read()
    for i in range(0, 31): # for each wells file we change the content in order to compare the lengths and see some patterns
        if (i+1) >= 10:
            file = open('wells_' + str(i+1) + '.txt')
        else:
            file = open('wells_0' + str(i+1) + '.txt')
        
        lines = file.readlines()
        result = ""
        for l in lines:
            for c in l:
                valueL = ord(c)
                # we only add the character if it is a letter, otherwise we pass to the next char
                if valueL >= 65 and valueL <= 90: # if it is an uppercase letter, it changes to lowercase letter
                    result = result + chr(valueL + 32)  
                elif valueL >= 97 and valueL <= 122: 
                    result = result + chr(valueL)

        print("Size of file wells " +  str(i+1))
        print("FILE CONTENT LENGTH: ")
        print(len(result))
        print("ENCRYPTED FILE LENGTH: ")
        print(str(len(contentCr)) + "\n")

        fileOut = open('salida_' +  str(i+1) + '.out', 'w')
        fileOut.write(result)
        
        fileOut.close()
        file.close()
    
    fileCr.close()

