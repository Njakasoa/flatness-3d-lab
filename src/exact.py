"""Ordered Q(sqrt(d)), d=2 or 3. No floating-point proof decisions."""
from dataclasses import dataclass
from fractions import Fraction as F
from functools import total_ordering


@total_ordering
@dataclass(frozen=True, eq=False)
class Q:
    a: F = F(0)
    b: F = F(0)
    d: int = 2

    def __post_init__(self):
        if isinstance(self.a, float) or isinstance(self.b, float):
            raise TypeError('Float input is not an exact body; use explicit rationalization')
        if self.d not in (2, 3):
            raise ValueError('Only Q(sqrt(2)) and Q(sqrt(3)) are supported')
        object.__setattr__(self, 'a', F(self.a))
        object.__setattr__(self, 'b', F(self.b))
        if not self.b:
            object.__setattr__(self, 'd', 2)

    def pair(self, other):
        other = other if isinstance(other, Q) else Q(other)
        if self.b and other.b and self.d != other.d:
            raise ValueError('Mixed quadratic fields are unsupported')
        return other, self.d if self.b else other.d

    def __add__(self, other):
        other, d = self.pair(other)
        return Q(self.a + other.a, self.b + other.b, d)
    __radd__ = __add__
    def __neg__(self): return Q(-self.a, -self.b, self.d)
    def __sub__(self, other): return self + (-Q.coerce(other))
    def __rsub__(self, other): return Q.coerce(other) + (-self)
    def __mul__(self, other):
        other, d = self.pair(other)
        return Q(self.a*other.a+d*self.b*other.b, self.a*other.b+self.b*other.a, d)
    __rmul__ = __mul__
    def __truediv__(self, other):
        other, d = self.pair(other)
        den = other.a**2 - d*other.b**2
        if not den: raise ZeroDivisionError
        return self * Q(other.a/den, -other.b/den, d)
    def __rtruediv__(self, other): return Q.coerce(other) / self
    def sign(self):
        a, b = self.a, self.b
        if not b: return (a > 0) - (a < 0)
        if not a: return (b > 0) - (b < 0)
        if (a > 0) == (b > 0): return 1 if a > 0 else -1
        cmp = (a*a > self.d*b*b) - (a*a < self.d*b*b)
        return cmp if a > 0 else -cmp
    def __eq__(self, other):
        if not isinstance(other, (Q, int, F)): return False
        return (self - other).sign() == 0
    def __lt__(self, other): return (self - other).sign() < 0
    def __hash__(self):
        return hash(self.a) if not self.b else hash((self.a,self.b,self.d))
    def __bool__(self): return bool(self.a or self.b)
    def __abs__(self): return -self if self.sign() < 0 else self
    def __float__(self): return float(self.a)+float(self.b)*self.d**0.5
    def floor(self):
        # sqrt(d)<d gives an integer bracket using rational arithmetic only.
        lo = (self.a - abs(self.b)*self.d).__floor__() - 1
        hi = (self.a + abs(self.b)*self.d).__ceil__() + 1
        while hi - lo > 1:
            mid = (hi + lo)//2
            if self < mid: hi = mid
            else: lo = mid
        return lo
    def ceil(self): return -(-self).floor()
    def integer(self): return not self.b and self.a.denominator == 1
    def __str__(self):
        return str(self.a) if not self.b else f'({self.a})+({self.b})*sqrt({self.d})'
    def json(self): return {'a':str(self.a),'b':str(self.b),'d':self.d}
    @staticmethod
    def coerce(x): return x if isinstance(x,Q) else Q(x)
    @staticmethod
    def from_json(x): return Q(x['a'],x['b'],x['d'])


def dot(a,b): return sum((x*y for x,y in zip(a,b)),Q())
def sub(a,b): return tuple(x-y for x,y in zip(a,b))
def transpose(a): return list(map(list,zip(*a)))
def determinant(a):
    n=len(a)
    if n==0: return Q(1)
    if n==1: return Q.coerce(a[0][0])
    return sum(((-1)**j*a[0][j]*determinant([r[:j]+r[j+1:] for r in a[1:]]) for j in range(n)),Q())
def inverse(a):
    n=len(a); det=determinant(a)
    if not det: raise ValueError('Singular matrix')
    return [[(-1)**(i+j)*determinant([r[:i]+r[i+1:] for k,r in enumerate(a) if k!=j])/det for j in range(n)] for i in range(n)]
def matvec(a,v): return tuple(dot(r,v) for r in a)
def matmul(a,b): return [[dot(r,c) for c in zip(*b)] for r in a]
