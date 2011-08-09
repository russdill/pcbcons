#!/usr/bin/env python
from pcons import Point, FixedDist, X, Y, Pad, Align
from pcons import Val as V
from decimal import Decimal as D
import pcons
import render_pcb

des = pcons.Design("test")

pads = des.add_pad_array( (D(10), D(20)),
                          names = [ "apple", "orange" ],
                          direction = pcons.X,
                          pitch = D(12) )

des.set_origin( pads[0].bl )

des.resolve()
render_pcb.render(des)

