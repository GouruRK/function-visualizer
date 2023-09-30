from typing import Union
from derivative import Derivative
from function import Function
from window import Window
from settings import *

import sys


class Graph:
    """Object allowing to the user to draw math functions.
    It can only plot real numbers, which means that complex numbers wont be plot.
    """

    def __init__(
        self,
        window: object,
        x_min: Union[int, float],
        x_max: Union[int, float],
        y_min: Union[int, float],
        y_max: Union[int, float],
        step: float,
        width: int,
        height: int,
        axes: bool,
        functions: list[str],
    ) -> None:
        """Graph initialisation

        :param window: the window object to draw the graph.
        :type window: object
        :param x_min: the smallest absciss of the graph
        :type x_min: Union[int, float]
        :param x_max: the largest absciss of the graph
        :type x_max: Union[int, float]
        :param y_min: the smallest ordinate of the graph
        :type y_min: Union[int, float]
        :param y_max: the largest ordinate of the graph
        :type y_max: Union[int, float]
        :param step: this number represent the step between to absciss of the graph.
            if the step is 0.1, the next point of the absciss after 0 is 0.1.
        :type step: float
        :param width: the width of the window (in pixel)
        :type width: int
        :param height: the height of the window (in pixel)
        :type height: int
        :param axes: indicate to draw or not the axes
        :type axes: bool
        :param functions: the list of the functions to draw
        :type functions: list[str]
        """
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.step = step
        self.width = width
        self.height = height
        self.axes = axes
        self.functions = functions
        self.window = window
        self.coefs = self.calculate_coef()
        self.colors = ["blue", "red", "green", "yellow", "purple"]

    def calculate_points(self) -> list[list[tuple[float, float]]]:
        """Generate a list of points for all functions
        from the ``self.x_min`` absciss to the ``self.x_max``

        :return: the list of list containing the points
        :rtype: list[list[tuple[float, float]]]
        """
        points = []
        fi = 0
        for f in self.functions:
            points.append([])
            x = self.x_min
            while x < self.x_max:
                try:
                    y = f(x)
                    if isinstance(y, complex):
                        raise TypeError
                    a, b = self.coordinate_to_screen((x, y))
                    points[fi].append((a, b))
                except ZeroDivisionError:
                    pass
                except TypeError:
                    pass
                x += self.step
            fi += 1
        return points

    def calculate_coef(self) -> tuple[float, float, float, float]:
        """The (0, 0) of the window (the top left corner)
        is not the same (0, 0) for the graph (the center).
        This function calculate a, b, c, d coefficient to go
        from coordinate of the graph to coordinate of the window,
        using x1 = a*x+b, y1 = c*y+d equations.

        :return: the coefficients
        :rtype: tuple[float, float, float, float]
        """
        x1 = self.x_min
        y1 = self.y_min
        x2 = self.x_max
        y2 = self.y_max
        a = self.width / (x2 - x1)
        b = -a * x1
        c = -self.height / (y2 - y1)
        d = self.height - c * y1
        return a, b, c, d

    def coordinate_to_screen(self, point: tuple[float, float]) -> tuple[float, float]:
        """The (0, 0) of the window (the top left corner)
        is not the same (0, 0) for the graph (the center).
        This function calculate the coordinate of a point on the
        window from a point on the graph, using
        x1 = a*x+b, y1 = c*y+d equations.

        :param point: the point from the graph
        :type point: tuple[float, float]
        :return: the point on the window
        :rtype: tuple[float, float]
        """
        x, y = point
        a, b, c, d = self.coefs
        return a * x + b, c * y + d

    def display(self) -> None:
        """display the graph and the axes on the window"""
        if self.axes:
            self.display_axes()
        self.display_graph()

    def display_graph(self) -> None:
        """display functions's points of the window"""
        points = self.calculate_points()
        fi = 0
        c = 0
        for i in range(len(points)):
            if c == len(self.colors):
                c = 0
            for point in range(len(points[i])):
                if point + 1 < len(points[i]):
                    x1, y1 = points[i][point]
                    x2, y2 = points[i][point + 1]
                    window.line(x1, y1, x2, y2, fill=self.colors[c], width=2)
                fi += 1
            c += 1

    def display_axes(self) -> None:
        """display the axes"""
        self.display_absciss()
        self.display_ordinate()

    def display_absciss(self) -> None:
        """display the absciss"""
        p1 = (self.x_min, 0)
        p2 = (self.x_max, 0)
        p1 = self.coordinate_to_screen(p1)
        p2 = self.coordinate_to_screen(p2)
        self.abscisse = window.line(p1[0], p1[1], p2[0], p2[1])

    def display_ordinate(self) -> None:
        """display the ordinate"""
        p1 = (0, self.y_min)
        p2 = (0, self.y_max)
        p1 = self.coordinate_to_screen(p1)
        p2 = self.coordinate_to_screen(p2)
        self.ordinate = window.line(p1[0], p1[1], p2[0], p2[1])


def parse_functions() -> None:
    """Get function's expression from the command line.
    All functions must been written between ''.
    To draw a function derivative, add a "d" at the begining of the
        function expression
    """
    argv = sys.argv
    if len(argv) != 1:
        for expr in argv[1:]:
            if expr[0] == "d":
                FUNCTIONS.append(Derivative(expr[1:]))
            else:
                FUNCTIONS.append(Function(expr))


if __name__ == "__main__":
    parse_functions()
    graph = Graph(
        Window, X_MIN, X_MAX, Y_MIN, Y_MAX, STEP, WIDTH, HEIGHT, AXES, FUNCTIONS
    )
    window = Window(WIDTH, HEIGHT)
    graph.display()
    window.mainloop()
