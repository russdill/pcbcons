#!/usr/bin/env python
from pcons import Point, FixedDist, X, Y, Pad, Align
from pcons import Val as V
from decimal import Decimal as D
import pcons
import render_pcb

pads, cons = pcons.pad_array( (D(10), D(20)), 10, X, D(12) )

cons += pcons.set_origin( pads[0].bl )

pcons.resolve( pads, cons )
render_pcb.render( pads )

