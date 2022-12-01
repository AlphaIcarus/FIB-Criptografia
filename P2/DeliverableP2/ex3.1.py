from curses import KEY_B2
from Crypto.Cipher import AES
 

def decrypt(key, iv, encryptedText):
    cip = AES.new(key, AES.MODE_OFB, iv)
    return cip.decrypt(encryptedText)
    
if __name__ == '__main__':
    fileInf = open('AES_daniel.moron.roces_2022_09_29_11_10_26.enc', 'rb')
    fileIV = open('AES_daniel.moron.roces_2022_09_29_11_10_26.iv', 'rb')
    fileKey = open('AES_daniel.moron.roces_2022_09_29_11_10_26.key', 'rb')
    
    key = fileKey.read()
    iv =  fileIV.read()
    encryptedText = fileInf.read()

    #3.1 Decrypting the plain text encrypted with mode OFB
    out = open("out", 'wb')
    out.write(decrypt(key, iv, encryptedText))
   
 
    fileInf.close()
    fileIV.close()
    fileKey.close()
    out.close()
  