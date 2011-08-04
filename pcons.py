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

class Pad(object):
    # Corners.  Bottom left, bottom right, top left, top right.
    BL, BR, TL, TR = 0,1,2,3

    def __init__(self, size):
        self.cons = []
        self.size = size

        # Initialise with four unknown corner points
        c = self.corners = [ Point( (Val(), Val()) ) for x in range(0,4) ]

        # Constrain corners to be in-line
        self.cons.append( FixedDist( D(0), c[self.BL].x, c[self.TL].x ) )
        self.cons.append( FixedDist( D(0), c[self.BR].x, c[self.TR].x ) )
        self.cons.append( FixedDist( D(0), c[self.BL].y, c[self.BR].y ) )
        self.cons.append( FixedDist( D(0), c[self.TL].y, c[self.TR].y ) )

        # Space left-hand-side from right
        self.cons.append( FixedDist( size[X], c[self.BL].x, c[self.BR].x ) )
        # Space top from bottom
        self.cons.append( FixedDist( size[Y], c[self.TL].y, c[self.BL].y ) )

    def __repr__(self):
        return "Pad( %s, %s, %s, %s )" % tuple(self.corners)

def filter_cons(t):
    cons = []

    for i in t:
        cons += i.cons
    return cons

def resolve( objects, constraints ):
    unsat = []
    unsat += constraints
    unsat += filter_cons(objects)

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

# The origin
O = Point( (Val(0),Val(0)) )

def set_origin( point ):
    l = []

    l.append( FixedDist( 0, point.x, O.x ) )
    l.append( FixedDist( 0, point.y, O.y ) )
    return l

    
