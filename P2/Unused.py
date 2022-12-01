

def xor(a: int, b: int):     # FUNCIONA
    return a ^ b

def xor_p(a: list, b: list):    # FUNCIONA
    return itp(xor(pti(a), pti(b)))

# Funciones buenas:

def pti(b: list):       # FUNCIONA
    """
    Polynomial list to integer

    is of the form x7 + x6 + x5 ... = [1,1,1...]
    """
    sum = 0
    for i in range(0, len(b)):
        if b[i] == 1:
            sum += int(2 ** (len(b)-1-i))

    return sum

def itp(x: int):        # FUNCIONA
    """
    Integer to polynomial

    is of the form x7 + x6 + x5 ... = [1,1,1...]
    """
    pol: list = []

    for i in range(0, 9):
        if x - int(2**(8-i)) >= 0:
            pol.append(1)
            x -= int(2**(8-i))
        else:
            pol.append(0)

    return pol

def prod_X(B: list):    # A PRIORI FUNCIONA
    """
    Polynomial * x

    is of the form x7 + x6 + x5 ... = [1,1,1...]
    """
    B.append(0)

    if pti(B) > 0xFF :
        B = xor_p(B, m_pol)

    while len(B) > 8 and B[0] == 0:
        B.pop(0)
    
    return B

def i_prod_X(B: list, i: int):
    
    res = B
    while i > 0:
        res = prod_X(res)
        i -= 1

    return res