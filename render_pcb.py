# Copyright 2011 Robert Spanton
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import copy
import pcons
from pcons import Pad

def output_pad( x1, y1, x2, y2, thickness, clearance, mask, name, round ):
    print """\tPad[ %smm %smm %smm %smm %smm %smm %smm "%s" "%s" "%s"]""" % (
        x1, y1, x2, y2, thickness*2,
        clearance * 2, mask + thickness*2,
        name, name, "round" if round else "square"  )

def render_square_pad( pad ):
    "pcb doesn't support square pads - so hack it with two rectangles"
    d = pad.tr.x.val - pad.bl.x.val
    assert d == (pad.bl.y.val - pad.tl.y.val)

    thickness = d / 4

    p1 = ( ( pad.tl.x.val + thickness, pad.tl.y.val + thickness ),
           ( pad.tr.x.val - thickness, pad.tl.y.val + thickness ) )

    p2 = ( ( pad.bl.x.val + thickness, pad.bl.y.val - thickness ),
           ( pad.br.x.val - thickness, pad.bl.y.val - thickness ) )

    for p in (p1, p2):
        output_pad( p[0][0], p[0][1], p[1][0], p[1][1],
                    thickness = thickness,
                    clearance = pad.clearance,
                    mask = pad.mask_clearance,
                    name = pad.name )

def render_simple_pad( pad, round = False ):
    # Need to work out the longest dimension
    dims = ( pad.tr.x.val - pad.bl.x.val,
             pad.bl.y.val - pad.tl.y.val )

    thickness = min(dims) / 2

    if dims[0] > dims[1]:
        "Draw the pad in the x-direction"

        r1 = ( pad.bl.x.val + thickness,
               pad.bl.y.val - thickness )

        r2 = ( pad.br.x.val - thickness,
               pad.bl.y.val - thickness )

    elif dims[0] < dims[1] or round:
        "Draw the pad in the y-direction"

        r1 = ( pad.bl.x.val + thickness,
               pad.bl.y.val - thickness )

        r2 = ( pad.bl.x.val + thickness,
               pad.tr.y.val + thickness )
    else:
        render_square_pad(pad)
        return

    output_pad( r1[0], r1[1], r2[0], r2[1],
                thickness = thickness,
                clearance = pad.clearance,
                mask = pad.mask_clearance,
                name = pad.name,
                round = round )

def render_pad( pad ):

    dims = ( pad.tr.x.val - pad.bl.x.val,
             pad.bl.y.val - pad.tl.y.val )

    thickness = min(dims) / 2
    length = max(dims) / 2

    if pad.r > 0 and pad.r < thickness:
        middle_pad = copy.deepcopy( pad )
        middle_pad.tr.x.val -= pad.r
        middle_pad.br.x.val -= pad.r
        middle_pad.tl.x.val += pad.r
        middle_pad.bl.x.val += pad.r
	render_simple_pad( middle_pad )

        left_pad = copy.deepcopy( pad )
        left_pad.br.x.val = left_pad.tr.x.val = left_pad.tl.x.val + pad.r * 2
	render_simple_pad( left_pad, True )

        right_pad = copy.deepcopy( pad )
        right_pad.bl.x.val = left_pad.tl.x.val = left_pad.tl.x.val + pad.r * 2
	render_simple_pad( right_pad, True )

    elif pad.r == thickness:
        render_simple_pad( pad, True )

    elif pad.r == 0:
        render_simple_pad( pad )

    else:
        raise Exception("Invalid r")

def render_hole( hole ):
    print """\tPin[ %smm %smm %smm %smm %smm %smm"" "" "hole"]""" % (
        hole.pos.x.val, hole.pos.y.val,
        hole.diameter,
        hole.clearance * 2, hole.mask_clearance + hole.diameter,
        hole.diameter + 0 )

def render_silk_line( line ):
    print """\tElementLine[ %smm %smm %smm %smm %smm ]""" % (
        line.start.x.val, line.start.y.val,
        line.end.x.val, line.end.y.val,
        line.thickness )

def render_silk_circle( c ):
    print """\tElementArc[ %smm %smm %smm %smm 0 360 %smm ]""" % (
        c.pos.x.val, c.pos.y.val,
        c.diameter, c.diameter,
        c.thickness )

renderers = {
    pcons.Pad: render_pad,
    pcons.Hole: render_hole,
    pcons.SilkLine: render_silk_line,
    pcons.SilkCircle: render_silk_circle,
    pcons.SilkRect: None,
}

def render( des ):
    print """Element[0x00 "%s" "" "" 0 0 0 0 0 100 0x00000000]""" % des.desc
    print "("

    for obj in des.ents:
        rendered = False

        for k,r in renderers.iteritems():
            if isinstance( obj, k ):
                if r != None:
                    r( obj )
                rendered = True
                break

        if not rendered:
            raise Exception("No renderer for object.")

    print ")"



