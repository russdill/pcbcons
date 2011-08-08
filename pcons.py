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
from decimal import Decimal as D
X, Y = 0, 1

class Val(object):
    "A value"
    def __init__(self, val = None):
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

class FixedDist(object):
    "Represents a fixed distance constraint between two values"

    def __init__(self, sep, v1, v2):
        "Constrain so that v2 = v1 + sep"
        self.sep = sep
        self.v = (v1,v2)

    def resolvable(self):
        "Return True is it's possible to resolve this"
        if self.v[0].val != None or self.v[1].val != None:
            "We can do something if they're both not None"
            return True

        return False

    def resolve(self):
        "Attempt to resolve this constraint"

        if not self.resolvable():
            "Cannot be satisfied at this time"
            return False

        if self.v[0].val != None and self.v[1].val != None:
            "Both values are already set"

            if self.v[0].val + self.sep != self.v[1].val:
                "This constraint has not been satisfied"
                raise Exception("Unsatisfiable constraint")

            # Contraint already satisfied
            return True

        if self.v[0].val != None:
            self.v[1].val = self.v[0].val + self.sep
        else:
            self.v[0].val = self.v[1].val - self.sep

        return True

def Align( points, axis ):
    "Align all the given items in the specified axis"
    assert axis in (X,Y)
    c = []

    for p in points[1:]:
        c.append( FixedDist( D(0),
                             points[0].pos[axis],
                             p.pos[axis] ) )
    return c

class Pad(object):
    "A rectangular pad"
    def __init__(self, size, name):
        self.cons = []
        self.size = size
        self.name = name

        # Initialise with four unknown corner points
        self.bl, self.br, self.tl, self.tr = [ Point( (Val(), Val()) ) for x in range(0,4) ]

        # Constrain corners to be in-line
        self.cons.append( FixedDist( D(0), self.bl.x, self.tl.x ) )
        self.cons.append( FixedDist( D(0), self.br.x, self.tr.x ) )
        self.cons.append( FixedDist( D(0), self.bl.y, self.br.y ) )
        self.cons.append( FixedDist( D(0), self.tl.y, self.tr.y ) )

        # Space left-hand-side from right
        self.cons.append( FixedDist( size[X], self.bl.x, self.br.x ) )
        # Space top from bottom
        self.cons.append( FixedDist( size[Y], self.tl.y, self.bl.y ) )

    def __repr__(self):
        return "Pad( %s, %s, %s, %s )" % ( self.bl, self.br, self.tr, self.tl )


class Hole(object):
    "A hole in the PCB"
    def __init__(self, diameter):
        self.diameter = diameter
        self.pos = Point( (Val(), Val()) )

    def __repr__(self):
        return "Hole( %s )" % self.pos


# The origin
O = Point( (Val(0),Val(0)) )

class Design(object):
    def __init__(self):
        # Constraints
        self.cons = []

        # Entities
        self.ents = []

    def clearance(self, clearance):
        print "TODO: clearance"

    def mask_clearance(self, mask):
        print "TODO: mask"

    def set_origin(self, point):
        self.cons.append( FixedDist( 0, point.x, O.x ) )
        self.cons.append( FixedDist( 0, point.y, O.y ) )

    def add_hole(self, diam):
        hole = Hole(diam)
        self.ents.append(hole)
        return hole

    def add_pad( self, size, name ):
        pad = Pad( size, name )
        self.ents.append(pad)
        return pad

    def add_pad_array( self, pad_size, names, direction, pitch ):
        pads = [Pad(pad_size, name) for name in names]
        self.ents += pads

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

        satisfied = []
        solved = 1

        while solved > 0 and len(unsat):
            "Loop until there are no more soluble constraints"
            sat = []

            for c in unsat:
                if c.resolve():
                    "Constraint solved"
                    sat.append(c)

            solved = len(sat)
            for c in sat:
                satisfied.append(c)
                unsat.remove(c)

        return len(unsat)
