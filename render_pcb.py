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
import pcons
from pcons import Pad
# TODO: Get the soldermask and clearance into the Pad object

def render_pad( pad ):
    # Need to work out the longest dimension
    dims = ( pad.tr.x.val - pad.bl.x.val,
             pad.bl.y.val - pad.tl.y.val )

    if dims[0] > dims[1]:
        "Draw the pad in the x-direction"
        thickness = dims[1] / 2

        r1 = ( pad.bl.x.val + thickness,
               pad.bl.y.val - thickness )

        r2 = ( pad.br.x.val - thickness,
               pad.bl.y.val - thickness )

    elif dims[0] < dims[1]:
        "Draw the pad in the y-direction"
        thickness = dims[0] / 2

        r1 = ( pad.bl.x.val + thickness,
               pad.bl.y.val - thickness )

        r2 = ( pad.bl.x.val + thickness,
               pad.tr.y.val + thickness )
    else:
        raise Exception( "Square pads are not yet supported :-(" )

    print """\tPad[ %smm %smm %smm %smm %smm %smm %smm "%s" "%s" "square"]""" % (
        r1[0], r1[1], r2[0], r2[1], thickness*2,
        pad.clearance * 2, pad.mask_clearance + thickness*2,
        pad.name, pad.name )

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
}

def render( des ):
    print """Element[0x00 "%s" "" "" 0 0 0 0 0 100 0x00000000]""" % des.desc
    print "("

    for obj in des.ents:
        rendered = False

        for k,r in renderers.iteritems():
            if isinstance( obj, k ):
                r( obj )
                rendered = True
                break

        if not rendered:
            raise Exception("No renderer for object.")

    print ")"



