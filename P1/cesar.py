import codecs
import sys

def computeMinim(text):
    valMin = 0xFF
    for line in text:
        for c in line:
            cval = ord(c)
            if cval >= 126:
                if (cval < valMin):
                    valMin = cval
    
    info = ""
    for line in text:
        for c in line:
            cval = ord(c)
            if cval >= 126:
                if 65 <= valMin:
                    dist = valMin - 65
                else:
                    dist = 65 - valMin        
                newVal = (cval - dist) % 26 + 65
                info = info + chr(newVal)
            else:
                info = info + chr(cval)
    return info

def countFrequency(text):
    d = {}
    for l in text:
        for c in l:
            d[l] = text.count(c)
    return d

def desencryptText(text, freqL):
    result = ""
    for l in text:
        for c in l:
            valueL = ord(c)
            if valueL >= 126:
                if freqL >= valueL:
                    dif = freqL - 69
                else:
                    dif = 69 - freqL 
                if (valueL - dif) < 65:
                    newVal = valueL - dif + 26
                else :
                    newVal = valueL - dif
                result = result + chr(newVal)
            else:
                result = result + c
    print(result.encode("utf-8", "replace").decode("utf-8", "ignore"))

if __name__ == '__main__':
    file = open('cesar.txt')
    lines = file.readlines()
    textMin = computeMinim(lines)
    dicFreq = countFrequency(textMin)
    freqL = max(dicFreq, key=dicFreq.get)
    desencryptText(textMin, ord(freqL))
    file.close()

