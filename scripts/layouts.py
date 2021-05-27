#     This file is part of LDV-plotter.
#
#     LDV-plotter is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     LDV-plotter is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with LDV-plotter.  If not, see <https://www.gnu.org/licenses/>.

import sys
from PySide2 import QtWidgets, QtCore, QtGui
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from costum_widgets import VerticalCostumLayout, CostumEntry, MainMenu

class MainLayout(QtWidgets.QGridLayout):
    def __init__(self, parent):
        QtWidgets.QGridLayout.__init__(self)
        self.parent = parent
        self.config()

    def config(self):
        self.create_widgets()
        self.add_widgets()

    def create_widgets(self):
        self.right_layout = RightLayout(self.parent)
        self.matplot_layout = MatplotLayout(self.parent)
        self.create_ax()
        self.menu = MainMenu(self.parent)

    def add_widgets(self):
        self.addWidget(self.menu, 0, 0, 1, 2)
        self.addLayout(self.matplot_layout, 1, 0)
        self.addLayout(self.right_layout, 1, 1)

    def add_app_func(self, app_func):
        self.right_layout.funcs.add_app_func(app_func)

    def clear_plt(self):
        self.matplot_layout.plt_figure.clear()

    def create_ax(self):
        ax = self.matplot_layout.plt_figure.add_subplot()
        ax.set_facecolor((0,0,0,0))

        return ax

    def get_x_range(self):
        start = self.right_layout.tools.x_start.value()
        end = self.right_layout.tools.x_end.value()
        step = float(self.right_layout.tools.x_step.text())
        return (start, end, step)

    def get_x_settings(self):
        start = self.right_layout.tools.x_start.value()
        end = self.right_layout.tools.x_end.value()
        n_points = int(self.right_layout.tools.points_range.text())
        return (start, end, n_points)   

    def set_x_settings(self, x_settings):
        self.right_layout.tools.x_start.setValue(float(x_settings[0]))
        self.right_layout.tools.x_end.setValue(float(x_settings[1]))
        self.right_layout.tools.points_range.setValue(float(x_settings[2]))
 

    def reset_ui(self):
        self.right_layout.tools.reset_ui()
        self.clear_plt()
        self.update_canvas()

    def update_canvas(self):
        plt.xlabel("x")
        plt.ylabel("y")
        self.matplot_layout.canvas.draw()

class MatplotLayout(VerticalCostumLayout):
    def create_widgets(self):
        self.plt_figure = plt.figure()
        self.canvas = FigureCanvas(self.plt_figure)
        self.toolbar = NavigationToolbar(self.canvas, self.parent)

    def configure_widgets(self):
        plt.xlabel("x")
        plt.ylabel("y")

    def add_widgets(self):
        self.addWidget(self.toolbar)
        self.addWidget(self.canvas)

class RightLayout(VerticalCostumLayout):
    def create_widgets(self):
        self.tools = ToolsLayout(self.parent)
        self.funcs = AppFuncsLayout()
        self.plot_button = QtWidgets.QPushButton('Plot')

    def configure_widgets(self):
        self.plot_button.clicked.connect(self.parent.plot)
        shortcut = QtWidgets.QShortcut('Return', self.plot_button)
        shortcut.activated.connect(self.parent.plot)

    def add_widgets(self):
        self.addLayout(self.tools)
        self.addLayout(self.funcs)
        self.addWidget(self.plot_button)

class AppFuncsLayout(QtWidgets.QVBoxLayout):
    def __init__(self, funcs=[]):
        QtWidgets.QVBoxLayout.__init__(self)
        self.addStretch()
        self.load_funcs(funcs)

    def load_funcs(self, funcs):
        for foo in funcs:
            self.add_app_func(foo)

    def add_app_func(self, app_func):
        self.addLayout(app_func)

    def remove_app_func(self, app_func):
        app_func.delete()
        self.removeWidget(app_func)

class ToolsLayout(QtWidgets.QFormLayout):
    def __init__(self, parent):
        QtWidgets.QFormLayout.__init__(self)
        self.parent = parent

        self.create_x_tools()
        self.create_x_tools_labels()
        self.create_new_func_button()
        self.config()

    def create_x_tools(self):
        self.create_x_start()
        self.create_x_end()
        self.create_x_step()
        self.create_points_range()

    def create_x_start(self):
        self.x_start = QtWidgets.QDoubleSpinBox()
        self.x_start.setRange(-2147483647, 2147483647)
        self.x_start.setDecimals(5)
        self.x_start.valueChanged.connect(self.set_num_step)


    def create_x_end(self):
        self.x_end = QtWidgets.QDoubleSpinBox()
        self.x_end.setRange(-2147483647, 2147483647)
        self.x_end.setValue(100)
        self.x_end.setDecimals(5)
        self.x_end.valueChanged.connect(self.set_num_step)

    def create_x_step(self):
        self.x_step = CostumEntry(0.1)

    def create_points_range(self):
        self.points_range = QtWidgets.QSpinBox()
        self.points_range.setRange(0, 2147483647)
        self.points_range.setValue(1000)
        self.points_range.valueChanged.connect(self.set_num_step)

    def create_x_tools_labels(self):
        self.x_start_label = QtWidgets.QLabel("x starts at")
        self.x_end_label = QtWidgets.QLabel("x ends at")
        self.x_step_label = QtWidgets.QLabel("steps are of")
        self.points_range_label = QtWidgets.QLabel("№ of points")


    def create_new_func_button(self):
        self.new_func_button = QtWidgets.QPushButton('New Func')
        self.new_func_button.clicked.connect(self.parent.create_new_func)

    def config(self):
        l = ((self.x_start_label, self.x_start),
             (self.x_end_label, self.x_end),
             (self.points_range_label, self.points_range),
             (self.x_step_label, self.x_step),
             (QtWidgets.QWidget(), self.new_func_button))

        for label, effective in l:
            self.addRow(label, effective)

    def set_num_step(self):
        start = self.x_start.value()
        end = self.x_end.value()
        n_points = self.points_range.value()

        if n_points == 0:
            self.points_range.setValue(1)
            return 1

        step = (end - start)/n_points
        self.x_step.setValue(step)

    def reset_ui(self):
        self.x_start.setValue(0)
        self.x_end.setValue(100)
        self.x_step.setValue(0.1)
        self.points_range.setValue(1000)
