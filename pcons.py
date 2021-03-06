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
from sympy import *

X, Y, XY = 0, 1, 2

vals = dict()
def addv(val):
    try:
        for n in val:
            vals[n.val] = n
    except:
        vals[val.val] = val

class capture(object):
    def __init__(self, f):
        self.f = f
    def __call__(self, *args):
        _args = []
        for arg in args:
            if type(arg) == Val:
                vals[arg.val] = arg
                _args.append(arg.val)
            else:
                _args.append(arg)
        return self.f(*_args)

class Val(object):
    "A value"
    def __init__(self, val = None):
        if val is None:
            val = Dummy()
        self.val = val

    def __repr__(self):
        return str(self.val)

class Point:
    "A point in space"
    def __init__(self, pos = None):
        if pos == None:
            self.pos = ( Val(), Val() )
        else:
            self.pos = pos

    @property
    def x(self):
        "x co-ordinate"
        return self.pos[X]

    @x.setter
    def x(self, val):
        self.pos[X] = val

    @property
    def y(self):
        "y co-ordinate"
        return self.pos[Y]

    @y.setter
    def y(self, val):
        self.pos[Y] = val

    def __repr__(self):
        return """Point( %s )""" % ( str(self.pos) )

@capture
def Mid( a, b, c ):
    return (a + b) / S(2) - c

def MidPoint( a, b, c, axis ):
    assert axis in (X,Y,XY)
    ret = []

    for i in X, Y:
        if axis == i or axis == XY:
            ret.append( Mid( a.pos[i], b.pos[i], c.pos[i] ) )

    return ret

@capture
def FixedDist(sep, v1, v2):
    return v1 + sep - v2

def Align( points, axis ):
    "Align all the given items in the specified axis"
    assert axis in (X,Y)
    c = []

    for p in points[1:]:
        c.append( FixedDist( S(0), points[0].pos[axis], p.pos[axis] ) )
    return c

class Pad(object):
    "A rectangular pad"
    def __init__(self, size, name, clearance = 0, mask_clearance = 0, r = S(0)):
        self.cons = []
        self.size = size
        self.name = name
        self.clearance = clearance
        self.mask_clearance = mask_clearance
	self.r = r

        # Initialise with four unknown corner points
        self.bl, self.br, self.tl, self.tr = [ Point( (Val(), Val()) ) for x in range(0,4) ]

        # Constrain corners to be in-line
        self.cons.append( FixedDist( S(0), self.bl.x, self.tl.x ) )
        self.cons.append( FixedDist( S(0), self.br.x, self.tr.x ) )
        self.cons.append( FixedDist( S(0), self.bl.y, self.br.y ) )
        self.cons.append( FixedDist( S(0), self.tl.y, self.tr.y ) )

        # Space left-hand-side from right
        self.cons.append( FixedDist( size[X], self.bl.x, self.br.x ) )
        # Space top from bottom
        self.cons.append( FixedDist( size[Y], self.tl.y, self.bl.y ) )

        # Add a centre point
        self.centre = Point( (Val(), Val()) )
        # And put it in the centre
        self.cons.append( FixedDist( size[X]/2, self.bl.x, self.centre.x ) )
        self.cons.append( FixedDist( size[Y]/2, self.tl.y, self.centre.y ) )

    def __repr__(self):
        return "Pad( %s, %s, %s, %s )" % ( self.bl, self.br, self.tr, self.tl )


class Hole(object):
    "A hole in the PCB"
    def __init__( self, diameter,
                  clearance = 0, mask_clearance = 0 ):
        self.diameter = diameter
        self.pos = Point( (Val(), Val()) )
        self.clearance = clearance
        self.mask_clearance = mask_clearance

    def __repr__(self):
        return "Hole( %s )" % self.pos


class SilkLine(object):
    "A line on the silkscreen"
    def __init__( self, thickness ):
        self.thickness = thickness
        self.start = Point( (Val(), Val()) )
        self.end = Point( (Val(), Val()) )

