#Code taken from https://mattpap.github.io/masters-thesis/html/src/groebner.html

from colors import *
from sympy import *

x=Symbol('x')
y=Symbol('y')

F = [f1, f2] = [x*y - 2*y, x**2 - 2*y**2]

f3 = reduced(s_polynomial(f1, f2), F)[1]
F.append(f3)

#Replace with (f2,f3) and (f1,f3) with the same result. This is Buchbergers criterion (getting a 0 for the remainder).
reduced(s_polynomial(f1,f2),F)[1]


#Play with different monomial orderings (lex, grlex (total degree with ties broken by lex), grevlex(total degree with ties broken by reverse lex))
f1, f2 = [2*x**2*y + x*y**4, x**2 + y + 1]
LT(f1, x, y, order='lex')

LT(f1, x, y, order='grlex')


print bcolors.YELLOW + "Grobner basis for the polynomials:" + str(f1) + ", " + str(f2) +  bcolors.ENDC
print bcolors.BOLD + str(groebner([f1, f2], x, y, order='lex')) + bcolors.ENDC

def monomial_lex_key(monom):
    """Key function for sorting monomials in lexicographic order. """
    return monom

def monomial_grlex_key(monom):
    """Key function for sorting monomials in graded lexicographic order. """
    return (sum(monom), monom)

print bcolors.UNDERLINE + "Special cases of Grobner basis" + bcolors.ENDC
print "#A system of linear equations"
F = [x + 5*y - 2, -3*x + 6*y - 15]

print bcolors.YELLOW + "The system of linear equations is:" + bcolors.ENDC
print bcolors.BOLD + str(groebner(F, x, y)) + bcolors.ENDC

print bcolors.YELLOW + "Euclids algorithm:" + bcolors.ENDC
f = expand((x - 2)**3 * (x + 3)**4 * (x + 7))
g = expand((x + 2)**3 * (x + 3)**3 * (x + 7))

print bcolors.BOLD + str(factor(groebner([f, g])[0])) + bcolors.ENDC

#TODO: LCM example.

print bcolors.UNDERLINE + "Solving system of polynomial equations" + bcolors.ENDC
F = [x*y - 2*y, x**2 - 2*y**2]
print bcolors.YELLOW +"Input polynomials:"+bcolors.ENDC
print F
#Doubt - what does with respect to y mean?
G = groebner(F, wrt=y)
print G

#Doubt - why does G have 6 polynomials indexed by -3 to 2 with the set of 3 repeated twice?
print bcolors.YELLOW + "Roots:" + bcolors.ENDC
print roots(G[2])
#{0:2, 2:1} => x=0 twice and x=2 once.
print bcolors.YELLOW + "=> x=0 twice and x=2 once" + bcolors.ENDC

print bcolors.YELLOW + "substitute them back into the Grobner basis" + bcolors.ENDC
[g.subs(x,0) for g in G]

print groebner([g.subs(x,0) for g in G], y)

print "roots: " + str(roots([g.subs(x,2) for g in G][0]))

print bcolors.YELLOW + "polynomial equations can be solved directly. For example, solution of F:" + bcolors.ENDC
print str(solve(F))



