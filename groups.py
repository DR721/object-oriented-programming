from numbers import Integral
import numpy as np


class Element:
    def __init__(self, group, value):
        group._validate(value)
        self.group = group
        self.value = value

    def __mul__(self, other):
        return type(self)(self.group, 
                          self.group.operation(self.value, other.value))

    def __str__(self): # human readable output
        return f"{self.value}_{self.group}"

    def __repr__(self): # code used to make the group object
        return f"{type(self).__name__}({self.group!r}, {self.value!r})"
        # do not hard type the name of the element
        # due to inheritance, this may not always work

    
class CyclicGroup:
    def __init__(self, order):
        self.order = order

    def validate(self, value):
        if not isinstance(value, Integral) and 0 <= value < self.order:
            raise ValueError(f"Element value must be an integer between 0 and \
                             {self.order}")

    def operation(self, a, b):
        return (a + b) % self.order
        
    def __call__(self, value):
        return Element(self, value)
    
    def __str__(self):
        return f"C{self.order}"
    
    def __repr__(self):
        return f"{type(self).__name__}({self.order!r})"
    

class Group:
    """A base class containing methods common to many groups.

    Each subclass represents a family of parametrised groups.

    Parameters
    ----------
    n: int
        The primary group parameter, such as order or degree. The
        precise meaning of n changes from subclass to subclass.
    """
    def __init__(self, n):
        self.n = n

    def __call__(self, value):
        """Create an element of this group."""
        return Element(self, value)

    def __str__(self):
        """Return a string in the form symbol then group parameter."""
        return f"{self.symbol}{self.n}"

    def __repr__(self):
        """Return the canonical string representation of the element."""
        return f"{type(self).__name__}({self.n!r})"


class CyclicGroupInherit(Group):
    """A cyclic group represented by integer addition modulo n."""
    symbol = "C" # class attribute

    def _validate(self, value):
        """Ensure that value is an allowed element value in this group."""
        if not (isinstance(value, Integral) and 0 <= int(value) < self.n):
            raise ValueError("Element value must be an integer"
                            f" in the range [0, {self.n})")

    def operation(self, a, b):
        """Perform the group operation on two values.

        The group operation is addition modulo n.
        """
        return (a + b) % self.n


class GeneralLinearGroup(Group):
    """The general linear group represented by n x n matrices."""

    symbol = "G" #notice we do not write self, it is not defined in this scope

    def _validate(self, value):
        """Ensure that value is an allowed element value in this group."""
        value = np.asarray(value)
        if not (value.shape == (self.n, self.n)):
            raise ValueError("Element value must be a "
                            + f"{self.n} x {self.n}" + "square array.")

    def operation(self, a, b):
        """Perform the group operation on two values.

        The group operation is matrix multiplication.
        """
        return a @ b