class SilkCircle(object):
    "A circle on the silkscreen"
    def __init__( self, thickness, diameter ):
        self.thickness = thickness
        self.diameter = diameter
        self.pos = Point()

class SilkRect(object):
    "A silkscreen rectangle made of four lines"
    def __init__( self, thickness ):
        self.thickness = thickness
        self.lines = [ SilkLine(thickness) for x in range(0,4) ]
        # Some things for convenience
        self.t, self.b, self.r, self.l = self.lines
        self.bl = self.b.start
        self.br = self.b.end
        self.tl = self.t.start
        self.tr = self.t.end

        self.cons = []

        # Align everything we can
        self.cons += Align( ( self.t.start,
                              self.l.start, self.l.end,
                              self.b.start ), X )

        self.cons += Align( ( self.t.end,
                              self.r.start, self.r.end,
                              self.b.end ), X )

        self.cons += Align( ( self.t.start, self.t.end,
                              self.l.end,
                              self.r.end ), Y )

        self.cons += Align( ( self.b.start, self.b.end,
                              self.l.start,
                              self.r.start ), Y )

# The origin
O = Point( (Val(0),Val(0)) )

class Design(object):
    def __init__(self, desc):
        self.desc = desc

        # Constraints
        self.cons = []

        # Entities
        self.ents = []

        self.clearance = S(0.2)
        self.mask_clearance = S(0.1)

    def set_origin(self, point):
        self.cons.append( FixedDist( 0, point.x, O.x ) )
        self.cons.append( FixedDist( 0, point.y, O.y ) )

    def add_hole(self, diam,
                 clearance = None, mask_clearance = None ):
        if clearance == None:
            clearance = self.clearance
        if mask_clearance == None:
            mask_clearance = self.mask_clearance

        hole = Hole(diam, clearance = clearance, mask_clearance = mask_clearance)
        self.ents.append(hole)
        return hole

    def add_pad( self, size, name,
                 clearance = None, mask_clearance = None, r = S(0) ):

        if clearance == None:
            clearance = self.clearance
        if mask_clearance == None:
            mask_clearance = self.mask_clearance

        pad = Pad( size, name,
                   clearance = clearance, mask_clearance = mask_clearance, r = r )
        self.ents.append(pad)
        return pad

    def add_pad_array( self, pad_size, names, direction, pitch,
                       clearance = None, mask_clearance = None, r = S(0) ):
        pads = [ self.add_pad( pad_size, name,
                               clearance = clearance,
                               mask_clearance = mask_clearance, r = r ) for name in names ]

        if direction == X:
            perp = Y
        else:
            perp = X

        for i in range(0, len(pads)-1):
            # Sort out the pitch
            self.cons += [ FixedDist( pitch,
                                      pads[i].bl.pos[direction],
                                      pads[i+1].bl.pos[direction] ) ]

        # Align them all in the perpendicular axis
        self.cons += Align( [p.bl for p in pads], perp )

        return pads

    def add_silk_circle( self, thickness, diameter ):
        c = SilkCircle( thickness, diameter )
        self.ents.append( c )
        
        return c

    def add_silk_line( self, thickness ):
        l = SilkLine( thickness )
        self.ents.append( l )

        return l

    def add_silk_rect( self, thickness ):
        "Add a silk rectangle.  Returns the four lines "
        r = SilkRect( thickness )
        self.ents += r.lines
        self.ents += [r]
        return r

    def _filter_obj_cons(self, t):
        "Filter the constraints out of a list of objects"
        cons = []

        for i in t:
            try:
                cons += i.cons
            except AttributeError:
                pass
        return cons
        
    def resolve(self):
        unsat = []
        unsat += self.cons
        unsat += self._filter_obj_cons(self.ents)

        for key, val in solve(unsat).iteritems():
            vals[key].val = val

