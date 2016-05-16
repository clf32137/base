#Code taken from https://mattpap.github.io/masters-thesis/html/src/groebner.html

from sympy import *

def s_polynomial(f, g):
    return expand(lcm(LM(f), LM(g))*(1/LT(f)*f - 1/LT(g)*g))

F = [f1, f2] = [x*y - 2*y, x**2 - 2*y**2]

s_polynomial(f1, f2)

reduced(_, F)[1]

#_ means whatever was computed right before.
f3 = _
F.append(f3)


s_polynomial(f1,f2)

#Replace with (f2,f3) and (f1,f3) with the same result. This is Buchbergers criterion (getting a 0 for the remainder).
reduced(_,F)[1]


def buchberger(F, reduced=True):
    """Toy implementation of Buchberger algorithm. """
    G, pairs = list(F), set([])#Assign G with the input system of polynomial equations, F.

    for i, f1 in enumerate(F):#Generate a set with all (unordered) pairs of polynomials from F. Will be used to verify Buchbergers criterion.
        for f2 in F[i+1:]:
            pairs.add((f1, f2))#A quadratic number of pairs.

    while pairs: #Loops until there are critical pairs to check. If not, Buchbergers criterion is satisfied and you can go home with G, your Grobner basis.
        f1, f2 = pairs.popitem()
        #Compute S-polynomial and reduction as per the current basis.
        s = s_polynomial(f1, f2)
        _, h = reduced(s, G)
        #If the reduction is non-zero, update the set of critical pairs and adjoin to the new element to G.
        if h != 0:
            for g in G:
                pairs.add((g, h))

            G.append(g)
    #When the loop terminates, we get the Grobner basis of F.
    
    if reduced:#If the reduced flag is set, reduce each element of the basis with respect to the other elements and make each element "monic", obtaining a reduced Grobner basis.
        for i, g in enumerate(G):
            _, G[i] = reduced(g, G[:i] + G[i+1:])

        G = map(monic, G)

    return G

#In practice, sympy implements a build-in function which is more efficient.
#It removes useless divisions.

#Play with different monomial orderings (lex, grlex (total degree with ties broken by lex), grevlex(total degree with ties broken by reverse lex))
f1, f2 = [2*x**2*y + x*y**4, x**2 + y + 1]
LT(f1, x, y, order='lex')

LT(f1, x, y, order='grlex')


groebner([f1, f2], x, y, order='lex')

def monomial_lex_key(monom):
    """Key function for sorting monomials in lexicographic order. """
    return monom


