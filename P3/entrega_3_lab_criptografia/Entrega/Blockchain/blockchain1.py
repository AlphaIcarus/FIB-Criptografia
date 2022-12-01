import pickle
from random import randint
from hashlib import sha256
from time import time 

from rsa1 import rsa_key
from transaction1 import transaction

# METHODS  
 
def egcd(a,b):
    prevx, x = 1, 0; prevy, y = 0, 1
    while b:
        q = a/b
        x, prevx = prevx - q*x, x
        y, prevy = prevy - q*y, y
        a, b = b, a % b
    return a, prevx, prevy

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
    
def generate_block_chain(file_name, limit):
    print("Generating new Block Chain...")
    now = time()

    # Generating an iterator (only for one use case)
    transactions = list(map(lambda i: transaction(int(sha256(f"hola {i}".encode()).hexdigest(), 16), RSA), range(100)))
    blockChain = block_chain(transactions[0])  #generating the first transaction for the blockChain
    
    f = open(file_name + ".txt", 'w')
    for i in range(0, limit): 
        f.write('Number of block: '  + str(i) + '\n')
        f.write('transaction signature: ' + '\n')
        f.write(str(transactions[i].signature) + '\n')
        f.write('previous block hash: ' + '\n')
        f.write(str(blockChain.list_of_blocks[-1].previous_block_hash) + '\n')
        f.write('block seed: ' + '\n')
        f.write(str(blockChain.list_of_blocks[-1].seed) + '\n')
        f.write('block hash: ')
        f.write(str(blockChain.list_of_blocks[-1].block_hash) + '\n')
        f.write('Verified trans? : ')
        f.write(str(blockChain.list_of_blocks[-1].verify_block()) + '\n')
        f.write('-------------------------------------------------------------------------------------------------\n')

        blockChain.add_block(transactions[i])  

    if limit != 100:
        for x in range(limit, 100):
            f.write('Number of block: '  + str(x) + '\n')
            f.write('transaction signature: ' + '\n')
            f.write(str(transactions[x].signature) + '\n')
            f.write('previous block hash: ' + '\n')
            f.write(str(blockChain.list_of_blocks[-1].previous_block_hash) + '\n')
            f.write('block seed: ' + '\n')
            f.write(str(blockChain.list_of_blocks[-1].seed) + '\n')
            f.write('block hash: ' + '\n')
            f.write(str(blockChain.list_of_blocks[-1].block_hash) + '\n')
            f.write('Verified trans? : ' + '\n')
            f.write(str(blockChain.list_of_blocks[-1].verify_block()) + '\n')
            f.write('-------------------------------------------------------------------------------------------------\n')
            add_wrong_block(blockChain, transactions[x])  # we obtain the rest of transactions and we put into the block chain

    f.close()
    with open(file_name, 'wb') as output_file:
        pickle.dump(blockChain, output_file)

    print(f"File '{file_name}' has been created!\nVerification: {blockChain.verify()}\nTime elapsed: {time() - now}")

def generate_block_hash(block):
    while True:  # For setting a correct seed
        block.seed = randint(0, 2 ** 256)
        aux = str(block.previous_block_hash)
        aux += str(block.transaction.public_key.publicExponent)
        aux += str(block.transaction.public_key.modulus)
        aux += str(block.transaction.message)
        aux += str(block.transaction.signature)
        aux += str(block.seed)
        aux = int(sha256(aux.encode()).hexdigest(), 16)
        if aux < 2 ** (256 - D):
            break
    block.block_hash = aux

def generate_wrong_block_hash(block):
    while True:
        block.seed = randint(0, 2 ** 256)
        aux = str(block.previous_block_hash)
        aux += str(block.transaction.public_key.publicExponent)
        aux += str(block.transaction.public_key.modulus)
        aux += str(block.transaction.message)
        aux += str(block.transaction.signature)
        aux += str(block.seed)
        aux = int(sha256(aux.encode()).hexdigest(), 16)
        if aux > 2 ** (256 - D):
            break
    block.block_hash = aux

def add_wrong_block(blockChain, transaction):
    last_block = blockChain.list_of_blocks[-1]
    new_block = block()
    new_block.transaction = transaction
    new_block.previous_block_hash = last_block.block_hash
    generate_wrong_block_hash(new_block)
    blockChain.list_of_blocks.append(new_block)

# CLASSES 

class block_chain:
    '''
        genera una cadena de bloques que es una lista de bloques,
        el primer bloque es un bloque "genesis" generado amb la transacci´o "transaction"
      '''
    def __init__(self,transaction):
        new_block = block()
        self.list_of_blocks: list[block] = [new_block.genesis(transaction)]

    '''
        a~nade a la cadena un nuevo bloque v´alido generado con la transacci´on "transaction"
    '''
    def add_block(self,transaction):
        new_block = self.list_of_blocks[-1].next_block(transaction)
        self.list_of_blocks.append(new_block)
    ''' 
    verifica si la cadena de bloques es v´alida:
        - Comprueba que todos los bloques son v´alidos
        - Comprueba que el primer bloque es un bloque "genesis"
        - Comprueba que para cada bloque de la cadena el siguiente es correcto
        Salida: el booleano True si todas las comprobaciones son correctas;
        en cualquier otro caso, el booleano False y un entero
        correspondiente al ´ultimo bloque v´alido
      '''
    def verify(self):
        for block in self.list_of_blocks:
            if not block.verify_block():
                return False 
        return True

class block:

    def __init__(self):
        '''
        crea un bloque (no necesariamente v´alido)
        '''
        self.block_hash = None
        self.previous_block_hash = None
        self.transaction = None
        self.seed = None

    
    '''
        genera el primer bloque de una cadena con la transacci´on "transaction"
        que se caracteriza por:
        - previous_block_hash=0
        - ser v´alido
    '''
    def genesis(self,transaction):
        self.previous_block_hash = 0
        self.transaction = transaction
        generate_block_hash(self)
        
        return self
    
    '''
     genera un bloque v´alido seguiente al actual con la transacci´on "transaction"
    '''
    def next_block(self, transaction):
        block_new = block()
        block_new.transaction = transaction
        block_new.previous_block_hash = self.block_hash
        generate_block_hash(block_new)
        
        return block_new
    '''
        Verifica si un bloque es v´alido:
        -Comprueba que el hash del bloque anterior cumple las condiciones exigidas
        -Comprueba que la transacci´on del bloque es v´alida
        -Comprueba que el hash del bloque cumple las condiciones exigidas
        Salida: el booleano True si todas las comprobaciones son correctas;
        el booleano False en cualquier otro caso.
    ''' 
    def verify_block(self):
        is_valid_first = self.previous_block_hash < 2 ** (256-D)
        is_valid_second = self.transaction.verify()
        is_valid_third = self.block_hash < 2 ** (256-D)
        return is_valid_first and is_valid_second and is_valid_third


if __name__ == "__main__":
    print("Generating RSA Key")
    D = 16 
    RSA = rsa_key()
    
    print("Starting Block Chains creation | ETA: 10 - 15 minutes")
    generate_block_chain("output/100_blocks.pickle", 100)
    generate_block_chain("output/100_blocks_valid42.pickle", 42)
