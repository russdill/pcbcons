#!/usr/bin/env python
import pcons, render_pcb
from decimal import Decimal as D

pad_size = ( D("0.55"), D("1.5") )
hole_diam = D("0.8")

des = pcons.Design()

# TODO: These aren't yet implemented
# # Default clearance between copper and pad
# des.clearance = D("0.2")

# # Default clearance between copper and soldermask
# des.mask_clearance = D("0.15")

# Create two rows of pads
rows = []
for i in range(0,2):
    names = range(4*i+1,4*i+5)
    if i == 1:
        "Make the names of the second row flow in the opposite direction"
        names.reverse()

    rows.append( des.add_pad_array( pad_size,
                                    names = names,
                                    direction = pcons.X,
                                    pitch = D("0.8") ) )
# Create two holes
holes = []
for i in range(0,2):
    holes += [ des.add_hole( hole_diam ) ]

# Set origin
des.set_origin( rows[0][0].bl )

# Line up the pads in X
des.cons += pcons.Align( (rows[0][0].bl, rows[1][0].bl), pcons.X )

des.cons += [
    # Space the rows in Y
    pcons.FixedDist( D("2.5"),
                     rows[1][0].bl.y,
                     rows[0][0].tl.y ),

    # Put the holes out to the sides
    pcons.FixedDist( D("1"),
                     holes[0].pos.x, 
                     rows[0][0].tl.x ),

    pcons.FixedDist( D("-1"),
                     holes[1].pos.x, 
                     rows[1][3].tr.x )
]

# Give the holes positions in y
des.cons += pcons.Align( (rows[0][0].tl, holes[0].pos), pcons.Y )
des.cons += pcons.Align( (rows[1][0].bl, holes[1].pos), pcons.Y )

des.resolve()
render_pcb.render(des.ents)
