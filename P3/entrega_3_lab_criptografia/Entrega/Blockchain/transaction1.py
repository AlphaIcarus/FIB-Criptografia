from rsa1 import rsa_public_key

class transaction:
    '''
        genera una transaccion firmando "message" con la clave "RSAkey"
      '''
    def __init__(self, message, RSAkey):
        self.public_key = rsa_public_key(RSAkey)
        self.message = message
        self.signature = RSAkey.sign(message)  


    '''
        Salida: el booleano True si "signature" se corresponde con la
        firma de "message" hecha con la clave RSA asociada a la clave
        publica RSA;
        el booleano False en cualquier otro caso.
    '''
    def verify(self):
        return self.public_key.verify(self.message, self.signature)