import subprocess
import hashlib 

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

cjt =  "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def gen_key():
    for fst_chr in cjt:
        for snd_chr in cjt:
            yield f"{fst_chr * 8}{snd_chr * 8}"


def read_file(path):
    with open(path, 'rb') as file:
        return file.read()


def write_file(path, data):
    with open(path, 'wb') as file:
        file.write(data)


if __name__ == "__main__":
    key_gen = gen_key()
    i = 0
    iter = 0

    while True:
        iter += 1
        try:
            H = hashlib.sha256(next(key_gen).encode()).digest()
            k = H[:16]
            iv = H[16:]

            encText = read_file('AES_daniel.moron.roces_2022_09_20_16_59_19.puerta_trasera.enc')
            aes = AES.new(k, AES.MODE_CBC, iv)
            decText = unpad(aes.decrypt(encText), AES.block_size)
        except ValueError:
            pass
        except StopIteration:
            break
    
        else:
            write_file('aux_dec', decText)
            file_type = subprocess.run(['file', '-b', 'aux_dec'], stdout=subprocess.PIPE)

            if 'data' not in file_type.stdout.decode('utf-8'):
                write_file(f"decripted{i}", decText)
                i += 1