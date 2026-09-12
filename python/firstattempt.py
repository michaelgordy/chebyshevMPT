# Toolkit for exploration of the Lebesgue 
# measure-preserving-transformation association with the
# Chebyshev polynomials

import math
#from pandas import cut

def sgn(x):
    return (x > 0) - (x < 0)

def wj(u, j, m):
    return math.acos(u) + math.pi*2*j/m

def coefsum(uk, trigfun, m):
    return sum([sgn(math.sin(wj(uk,j,m)))*trigfun(math.pi*2*j/m) for j in range(m)])

def chebyCoef(m):
    """
    Coefficients on u and sqrt(1-u**2) in ChebyshevMPT of order m.
    """   
    roots = [-math.cos(math.pi*(j+0.5)/m) for j in range(m)]
    coef1 = [coefsum(roots[k], math.cos, m) for k in range(m)]
    coef2 = [coefsum(roots[k], math.sin, m) for k in range(m)]
    return [coef1, coef2]

def chebysignedCoef(m):
    """
    Signed coefficients on u and sqrt(1-u**2) in ChebyshevMPT of order m.
    """   
    roots = [-math.cos(math.pi*(j+0.5)/m) for j in range(m)]
    coef1 = [((-1)**k)*coefsum(roots[k], math.cos, m) for k in range(m)]
    coef2 = [((-1)**k)*coefsum(roots[k], math.sin, m) for k in range(m)]
    return [coef1, coef2]

class ChebyshevMPT:
    def __init__(self, order):
        self.order = order
        self.coefficients = chebyCoef(order)
        self.signedcoefficients = chebysignedCoef(order)
        self.extrema = [-math.cos(math.pi*k/order) for k in range(order+1)]
   
    def S(self, u):
        theta = [math.acos(uu) for uu in u]
        region = [math.floor(self.order*t/math.pi) for t in theta]
        region = [min(max(r,0),self.order-1) for r in region]  # clamp it
        sgn_leading = [sgn(math.sin(self.order*t)) for t in theta]
        val = [sgn_leading[k]*self.coefficients[0][region[k]]*u[k] + 
                sgn_leading[k]*self.coefficients[1][region[k]]*((1-u[k]**2)**0.5) + 
                (self.order % 2) - 1 for k in range(len(u))]
        return val
    
    def S1(self, u):
        theta = math.acos(u)
        ku = theta*self.order/math.pi
        if abs(ku-round(ku))<1e-9:
            return float((-1) ** round(ku))
        region = min(max(math.floor(ku),0),self.order-1) # clamp it
        val = (self.signedcoefficients[0][region]*u + 
                self.signedcoefficients[1][region]*((1-u**2)**0.5) + 
                (self.order % 2) - 1) 
        return val
