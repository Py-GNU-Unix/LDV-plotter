import sys
import func_generator
from PyQt5 import QtWidgets, QtCore, QtGui
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class NoStepsError(Exception): pass

FUNCS_EXECUTION_ERRORS = (
    ArithmeticError,
    SyntaxError,
    NameError,
    NoStepsError)

class AppFunc(QtWidgets.QHBoxLayout):
    def __init__(self, name, master):
        QtWidgets.QHBoxLayout.__init__(self)
        self.name = name
        self.master = master
        self.entry = QtWidgets.QLineEdit()
        self.entry_doc = QtWidgets.QLabel(f"{name} = ")
        self.create_close_button()
        self.configure()

    def create_close_button(self):
        self.close_button = QtWidgets.QPushButton("X")
        self.close_button.clicked.connect(self.delete)

        css = open("../stylesheets/close_button_stylesheet.css","r").read()
        self.close_button.setStyleSheet(css)

    def configure(self):
        self.addWidget(self.entry_doc)
        self.addWidget(self.entry)
        self.addWidget(self.close_button)

    def delete(self):
        self.master.app_funcs.remove(self)
        self.delete_widgets()
        self.master.update_funcs_names()

    def delete_widgets(self):
        self.entry.deleteLater()
        self.entry_doc.deleteLater()
        self.close_button.deleteLater()

    def set_name(self, name):
        self.name = name
        self.entry_doc.setText(f"{name} = ")

    def get_layout(self):
        return self.layout

    def get_text(self):
        return self.entry.text()

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

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setup_win_style()
        self.setup_layout()

    def setup_win_style(self):
        icon = QtGui.QIcon()
        #icon.addFile('../images/icon.png', QtCore.QSize(128, 128))
        icon.addFile('../images/icon.png_64x64', QtCore.QSize(64, 64))
        icon.addFile('../images/icon.png_32x32', QtCore.QSize(32, 32))
        icon.addFile('../images/icon.png_16x16', QtCore.QSize(16, 16))
        self.setWindowIcon(icon)
        
        css = open("../stylesheets/window_stylesheet.css", "r").read()
        self.setStyleSheet(css)

    def setup_layout(self):
        self.app_funcs = []
        self.main_layout = MainLayout(self)
        self.setLayout(self.main_layout)
        self.add_new_func()

    def create_x(self):
        start, end, step = self.main_layout.get_x_range()
        count = start

        if not step:
            raise NoStepsError

        while end-count > step/2:
            yield count
            count += step

    def get_funcs(self):
        return self.app_funcs

    def alert_failed_func(self, app_func, error):
        alrt = QtWidgets.QMessageBox()
        alrt.setWindowTitle("Failed to evaluate the expression")
        alrt.setText(f"Your expression is wrong:\n in app_func {app_func.name}:\n {error}")
        alrt.exec_()

    def update_canvas(self):
        plt.xlabel("x")
        plt.ylabel("y")
        self.main_layout.matplot_layout.canvas.draw()

    def plot(self):
        self.main_layout.clear_plt()
        ax = self.main_layout.create_ax()

        for app_func in self.get_funcs():
            string = app_func.get_text()
            if not string: continue

            foo = func_generator.generate_func(string)
            try:
                data = [foo(i) for i in self.create_x()]

            except FUNCS_EXECUTION_ERRORS as error:
                self.alert_failed_func(app_func, error)

            else:
                ax.plot(list(self.create_x()), data, '.-')

        self.update_canvas()


    def add_new_func(self, name=""):
        if not name:
            name = f"f{len(self.app_funcs)+1}(x)"

        func = AppFunc(name, self)
        self.main_layout.add_app_func(func)
        self.app_funcs.append(func)

    def delete_func(self, foo):
        foo.delete()

    def update_funcs_names(self):
        count = 0
        for f in self.app_funcs:
            count += 1
            name = f"f{count}(x)"
            f.set_name(name)

app = QtWidgets.QApplication(sys.argv)

x = MainWindow()
x.show()
sys.exit(app.exec_())
