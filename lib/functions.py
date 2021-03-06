import sys
sys.path.insert(1, '/home/tonycueva/UTEC/CoordConv')


from math import trunc, sin, log, atan, sqrt
from lib.classes import Angle

def toDecimal(angle):
    return round(angle[0] + angle[1]/60 + angle[2]/3600, 6)

def toUTM(lat, long, ellip):
    lat = Angle(lat)
    long = Angle(long)

    huso = trunc(long.deg/6 + 31)
    Δlong= Angle(long.deg - huso * 6 + 183)

    A = lat.cos*Δlong.sin
    v = ellip.c * 0.9996 / sqrt(1 + ellip.ep2 * lat.cos2)

    ξ = 0.5 * log((1 + A)/(1 - A))
    ζ = ellip.ep2/2 * ξ**2 * lat.cos2  
    η = atan(lat.tan/Δlong.cos) - lat.rad
    α = 0.75 * ellip.ep2
    β = 5/3 * α**2
    γ = 35/27 * α**3

    A1 = sin(2*lat.rad)
    A2 = A1 * lat.cos2

    J2 = lat.rad + 0.5*A1
    J4 = 0.25 * (3*J2 + A2)
    J6 = (5*J4 + A2*lat.cos2)/3

    B = 0.9996 * ellip.c * (lat.rad - J2*α + J4*β - J6*γ)
    
    E = ξ * v * (1 + ζ/3) + 500000
    N = η * v * (1+ζ) + B

    if(lat.rad < 0):
        N+=  + 10**7


    return(round(E,4),round(N,4), huso)


def toCART(lat, long, h, ellip):
    lat = Angle(lat)
    long = Angle(long)
    
    N = ellip.a / (1 - ellip.e2 * lat.sin2)**0.5

    X = (N + h) * lat.cos * long.cos
    Y = (N + h) * lat.cos * long.sin    
    Z = (N * (1 - ellip.e2) + h) * lat.sin
    
    return (round(X,4),round(Y,4),round(Z,4))
