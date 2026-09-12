# Toolkit for exploration of the Lebesgue 
# measure-preserving-transformation association with the
# Chebyshev polynomials

from math import pi, sin, cos, asin, acos, tan, floor

def sgn(x):
    return (x > 0) - (x < 0)

def wj(u, j, m):
    return acos(u) + pi*2*j/m

def coefsum(uk, trigfun, m):
    return sum([sgn(sin(wj(uk,j,m)))*trigfun(pi*2*j/m) for j in range(m)])

def chebyCoefmark1(m):
    """
    Signed coefficients on u and sqrt(1-u**2) in ChebyshevMPT of order m.
    """   
    roots = [-cos(pi*(j+0.5)/m) for j in range(m)]
    coef1 = [((-1)**k)*coefsum(roots[k], cos, m) for k in range(m)]
    coef2 = [((-1)**k)*coefsum(roots[k], sin, m) for k in range(m)]
    return [coef1, coef2]

def coefsummark2(k, trigfun, m):
    wjm = [floor(((k+0.5) - 2*j)/m) for j in range(m)]
    return sum([(-1)**wjm[j]*trigfun(pi*2*j/m) for j in range(m)])


def chebyCoefmark2(m):
    """
    Signed coefficients on u and sqrt(1-u**2) in ChebyshevMPT of order m.
    """   
    coef1 = [((-1)**k)*coefsummark2(k, cos, m) for k in range(m)]
    coef2 = [((-1)**k)*coefsummark2(k, sin, m) for k in range(m)]
    return [coef1, coef2]

# This works only for odd m
def chebyCoefmark3odd(m):
    """
    Signed coefficients on u and sqrt(1-u**2) in ChebyshevMPT of order m.
    """   
    coef1 = [((-1)**k)*(cos(pi*k/m) + sin(pi*k/m)/tan(pi/(2*m))) for k in range(m)]
    coef2 = [((-1)**k)*(sin(pi*k/m) - cos(pi*k/m)/tan(pi/(2*m))) for k in range(m)]
    return [coef1, coef2]

def chebyCoefmark3even(m):
    """
    Signed coefficients on u and sqrt(1-u**2) in ChebyshevMPT of order m.
    """   
    ell = [2*floor(k/2) for k in range(m)]
    coef1 = [2*((-1)**k)*(cos(pi*ell[k]/m) + sin(pi*ell[k]/m)/tan(pi/(m))) for k in range(m)]
    coef2 = [2*((-1)**k)*(sin(pi*ell[k]/m) - cos(pi*ell[k]/m)/tan(pi/(m))) for k in range(m)]
    return [coef1, coef2]

def chebyCoef(m):
    """
    Signed coefficients on u and sqrt(1-u**2) in ChebyshevMPT of order m.
    """   
    xi = 2 - (m % 2)  # 1 if odd, two if even
    ell = [xi*floor(k/xi) for k in range(m)]
    c = [xi*((-1)**k)*(cos(pi*ell[k]/m) + sin(pi*ell[k]/m)/tan(xi*pi/(2*m))) for k in range(m)]
    s = [xi*((-1)**k)*(sin(pi*ell[k]/m) - cos(pi*ell[k]/m)/tan(xi*pi/(2*m))) for k in range(m)]
    return c, s

# def rotateCoef(cs):
#     c = cs[0]
#     s = cs[1]
#     const = [math.sqrt(c[k]**2+s[k]**2) for k in range(len(c))]
#     rot = [math.atan(s[k]/c[k]) for k in range(len(c))]
#     return const, rot

class ChebyshevMPT:
    def __init__(self, order):
        self.order = order
        self.xi = 2 - (self.order % 2)
        self.norm = self.xi/sin(self.xi*pi/(2*self.order))
        self.c, self.s = chebyCoef(order)
        self.extrema = [-cos(pi*k/order) for k in range(order+1)]
   
    def S(self, u):
        theta = acos(u)
        ku = theta*self.order/pi
        if abs(ku-round(ku))<1e-9:
            return float((-1) ** round(ku))
        region = min(max(floor(ku),0),self.order-1) # clamp it
        val = (self.c[region]*u + 
                self.s[region]*((1-u**2)**0.5) + 1 - self.xi)
        return val

    # circle map rotation for region kappa
    def rotation(self,kappa):
        return pi*(1/2 + floor(kappa/self.xi))*self.xi/self.order

    # Following assumes that theta in [0,2pi]
    def circlemap(self, theta):
        kappa = floor(theta*self.order/pi)
        return ((-1)**kappa)*self.norm*sin(self.rotation(kappa) - theta)

    def Scm(self,u):
        return self.circlemap(acos(u))+1-self.xi

    def Scmprime(self,u):
        theta = acos(u)
        kappa = floor(theta*self.order/pi)
        return ((-1)**kappa)*self.norm*cos(self.rotation(kappa) - theta)/sin(theta)

    def Sinverse(self,y):
        z = asin((y+self.xi-1)/self.norm)
        return [cos(self.rotation(k) - ((-1)**k)*z) for k in range(self.order)]

    def FP(self, f, x):
        z = self.Sinverse(x)
        Pf = 0
        for zk in z:
            Pf += f(zk)/abs(self.Scmprime(zk))
        return Pf
    

