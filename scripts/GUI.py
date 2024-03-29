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

# Copyright 2020-present Py-GNU-Unix <py.gnu.unix.moderator@gmail.com>

import os
import sys
import matplotlib.pyplot as plt

from PySide2 import QtWidgets, QtCore, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from layouts import MainLayout
from costum_widgets import AppFunc
import func_generator

from pathlib import Path
home = str(Path.home())
os.chdir(home)

class NoStepsError(Exception): pass

FUNCS_EXECUTION_ERRORS = (
    ArithmeticError,
    SyntaxError,
    NameError,
    NoStepsError)

class MainWindow(QtWidgets.QWidget):
    def __init__(self, filename=None):
        QtWidgets.QWidget.__init__(self)
        self.set_filename(filename)
        self.setup_win_style()
        self.setup_layout()
        self.setup_file()

    def setup_layout(self):
        self.app_funcs = []
        self.main_layout = MainLayout(self)
        self.setLayout(self.main_layout)

    def setup_file(self):
        if not self.filename:
            self.create_new_func()
        else:
            self.open_file(self.filename)

    def setup_win_style(self):
        self.setup_win_icon()
        self.setup_palette()

    def setup_palette(self):
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setColor(self.backgroundRole(), "white");
        self.setPalette(palette)

    def setup_win_icon(self):
        installationfolder = os.path.dirname(os.path.dirname(__file__))
        icon = QtGui.QIcon(f"{installationfolder}/images/icon.png")
        self.setWindowIcon(icon)

    def new_file(self):
        self.main_layout.reset_ui()
        self.set_filename(None)
        self.clear_app_funcs()
        self.create_new_func()

    def open_file(self, filename=None):
        if not filename:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, "Open File")[0]
            if not filename: return 0

        self.main_layout.reset_ui()
        self.set_filename(filename)
        self.clear_app_funcs()
        self.parse_file()

    def parse_file(self):
        try:
            file = open(self.filename)
            for line in file:
                self.parse_file_line(line)

        except IndexError:
            file.close()
            self.alert_invalid_file(line)

    def parse_file_line(self, line):
        name = line.split("=")[0].strip()
        context = line.split("=")[1].strip()
        print(line)
        if name in ("start", "end", "n_points"):
            self.set_x_range(name, context)
        else:
            self.create_new_func(name, context)

    def set_x_range(self, name, context):
        x_settings = list(self.main_layout.get_x_settings())
        if name == "start":
            x_settings[0] = context
        elif name == "end":
            x_settings[1] = context
        elif name == "n_points":
            x_settings[2] = context
        else:
            raise Exception
        self.main_layout.set_x_settings(x_settings)

            
    def alert_invalid_file(self, line):
        alrt = QtWidgets.QMessageBox()
        alrt.setWindowTitle("Failed to open the file")
        alrt.setText(f"The file is invalid:\n{line}")
        alrt.exec_()
    
    def get_x_settings(self):
        settings = self.main_layout.get_x_settings()
        names = ("start", "end", "n_points")
        string = ""
        i = 0
        while i < 3:
            string += names[i]+"="+str(settings[i])+"\n"
            i+=1

        return string

    def save_file(self):
        if not self.filename:
            self.save_file_as()
            return 0

        context = self.read_app_funcs_context()
        context += self.get_x_settings()

        with open(self.filename, "w") as file:
            file.write(context)

    def read_app_funcs_context(self):
        context = ""
        for foo in self.get_funcs():
            context += foo.get_name() + "=" + foo.get_text() + "\n"

        return context

    def save_file_as(self, filename=None):
        if not filename:
            filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')[0]
            if not filename: return 0

        self.set_filename(filename)
        self.save_file()

    def create_x(self):
        start, end, step = self.main_layout.get_x_range()
        count = start

        # Count from start to end
        while abs(count) < abs(end + step/2):
            yield count
            count += step

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
                ax.plot(list(self.create_x()), data)

        self.main_layout.update_canvas()

    def alert_failed_func(self, app_func, error):
        alrt = QtWidgets.QMessageBox()
        alrt.setWindowTitle("Failed to evaluate the expression")
        alrt.setText(f"Your expression is wrong:\n in app_func {app_func.name}:\n {error}")
        alrt.exec_()

    def create_new_func(self, name="", context=""):
        if not name:
            name = f"f{len(self.app_funcs)+1}(x)"

        func = AppFunc(name, self)
        func.set_text(context)
        self.main_layout.add_app_func(func)
        self.app_funcs.append(func)
        func.focus()

    def clear_app_funcs(self):
        for f in self.get_funcs()[:]:
            self.delete_func(f)

    def delete_func(self, foo):
        foo.delete()

    def get_funcs(self):
        return self.app_funcs

    def update_funcs_names(self):
        for count, f in enumerate(self.app_funcs):
            name = f"f{count+1}(x)"
            f.set_name(name)

    def remove_from_app_funcs_list(self, app_func):
        self.app_funcs.remove(app_func)

    def set_filename(self, new_filename):
        self.filename = new_filename
        self.set_title_from_filename(new_filename)

    def set_title_from_filename(self, filename):
        if not filename:
            filename = "untiteld"

        else:
            filename = os.path.split(filename)[-1]

        filename += "  -  LDV-plt"
        self.setWindowTitle(filename)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
