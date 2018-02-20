# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from matplotlib.figure import Figure
import random

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5

import matplotlib.pyplot as plt

from model.myutils import RGBA_arg

if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100, title="No title"):
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
        self.axes.cla()
        self.draw()

    def plot(self, data_x, data_y, legend="", color="red"):
        if legend == "":
            self.axes.plot(data_x, data_y, color=color)
        else:
            self.axes.plot(data_x, data_y, label=legend, color=color)

        handles, labels = self.axes.get_legend_handles_labels()
        self.axes.legend(handles, labels, loc="best")
        self.axes.grid('on')
        self.draw()
