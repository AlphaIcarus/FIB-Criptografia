# Imports
from subprocess import run
from time import sleep
import hashlib

# Utils

# Functions
def execute():

    run(["cat", "1.bin", "2.bin", "3.bin", "4.bin", ">", "mensaje.bin"])

    message_file = open("mensaje.bin", "r")
    message = message_file.read()

    preambulo = "20" * 64
    preambulo += "...L...H0F.!.......o..O.....cOS.....,..X$D~'..!....Mio>Xm.....}.....#O.5..R.K..u"
    preambulo += "00"

    sha256 = hashlib.sha256()
    sha256.update(message)
    message256 = sha256.hexdigest()

    sha256.update(preambulo + message256)
    m = sha256.hexdigest()
    
    mfile = open("m.txt", "w")
    mfile.flush()
    mfile.write(m)

    message_file.close()
    mfile.close()

    return

# Main
if __name__ == "__main__":
    execute()

