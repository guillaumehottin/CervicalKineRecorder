# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QSizePolicy
from matplotlib.figure import Figure

from matplotlib.backends.qt_compat import is_pyqt5

if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas)


class PlotCanvas(FigureCanvas):
    """
    This class is used to manage the canvas that contains graph
    """

    def __init__(self, parent=None, width=5, height=4, dpi=100, title="No title"):
        """
        This function is used to declare and define all the class attributes
        :param parent: The window in which this canvas will be displayed (UNUSED)
        :param width: Integer The width of this canvas
        :param height: Integer the height of this canvas
        :param dpi: Integer the resolution
        :param title: String The title of the graph
        """
        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        self.title = title
        self.figure.suptitle(title)

        parent = FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def clear(self):
        """
        Function used to clear the axes and update the graph
        :return: Nothing
        """
        self.axes.cla()
        self.draw()

    def plot(self, data_x, data_y, legend="", color="red"):
        """
        Function used to display data_x and data_y on a graph with given legend and in given color
        :param data_x: Integer/Float list, X values
        :param data_y: Integer/Float list, Y values
        :param legend: String Legend to display
        :param color: String Color given (Hexa code, already defined color, rgba, etc.)
        :return:
        """
        if legend == "":
            self.axes.plot(data_x, data_y, color=color)
        else:
            self.axes.plot(data_x, data_y, label=legend, color=color)

        handles, labels = self.axes.get_legend_handles_labels()
        self.axes.legend(handles, labels, loc="best")
        self.axes.grid('on')
        self.draw()
