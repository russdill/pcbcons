#!/usr/bin/env python
import pcons, render_pcb
from sympy import S

pad_size = ( S(0.65), S(0.6) )

des = pcons.Design("EIA0402")

# Default clearance between copper and pad
des.clearance = S(0.2)

# Default clearance between copper and soldermask
des.mask_clearance = S(0.15)

# Create a row of pads
names = (1, 2)
row = des.add_pad_array( pad_size,
                         names = names,
                         direction = pcons.X,
                         pitch = S(1.0),
                         r = S(0.15) )

# Set origin
des.cons += pcons.MidPoint(row[0].tr, row[1].bl, pcons.O, pcons.XY)

des.resolve()
render_pcb.render(des)
