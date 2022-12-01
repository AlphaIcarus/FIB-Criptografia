from pkgutil import extend_path
import galois
from time import time
from komm import BinaryPolynomial

# Utils

# function for extended Euclidean Algorithm
def gcdExtended(a, b):

    if a == 0 :
        return b,0,1

    gcd,x1,y1 = gcdExtended(b%a, a)

    x = y1 - (b//a) * x1
    y = x1
     
    return gcd,x,y

# Functions

def irreducible_polynomials():
    """
    Computes the list of irreductible polynomials of GF(2**8)
    """
    res = []

    for i in range(256, 512):
        aux = []
        for div in range(1,i+1):
            i_pol = BinaryPolynomial(i)
            div_pol = BinaryPolynomial(div)

            r = i_pol % div_pol
            if r == 0:
                aux.append(div)
        if aux.sort() == [1, i]:
            res.append(i)

    return res

def GF_product_p(a: int, b: int):
    """
    Computes the product of a and b in finite field GF(2**8)
    """

    res = 0
    while b > 0:
        if b % 2 != 0:
            res = res ^ a
        a <<= 1
        if a > 0xff:
            a = a ^ m
        b >>= 1
    return res

def GF_es_generador(a: int):
    """
    Returns wether the integer a is generator of the field GF(2**8) or not
    """
    if a == 0:
        return False
    res = 1
    for i in range(1, 256):
        res = GF_product_p(res, a)
        if res == 1:
            if i == 255:
                return True
            else:
                return False
    return False

def GF_tables():
    """
    For a given generator m, computes the exponential table (for every i, exponential[i] = generator**i == a)
    and logarithmic table (for every position a, logarithmic[a] = i)
    """

    gen = 6   # Generador
    global exp
    global log

    exp_res = 1
    exp = []
    for _ in range(1, 256):
        exp.append(exp_res)
        exp_res = GF_product_p(exp_res, gen)
    exp.append(1)

    # Logarithmic
    log_res = 1
    log = [None for _ in range(0, 256)]
    for i in range(0, 255):
        log[log_res] = i
        log_res = GF_product_p(log_res, gen)

    return 

def GF_product_t(a, b):
    """
    Computes the product of two integers a and b using exponential and logarithmic tables
    """
    if a == 0x00 or b == 0x00:
        return 0x00
    else:
        return exp[(log[a] + log[b]) % 255]

def GF_invers(a: int):
    """
    Computes the inverse poly1d of a given a, represented by its integer form
    """
    if a == 0:
        return None
    else:
        return exp[255 - log[a]]

# Test

def property_testing():

    # PROPERTIES TESTS
    for a in range(0,256):
        for b in range(0,256):
            # Property n1
            assert GF_product_p(a, b) == GF_product_t(a, b)
            # Property n2
            assert GF_product_p(a, b) == GF_product_p(b, a)

    for a in range(1,256):
        # Property n3
        assert GF_product_p(a, GF_invers(a)) == 1


def test():

    # Precomputations

    GF_tables()

    print(exp)
    print(log)

    # TESTS

    a = 125

    # TEST 1
    t1 = time()
    p = GF_product_p(a, 0x02)
    tf1 = time() - t1
    t2 = time()
    t = GF_product_t(a, 0x02)
    tf2 = time() - t2
    print("Test número 1: a = " + str(hex(a)) + ", 0x02")
    print(f"Resultado: {p} == {t}")
    print(f"Tiempo: {tf1} vs {tf2}\n")

    # TEST 2
    t1 = time()
    p = GF_product_p(a, 0x03)
    tf1 = time() - t1
    t2 = time()
    t = GF_product_t(a, 0x03)
    tf2 = time() - t2
    print("Test número 2: a = " + str(hex(a)) + ", 0x03")
    print(f"Resultado: {p} == {t}")
    print(f"Tiempo: {tf1} vs {tf2}\n")

    # TEST 3
    t1 = time()
    p = GF_product_p(a, 0x09)
    tf1 = time() - t1
    t2 = time()
    t = GF_product_t(a, 0x09)
    tf2 = time() - t2
    print("Test número 3: a = " + str(hex(a)) + ", 0x09")
    print(f"Resultado: {p} == {t}")
    print(f"Tiempo: {tf1} vs {tf2}\n")

    # TEST 4
    t1 = time()
    p = GF_product_p(a, 0x0b)
    tf1 = time() - t1
    t2 = time()
    t = GF_product_t(a, 0x0b)
    tf2 = time() - t2
    print("Test número 4: a = " + str(hex(a)) + ", 0x0b")
    print(f"Resultado: {p} == {t}")
    print(f"Tiempo: {tf1} vs {tf2}\n")

    # TEST 5
    t1 = time()
    p = GF_product_p(a, 0x0d)
    tf1 = time() - t1
    t2 = time()
    t = GF_product_t(a, 0x0d)
    tf2 = time() - t2
    print("Test número 5: a = " + str(hex(a)) + ", 0x0d")
    print(f"Resultado: {p} == {t}")
    print(f"Tiempo: {tf1} vs {tf2}\n")

    # TEST 6
    t1 = time()
    p = GF_product_p(a, 0x0e)
    tf1 = time() - t1
    t2 = time()
    t = GF_product_t(a, 0x0e)
    tf2 = time() - t2
    print("Test número 6: a = " + str(hex(a)) + ", 0x0e")
    print(f"Resultado: {p} == {t}")
    print(f"Tiempo: {tf1} vs {tf2}\n")


    # PROPERTIES TESTING
    property_testing()

m = 395
GF28 = galois.GF(2**8)

"""Tables"""
exp: list = []
log: list = []

if __name__ == '__main__':
    
    test()