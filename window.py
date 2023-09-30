import tkinter as tk


class Window:
    """A minimalist window using tkinter to display the
    graph of the functions choosen by the user
    """

    def __init__(self, width: int, height: int):
        """Initialisation of the Window object

        :param w: the width of the window
        :type w: int
        :param h: the height of the window
        :type h: int
        """
        self.root = tk.Tk()
        self.canvas = tk.Canvas(
            self.root, width=width, height=height, highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.focus_set()

    def line(
        self, x1: int, y1: int, x2: int, y2: int, fill: str = "black", width: int = 1
    ) -> None:
        """Function  to draw line on the window, from (x1, y1) to (x2, y2)

        :param x1: the absciss of the first point
        :type x1: int
        :param y1: the ordinate of the first point
        :type y1: int
        :param x2: the absciss of the second point
        :type x2: int
        :param y2: the ordinate of the second point
        :type y2: int
        :param fill: color of the line, defaults to "black"
        :type fill: str, optional
        :param width: the width of the line, defaults to 1
        :type width: int, optional
        """
        self.canvas.create_line(x1, y1, x2, y2, fill=fill, width=width)

    def mainloop(self) -> None:
        """tkinter mainloop function"""
        self.root.mainloop()
