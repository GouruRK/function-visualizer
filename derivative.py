from typing import Union
from function import Function


class Derivative(Function):
    """Object representing a mathematical function's derivative
    with "x" the argument of the function.
    This object support simple arithmetical functions, such as :
     - "plus" represented by "+" ;
     - "minus" represented	by "-" ;
     - "times" represented	by "*" ;
     - "divides" represented by "/" ;
     - "power" represented	by "^" ;
    and the parentheses.

    This program is using the difference quotient formula to calculate
    derivatives, which is f'(x) = lim (f(x+h)-f(x))/h as h approaches 0.
    """

    def __init__(self, expr: str) -> None:
        """Initialisation of the Derivative object.

        :param expr: the function expression
        :type expr: str

        Example of valid expression :
         - "x+2"
         - "(x-1)^2"
         - "((-x+2)^2)/(x*2)"
        """
        super().__init__(expr)

    def __call__(self, x: int | float) -> float:
        """Calculate the value of the function for an ``x``

        :param x: the value for the function to compute for
        :type x: int | float
        :return: the result
        :rtype: int | float
        """
        h = 1e-10
        f = self.compute(self.replace_x(self.expr, x))
        f2 = self.compute(self.replace_x(self.expr, x + h))
        return (f2 - f) / h
