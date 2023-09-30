from typing import Any, Union

Expression = list[Union[int, float]]

OPERATORS = {
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "^": lambda a, b: a**b,
}


class Function:
    """Object representing a math function, with "x" as unknown var.
    This object support simple arithmetical functions, such as :
     - "plus" represented by "+" ;
     - "minus" represented	by "-" ;
     - "times" represented	by "*" ;
     - "divides" represented by "/" ;
     - "power" represented	by "^" ;
    and the parentheses for priorities.
    """

    def __init__(self, expr: str) -> None:
        """Initialisation of the Function object.

        :param expr: the function expression
        :type expr: str

        Example of valid expression :
         - "x+2"
         - "(x-1)^2"
         - "((-x+2)^2)/(x*2)"
        """
        self.expr, length = self.tokenize(expr)
        if (not length) or (not len(self.expr)):
            raise ValueError("Expression cannot be empty")

    def tokenize(self, expr: str, i: int = 0) -> tuple[Expression, int]:
        """Transform the valid string's expression into a list of tokens.
        This method does not support invalid expression.
        All the numbers will be parsed as float (which means that "2"
        will be evaluated as 2.0).
        Relatives number (such as "-3") will be evaluated as "-1.0*3.0"
        Float numbers must be written with a "." (not a comma).

        :param expr: expression to tokenize
        :type expr: str, optional
        :param i: index of ``expr`` which indicates the starting point of
        the processus of tokenization, defaults to 0
        :type i: int, optional
        :return: list of tokens and it's total length
        :rtype: tuple[list, int]

        >>> Function.tokenize("x+2.3")
        (['x', '+', 2.3], 5)
        >>> Function.tokenize("(x-1)^2")
        ([['x', '-', 1.0], '^', 2.0], 7)
        >>> Function.tokenize("((-x+2)^2)/(x*2)")
        ([[[-1.0, '*', 'x', '+', 2.0], '^', 2.0], '/', ['x', '*', 2.0]], 16)
        """
        lst = []
        while i < len(expr):
            if expr[i] == "(":
                res, i = self.tokenize(expr, i + 1)
                lst.append(res)
            elif expr[i] == ")":
                return lst, i + 1
            elif expr[i] == "-":
                if i == 0 or expr[i - 1] == "(":
                    lst.append(-1.0)
                    lst.append("*")
                else:
                    lst.append("-")
                i += 1
            elif expr[i] == ".":
                i += 1
                depth = 1
                while i < len(expr) and expr[i].isdigit():
                    digit = float(expr[i])
                    lst[-1] += digit * 10 ** (-depth)
                    i += 1
                    depth += 1
            elif expr[i].isdigit():
                lst.append(0)
                while i < len(expr) and expr[i].isdigit():
                    lst[-1] = lst[-1] * 10 + float(expr[i])
                    i += 1
            elif expr[i] == " ":
                i += 1
            else:
                lst.append(expr[i])
                i += 1
        return lst, i

    def calculate(self, expr: Expression, indice: int) -> Expression:
        """Take an operation inside an expression and return
        the result of it.
        The result of this fonction modify the ``expr`` argument.

        :param expr: the expression
        :type expr: list
        :param indice: the index of the operator
        :type indice: int
        :return: The new expression
        :rtype: list

        >>> Function.calculate([2.0, "+", 3.0], 1)
        [5.0]
        >>> Function.calculate([2.0, "+", 3.0, '^', 2.0], 3)
        [2.0, '+', 9.0]
        """
        n_0 = expr[indice - 1]
        n_1 = expr[indice + 1]
        operator = expr[indice]
        expr[indice] = OPERATORS[operator](n_0, n_1)
        expr.pop(indice + 1)
        expr.pop(indice - 1)
        return expr

    def iterate(self, expr: list, operators: set) -> list[Union[float, str]]:
        """Loop on the list to see if the expression in ``lst``
        contains an operator in ``ope``, and calculate the result
        of that operation.
        The result of this fonction modify the ``expr`` argument.

        :param expr: the expression
        :type expr: list
        :param ope: all the operators to look at
        :type ope: set
        """
        i = 0
        while i < len(expr):
            prec = len(expr)
            if expr[i] in operators:
                self.calculate(expr, i)
            if len(expr) == prec:
                i += 1
        return expr

    def execute(self, expr: Expression) -> float:
        """This function will calculate the result of an expression
        whithout parentheses according to operators priorities.

        :param expr: the expression
        :type expr: list
        :return: the result
        :rtype: float

        >>> Function.execute([2.0, "+", 3.0])
        5.0
        >>> Function.execute([2.0, "+", 3.0, '^', 2.0])
        11.0
        """
        self.iterate(expr, {"^"})
        self.iterate(expr, {"*", "/"})
        self.iterate(expr, {"+", "-"})
        return expr[0]

    def compute(self, expr: Expression) -> float:
        """This function will calculate the result of an expression
        with parentheses, by calculating at first the result of all
        parentheses, following the rule of operators priority.

        :param expr: the expression
        :type expr: list
        :return: the result
        :rtype: float

        >>> Function.compute([[5.0, '-', 1.0], '^', 2.0])
        16.0
        >>> Function.compute([2.0, "+", 3.0, '^', 2.0], 3)
        11.0
        >>> Function.compute("((-5+2)^2)/(5*2)")
        0.9
        """
        is_parentheses = True
        while len(expr) != 0 and is_parentheses:
            is_parentheses = False
            for j in range(len(expr)):
                if isinstance(expr[j], list):
                    is_parentheses = True
                    res = self.compute(expr[j])
                    expr[j] = res
        return self.execute(expr)

    def replace_x(self, expr: Expression, x: Union[int, float]) -> Expression:
        """Replace the "x" variable of the function by the
        ``x`` argument

        :param expr: the expression
        :type expr: list
        :param x: the new value
        :type x: int | float
        :return: the new expression
        :rtype: list

        >>> replace_x(['x', '+', 2.3], 0)
        [0, '+', 2.3]
        >>> replace_x([['x', '-', 1.0], '^', 2.0, '+', 'x'], 5)
        [[5.0, '-', 1.0], '^', 2.0, '+', 5.0]
        """
        lst = []
        for i in range(len(expr)):
            if expr[i] == "x":
                lst.append(x)
            elif isinstance(expr[i], list):
                res = self.replace_x(expr[i], x)
                lst.append(res)
            else:
                lst.append(expr[i])
        return lst

    def __call__(self, x: Union[int, float]) -> float:
        """Calculate the value of the function for an ``x``

        :param x: the value for the function to compute for
        :type x: int | float
        :return: the result
        :rtype: int | float
        """
        fun = self.replace_x(self.expr, x)
        return self.compute(fun)


if __name__ == "__main__":
    f = Function("((-x+2)^2)/(x*2)")
