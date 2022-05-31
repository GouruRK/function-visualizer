from typing import Union


class Function:
    """Object representing a mathematical function, with "x"
    the argument of the function.
    This object support simple arithmetical functions, such as :
     - "plus" representing by the symbol "+" ;
     - "minus" representing	by the symbol "-" ;
     - "times" representing	by the symbol "*" ;
     - "divides" representing by the symbol "/" ;
     - "power" representing	by the symbol "^" ;
    and the parentheses.
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
        self.expr = expr
        self.expr_list = self.tokenize()

    def tokenize(self, expr: str = "", i: int = 0) -> list[Union[float, str]]:
        """Transform the valid string's expression into a list of tokens.
        This method does not support invalid expression.
        All the numbers will be parsed as flaot (which means that "2"
        will be evaluated as 2.0).
        Relatives number (such as "-3") will be evaluated as "-1.0*3.0"
        Float numbers must be written with a "." (not a comma).

        :param expr: expression to tokenize, defaults to "" means that
            "self.expr" will be the string to tokenize
        :type expr: str, optional
        :param i: index of ``expr`` which indicates the starting point of
        the processus of tokenization, defaults to 0
        :type i: int, optional
        :return: The list with the tokens
        :rtype: lst

        >>> Function.tokenize("x+2.3")
        ['x', '+', 2.3]
        >>> Function.tokenize("(x-1)^2")
        [['x', '-', 1.0], '^', 2.0]
        >>> Function.tokenize("((-x+2)^2)/(x*2)")
        [[[-1.0, '*', 'x', '+', 2.0], '^', 2.0], '/', ['x', '*', 2.0]]
        """
        if expr == "":
            expr = self.expr
        lst = []
        while i < len(expr):
            if expr[i] == "(":
                res = self.tokenize(expr, i + 1)
                lst.append(res)
                result, depth = self.get_full_lenght(res)
                i += result + 1 + depth
            elif expr[i] == ")":
                return lst
            elif expr[i] == "-":
                if i == 0 or expr[i - 1] == "(":
                    lst.append(-1.0)
                    lst.append("*")
                else:
                    lst.append("-")
            elif expr[i] == ".":
                i += 1
                depth = 1
                while i < len(expr) and expr[i].isdigit():
                    digit = float(expr[i])
                    lst[-1] += digit * 10 ** (-depth)
                    i += 1
                    depth += 1
                i -= 1
            elif expr[i].isdigit():
                lst.append(0)
                while i < len(expr) and expr[i].isdigit():
                    lst[-1] = lst[-1] * 10 + float(expr[i])
                    i += 1
                i -= 1
            else:
                lst.append(expr[i])
            i += 1
        return lst

    def get_full_lenght(self, lst: list, depth: int = 0) -> tuple[int, int]:
        """Return the full length of a current expression, depending on the
        number of terms in ``lst``, includings list of list etc ; and the
        depth, the number of list of lists.

        :param lst: the list to be evaluated
        :type lst: list
        :param depth: the current depth, defaults to 0
        :type depth: int, optional
        :return: the length and the depth
        :rtype: tuple

        >>> Function.get_full_lenght(['x', '+', 2.3])
        (3, 0)
        >>> Function.get_full_lenght([['x', '-', 1.0], '^', 2.0])
        (5, 1)
        """
        lenght = 0
        for i in range(len(lst)):
            if isinstance(lst[i], list):
                result, depth = self.get_full_lenght(lst[i], depth + 1)
                lenght += result
            lenght += 1
        return lenght, depth

    def calculate(self, expr: list, indice: int) -> list[Union[float, str]]:
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
        operations = {
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "^": lambda a, b: a**b,
        }
        n_0 = expr[indice - 1]
        n_1 = expr[indice + 1]
        operator = expr[indice]
        res = operations[operator](n_0, n_1)
        expr[indice] = res
        expr.pop(indice + 1)
        expr.pop(indice - 1)
        return expr

    def iterate(self, expr: list, operators: set) -> list[Union[float, str]]:
        """Loop on the list to see if the expression in ``lst``
        contains an operator in ``ope``, an calculate the result
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

    def proceed(self, expr: list) -> float:
        """This function will calculate the result of an expression
        whithout parentheses following the rules of maths
        operators order.

        :param expr: the expression
        :type expr: list
        :return: the result
        :rtype: int | float

        >>> Function.proceed([2.0, "+", 3.0])
        5.0
        >>> Function.proceed([2.0, "+", 3.0, '^', 2.0])
        11.0
        """
        self.iterate(expr, {"^"})
        self.iterate(expr, {"*", "/"})
        self.iterate(expr, {"+", "-"})
        return expr[0]

    def compute(self, expr: list) -> float:
        """This function will calculate the result of an expression
        with parentheses, by calculate at first the result of all
        parentheses, following the rule of operators order.

        :param expr: the expression
        :type expr: list
        :return: the result
        :rtype: int | float

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
        return self.proceed(expr)

    def replace_x(self, expr: list, x: Union[int, float]) -> list[Union[float, str]]:
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

    def f(self, x: Union[int, float]) -> float:
        """Calculate the value of the function for an ``x``

        :param x: the value for the function to compute for
        :type x: int | float
        :return: the result
        :rtype: int | float
        """
        fun = self.replace_x(self.expr_list, x)
        return self.compute(fun)


if __name__ == "__main__":
    f = Function("((-x+2)^2)/(x*2)")
