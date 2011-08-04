#!/usr/bin/env python
from pcons import Point, FixedDist, X, Y, Pad
from pcons import Val as V
from decimal import Decimal as D
import pcons

origin = Point( (V(0), V(0)) )

p = Pad( (D(10), D(20)) )
q = Pad( (D(10), D(20)) )

cons = []

cons.append( FixedDist( D(0), p.corners[Pad.BL].pos[X], origin.pos[X] ) )
cons.append( FixedDist( D(0), p.corners[Pad.BL].pos[Y], origin.pos[Y] ) )

cons.append( FixedDist( D(50),
                        p.corners[Pad.BL].pos[X],
                        q.corners[Pad.BL].pos[X] ) )

cons.append( FixedDist( D(0),
                        p.corners[Pad.BL].pos[Y],
                        q.corners[Pad.BL].pos[Y] ) )

pcons.resolve( [p,q], cons )

print p
print q


