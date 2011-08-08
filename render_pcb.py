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

    print """Pad[ %smm %smm %smm %smm %smm 0.1mm 0.1mm "%s" "%s" "square"]""" % (
        r1[0], r1[1], r2[0], r2[1], thickness*2, pad.name, pad.name )

def render_hole( hole ):
    print """Pin[%smm %smm %smm 0mm 0mm %smm"" "" "hole"]""" % (
        hole.pos.x.val, hole.pos.y.val,
        hole.diameter,
        hole.diameter + 0 )

renderers = {
    pcons.Pad: render_pad,
    pcons.Hole: render_hole
}

def render( objects ):
    print """Element[0x00 "Thing" "" "Thing" 0 0 0 0 0 100 0x00000000]"""
    print "("

    for obj in objects:
        rendered = False

        for k,r in renderers.iteritems():
            if isinstance( obj, k ):
                r( obj )
                rendered = True
                break

        if not rendered:
            raise Exception("No renderer for object.")

    print ")"



