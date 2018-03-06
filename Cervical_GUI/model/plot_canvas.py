# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QSizePolicy
from descartes import PolygonPatch
from matplotlib.figure import Figure
from matplotlib.backends.qt_compat import is_pyqt5
import numpy as np

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
        self.axes.cla()
        self.plot_polygon_MP(hull)
        x, y = [pt[0] for pt in grid_pts], [pt[1] for pt in grid_pts]
        self.axes.scatter(x, y, c='b')
        # plt.scatter(x, y)
        ind_ones = []
        for i in range(len(x)):
            if grid[i] == 1:
                ind_ones += [i]
        xd = [x[i] for i in ind_ones]
        yd = [y[i] for i in ind_ones]
        self.axes.scatter(xd, yd, c='r')
        self.axes.set_ylim(bottom=0.38, top=0.62)
        self.axes.set_xlim(left=-0.05, right=1.05)
        self.draw()

    def plot_hull_spline(self, hull, spline, curve, type_motion):
        """
        Plot the curve of the acquisition and the hull.
        
        Parameters
        ----------
        curve : array of arrays
                First array is x-axis component of the acquisition, second is y-axis.
        hull : Polygon
                Model hull.
        spline : array of array
                Same as curve but for the spline.
        type_motion : str
                'pitch' or 'roll', according to the angle considered.
        """
        self.axes.cla()
        self.plot_polygon_MP(hull)
        self.plot(curve[0], curve[1], color='red', legend='Dernière acquisition')
        self.plot(spline[0], spline[1], color='blue', legend='Spline')
        if type_motion == 'pitch':
            self.axes.set_ylim(bottom=0.44, top=0.56)
        elif type_motion == 'roll':
            self.axes.set_ylim(bottom=0.33, top=0.67)
        else:
            raise ValueError('type_motion must be either "pitch" or "roll"')
        self.axes.set_ylabel(type_motion)
        self.axes.set_xlim(left=-0.05, right=1.05)
        self.axes.set_xlabel('yaw')
        self.draw()

    def plot_final_time(self, new_coord, mean_coords, nb_window, norm=1):
        """
        Plot the final figure : pitch vs pitch_mean, yaw vs yaw_mean, roll vs roll_mean, pitch vs yaw vs roll
        :param new_coord: list of the three coordinates of the current data
        :param nb_window: id of the plot window
        :param mean_coords: list of every patient of the data_base
        :param norm: optional, 1 if you want the data to be normed
        :return: void
        """

        yaw_mean, pitch_mean, roll_mean = mean_coords
        len_mean = len(pitch_mean)
        yaw, pitch, roll = new_coord
        len_coord = len(pitch)

        self.axes.cla()

        if nb_window == 1:
            self.plot(np.linspace(0, len_coord-1, len_coord), pitch, legend='Tangage')
            self.plot(np.linspace(0, len_mean-1, len_mean), pitch_mean, color='blue', legend='Tangage moyen')
        elif nb_window == 2:
            self.plot(np.linspace(0, len_coord-1, len_coord), yaw, legend='Lacet')
            self.plot(np.linspace(0, len_mean-1, len_mean), yaw_mean, color='blue', legend='Lacet moyen')
        elif nb_window == 3:
            self.plot(np.linspace(0, len_coord-1, len_coord), roll, legend='Roulis')
            self.plot(np.linspace(0, len_mean-1, len_mean), roll_mean, color='blue', legend='Roulis moyen')
        elif nb_window == 4:
            self.plot(np.linspace(0, len_coord-1, len_coord), pitch, color='blue', legend='Tangage')
            self.plot(np.linspace(0, len_coord-1, len_coord), yaw, color='red', legend='Lacet')
            self.plot(np.linspace(0, len_coord-1, len_coord), roll, color='green', legend='Roulis')

        self.draw()
