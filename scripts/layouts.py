from PyQt5 import QtWidgets, QtCore, QtGui
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class VerticalCostumLayout(QtWidgets.QVBoxLayout):
    def __init__(self, parent):
        QtWidgets.QVBoxLayout.__init__(self)
        self.parent = parent
        self.config()

    def config(self):
        self.create_widgets()
        self.add_widgets()

    def create_widgets(self):
        raise NotImplementedError

    def add_widgets(self):
        raise NotImplementedError


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
        self.menu = MainMenu(self.parent)

    def add_widgets(self):
        self.addWidget(self.menu, 0, 0)
        self.addLayout(self.matplot_layout, 1, 0)
        self.addLayout(self.right_layout, 1, 1)

    def add_app_func(self, app_func):
        self.right_layout.funcs.add_app_func(app_func)

    def clear_plt(self):
        self.matplot_layout.plt_figure.clear()

    def create_ax(self):
        return self.matplot_layout.plt_figure.add_subplot(111)

    def get_x_range(self):
        start = self.right_layout.tools.x_start.value()
        end = self.right_layout.tools.x_end.value()
        step = self.right_layout.tools.x_step.value()
        return (start, end, step)

class MainMenu(QtWidgets.QMenuBar):
    def __init__(self, main_window):
        QtWidgets.QMenuBar.__init__(self)
        self.main_window = main_window
        self.setupStyleSheet()
        self.createFileMenu()

    def createFileMenu(self):
        files = self.addMenu("Files")
        files.addAction("New")
        files.addAction("Open")
        files.addAction("Save")
        files.addAction("Save as")
        files.addSeparator()
        files.addAction("Quit")
        files.setStyleSheet(self.css)


    def setupStyleSheet(self):
        self.css = open("../stylesheets/menu_stylesheet.css", "r").read()

class MatplotLayout(VerticalCostumLayout):
    def create_widgets(self):
        self.plt_figure = plt.figure()
        plt.xlabel("x")
        plt.ylabel("y")

        self.canvas = FigureCanvas(self.plt_figure)
        self.toolbar = NavigationToolbar(self.canvas, self.parent)

    def add_widgets(self):
        self.addWidget(self.toolbar)
        self.addWidget(self.canvas)

class RightLayout(VerticalCostumLayout):
    def create_widgets(self):
        self.tools = ToolsLayout(self.parent)
        self.funcs = AppFuncsLayout()

        self.plot_button = QtWidgets.QPushButton('Plot')
        self.plot_button.clicked.connect(self.parent.plot)
        shortcut = QtWidgets.QShortcut('Return', self.plot_button)
        shortcut.activated.connect(self.parent.plot)

    def add_widgets(self):
        self.addLayout(self.tools)
        self.addStretch()
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
        self.x_start = QtWidgets.QDoubleSpinBox()
        self.x_start.setRange(-2147483647, 2147483647)
        self.x_start.setDecimals(5)

        self.x_end = QtWidgets.QDoubleSpinBox()
        self.x_end.setRange(-2147483647, 2147483647)
        self.x_end.setValue(100)
        self.x_end.setDecimals(5)

        self.x_step = QtWidgets.QDoubleSpinBox()
        self.x_step.setRange(-2147483647, 2147483647)
        self.x_step.setValue(0.1)
        self.x_step.setDecimals(5)

        self.points_range = QtWidgets.QSpinBox()
        self.points_range.setRange(0, 2147483647)
        self.points_range.setValue(1)
        self.points_range.setStyleSheet("height: 40;")

    def create_x_tools_labels(self):
        self.x_start_label = QtWidgets.QLabel("x starts at")
        self.x_end_label = QtWidgets.QLabel("x ends at")
        self.x_step_label = QtWidgets.QLabel("steps are of")
        self.points_range_label = QtWidgets.QPushButton("set the №\nof points")
        self.points_range_label.clicked.connect(self.set_num_points)

    def create_new_func_button(self):
        self.new_func_button = QtWidgets.QPushButton('New Func')
        self.new_func_button.clicked.connect(self.parent.add_new_func)

    def config(self):
        l = (
            (self.x_end_label, self.x_end),
            (self.x_start_label, self.x_start),
            (self.x_step_label, self.x_step),
            (self.points_range_label, self.points_range),
            (QtWidgets.QWidget(), self.new_func_button))

        for label, effective in l:
            self.addRow(label, effective)

    def set_num_points(self):
        start = self.x_start.value()
        step = self.x_step.value()
        n_points = self.points_range.value()

        end = start + (step*n_points)
        self.x_end.setValue(end)

