#Code taken from https://mattpap.github.io/masters-thesis/html/src/groebner.html

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

from sympy import *

def s_polynomial(f, g):
    return expand(lcm(LM(f), LM(g))*(1/LT(f)*f - 1/LT(g)*g))

x=Symbol('x')
y=Symbol('y')

F = [f1, f2] = [x*y - 2*y, x**2 - 2*y**2]


f3 = reduced(s_polynomial(f1, f2), F)[1]
F.append(f3)

#Replace with (f2,f3) and (f1,f3) with the same result. This is Buchbergers criterion (getting a 0 for the remainder).
reduced(s_polynomial(f1,f2),F)[1]

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


print bcolors.OKBLUE + "Grobner basis for the polynomials:" + bcolors.ENDC
print bcolors.BOLD
print groebner([f1, f2], x, y, order='lex')
print bcolors.ENDC

def monomial_lex_key(monom):
    """Key function for sorting monomials in lexicographic order. """
    return monom

def monomial_grlex_key(monom):
    """Key function for sorting monomials in graded lexicographic order. """
    return (sum(monom), monom)

print bcolors.UNDERLINE + "#############\n#Special cases of Grobner basis\n#############" + bcolors.ENDC
print "#A system of linear equations"
F = [x + 5*y - 2, -3*x + 6*y - 15]

print bcolors.OKBLUE + "The system of linear equations is:" + bcolors.ENDC
print bcolors.BOLD
print groebner(F, x, y)
print bcolors.ENDC

print "Euclids algorithm:"
f = expand((x - 2)**3 * (x + 3)**4 * (x + 7))
g = expand((x + 2)**3 * (x + 3)**3 * (x + 7))

print bcolors.BOLD
print factor(groebner([f, g])[0])
print bcolors.ENDC



#TODO: LCM example.


print bcolors.UNDERLINE + "#############\n#Solving system of polynomial equations\n#############" + bcolors.ENDC
F = [x*y - 2*y, x**2 - 2*y**2]
G = groebner(F, wrt=y)
print G

print roots(G[-1])
