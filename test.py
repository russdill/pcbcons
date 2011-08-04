#!/usr/bin/env python
from pcons import Point, FixedDist, X, Y, Pad, Align
from pcons import Val as V
from decimal import Decimal as D
import pcons

p = Pad( (D(10), D(20)) )
q = Pad( (D(10), D(20)) )

cons = []
cons += pcons.set_origin( p.corners[Pad.BL] )

cons.append( FixedDist( D(50),
                        p.corners[Pad.BL].x,
                        q.corners[Pad.BL].x ) )

cons += Align( [ p.corners[Pad.BL],
                 q.corners[Pad.BL] ], Y )

pcons.resolve( [p,q], cons )

print p
print q


