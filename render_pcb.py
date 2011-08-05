import pcons
from pcons import Pad
# TODO: Get the soldermask and clearance into the Pad object

def render_pad( pad ):
    c = pad.corners

    # Need to work out the longest dimension
    dims = ( c[Pad.TR].x.val - c[Pad.BL].x.val,
             c[Pad.BL].y.val - c[Pad.TL].y.val )

    if dims[0] > dims[1]:
        "Draw the pad in the x-direction"
        thickness = dims[1] / 2

        r1 = ( c[Pad.BL].x.val + thickness,
               c[Pad.BL].y.val - thickness )

        r2 = ( c[Pad.BR].x.val - thickness,
               c[Pad.BL].y.val - thickness )

    elif dims[0] < dims[1]:
        "Draw the pad in the y-direction"
        thickness = dims[0] / 2

        r1 = ( c[Pad.BL].x.val + thickness,
               c[Pad.BL].y.val - thickness )

        r2 = ( c[Pad.BL].x.val + thickness,
               c[Pad.TR].y.val + thickness )
    else:
        raise Exception( "Square pads are not yet supported :-(" )


    print """Pad[ %smm %smm %smm %smm %smm 0.1mm 0.1mm "TODO" "TODO" "square"]""" % (
        r1[0], r1[1], r2[0], r2[1], thickness*2 )

renderers = {
    pcons.Pad: render_pad
}

def render( objects ):
    print """Element[0x00 "Thing" "" "Thing" 0 0 0 0 0 100 0x00000000]"""
    print "("

    for obj in objects:
        for k,r in renderers.iteritems():

            if isinstance( obj, k ):
                r( obj )

    print ")"



