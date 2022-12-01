from time import time
from hashlib import sha256
import Crypto
from Crypto import Random
from Crypto.Util import number

# Generals methods 

def gcd(a,b):
	if b > a:
		if b % a == 0:
			return a
		else:
			return gcd(b % a, a)
	else:
		if a % b == 0:
			return b
		else:
			return gcd(b, a % b)

# Classes
  
class rsa_key:
    '''
        genera una clave RSA (de 2048 bits y exponente p´ublico 2**16+1 por defecto)
    '''
    def __init__(self,bits_modulo=2048,e=2**16+1):
        self.publicExponent = e
        self.bits_modulo = bits_modulo
    
        self.generate_primes_PQ()
        phi_n = (self.primeP - 1) * (self.primeQ - 1)
        self.modulus = self.primeP * self.primeQ

        self.privateExponent = number.inverse(self.publicExponent, phi_n)

        self.inverseQModulusP = number.inverse(self.primeQ, self.primeP)
        self.privateExponentModulusPhiP = number.inverse(self.privateExponent, self.primeP - 1)
        self.privateExponentModulusPhiQ = number.inverse(self.privateExponent, self.primeQ - 1)

    
    def validate_PQ(self):
        phi_n = (self.primeP - 1) * (self.primeQ - 1)
        return gcd(self.publicExponent, phi_n) and self.primeP != self.primeQ
    
    def generate_primes_PQ(self):
        found = 0
        while(found != 1):
            self.primeP = Crypto.Util.number.getPrime(self.bits_modulo, randfunc=Crypto.Random.get_random_bytes) #enter prim de 1024 bits
            self.primeQ = Crypto.Util.number.getPrime(self.bits_modulo, randfunc=Crypto.Random.get_random_bytes) #enter prim de 1024 bits
            found = self.validate_PQ()
	

    '''
        Salida: un entero que es la firma de "message" hecha con la clave RSA usando el TCR
    '''
    def sign(self,message):
     
        ''' p_prime = modinv(self.primeP, self.primeQ)
        q_prime = modinv(self.primeQ, self.primeP)

        a = pow(message, self.privateExponent % (self.primeP-1), self.primeP)
        b = pow(message, self.privateExponent % (self.primeQ-1), self.primeQ)

        x = self.primeQ*q_prime*a + self.primeP*p_prime*b # d^d
        
        return x % self.modulus'''
        d_1 = self.privateExponent % (self.primeP - 1)
        d_2 = self.privateExponent % (self.primeQ - 1)
        p_1 = number.inverse(self.primeP, self.primeQ)
        q_1 = number.inverse(self.primeQ, self.primeP)

        c_1 = pow(message, d_1, self.primeP)
        c_2 = pow(message, d_2, self.primeQ)

        return (c_1 * q_1 * self.primeQ + c_2 * p_1 * self.primeP) % self.modulus
    
    '''
        Salida: un entero que es la firma de "message" hecha con la clave RSA sin usar el TCR
    '''
    def sign_slow(self,message):
        return pow(message, self.privateExponent % ((self.primeP-1)*(self.primeQ-1)), self.modulus)

class rsa_public_key:
    '''
        genera la clave p´ublica RSA asociada a la clave RSA "rsa_key"
    '''
    def __init__(self, rsa_key):
        self.publicExponent = rsa_key.publicExponent
        self.modulus = rsa_key.modulus

    '''
        Salida: el booleano True si "signature" se corresponde con la
        firma de "message" hecha con la clave RSA asociada a la clave
        pública RSA;
        el booleano False en cualquier otro caso.
    '''
    def verify(self, message, signature):
        return pow(signature, self.publicExponent, self.modulus) == message 

if __name__ == "__main__":

    bits_modulo = [512, 1024, 2048, 4096]
    messages = [int(sha256(f"hola {i}".encode()).hexdigest(), 16) for i in range(100)]
    
    output_string = "Bits Modulo,Tiempo con TXR,Tiempo sin TXR\n"

    for modulo in bits_modulo:
        RSA = rsa_key(bits_modulo=modulo)
        
        now = time()
        for message in messages:
            RSA.sign(message)
        time_signatures = time() - now

        now = time()
        for message in messages:
            RSA.sign_slow(message)
        slow_time_signatures = time() - now

        output_string += f"{modulo},{time_signatures},{slow_time_signatures}\n"

        print(f'''
        module: {modulo}
        fast: {time_signatures}
        slow: {slow_time_signatures}
        ''')

    with open("output/tabla_comparativa.csv", "w") as output_file:
        output_file.write(output_string)

