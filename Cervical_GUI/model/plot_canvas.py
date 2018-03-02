# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QSizePolicy
from descartes import PolygonPatch
from matplotlib.figure import Figure

from matplotlib.backends.qt_compat import is_pyqt5

from model.myutils import RGBA_arg

if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas)

# TODO FX ICI RAJOUTER FONCTION DE DESSIN DES DIFFERENTS MODELES

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

    def plot_polygon_MP(self, polygon):
        """
        Plot a polygon using PolygonPatch.

        Parameters
        ----------
        polygon : MultiPoint
                The polygon to plot
        """
        margin = .3
        x_min, y_min, x_max, y_max = polygon.bounds
        self.axes.set_xlim([x_min - margin, x_max + margin])
        self.axes.set_ylim([y_min - margin, y_max + margin])
        patch = PolygonPatch(polygon, fc='#999999',
                             ec='#000000', fill=True,
                             zorder=-1)
        self.axes.add_patch(patch)

    def plot_many_polygons(self, lst_poly):
        """
        Plot a list of polygons contained in a list.

        Parameters
        ----------
        lst_poly : array(MultiPoints)
                List of polygons

        Returns
        -------
        figure
                The corresponding figure.
        """
        x_max = 0
        y_max = 0
        x_min = 0
        y_min = 0

        margin = .3
        for poly in lst_poly:
            # Determine the axes limits
            x_min_curr, y_min_curr, x_max_curr, y_max_curr = poly.bounds
            if x_max < x_max_curr:
                x_max = x_max_curr
            if y_max < y_max_curr:
                y_max = y_max_curr
            if y_min > y_min_curr:
                y_min = y_min_curr
            if x_min > x_min_curr:
                x_min = x_min_curr

            color = RGBA_arg()
            patch = PolygonPatch(poly, fc=color,
                                 ec=color, fill=True,
                                 zorder=-1)
            self.axes.add_patch(patch)
        self.axes.set_xlim([x_min - margin, x_max + margin])
        self.axes.set_ylim([y_min - margin, y_max + margin])
        self.axes.legend([str(i + 1) for i in range(len(lst_poly))])

    def plot_discrete_hull(self, grid, grid_pts, hull):
        """
        Plot a hull and its discretization.

        Parameters
        ----------
        grid : array
                Array of 1s (within hull) and 0s (outside), the discrete hull.
        grid_pts : array
                Array of points of the grid.
        hull : Polygon
                The concave hull.
        """
        self.plot_polygon_MP(hull)
        x, y = [pt[0] for pt in grid_pts], [pt[1] for pt in grid_pts]
        self.axes.scatter(x, y)
        # plt.scatter(x, y)
        ind_ones = []
        for i in range(len(x)):
            if grid[i] == 1:
                ind_ones += [i]
        xd = [x[i] for i in ind_ones]
        yd = [y[i] for i in ind_ones]
        self.axes.scatter(xd, yd, c='r')

