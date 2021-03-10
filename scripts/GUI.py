import sys
import func_generator
from PySide2 import QtWidgets, QtCore, QtGui
import matplotlib.pyplot as plt
import os

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from layouts import MainLayout

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
        self.entry.setFocusPolicy(QtCore.Qt.StrongFocus)
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
    
    def get_name(self):
        return self.name

    def get_layout(self):
        return self.layout

    def get_text(self):
        return self.entry.text()

    def set_text(self, text):
        self.entry.setText(text)
    
    def focus(self):
        self.entry.setFocus()

class MainWindow(QtWidgets.QWidget):
    def __init__(self, filename=None):
        QtWidgets.QWidget.__init__(self)
        self.set_filename(filename)
        self.setup_win_style()
        self.setup_layout()
        self.setup_file()

    def setup_win_style(self):
        icon = QtGui.QIcon("../images/icon.png")
        self.setWindowIcon(icon)
        
        self.setAutoFillBackground(True)
        palette = QtGui.QPalette()
        palette.setColor(self.backgroundRole(), "white");
        self.setPalette(palette)

    def setup_layout(self):
        self.app_funcs = []
        self.main_layout = MainLayout(self)
        self.setLayout(self.main_layout)

    def setup_file(self):
        if not self.filename:
            self.new_file(alert=False)
        else:
            self.open_file(self.filename)
    
    def new_file(self, alert=True):
        self.set_filename(None)
        self.clear_funcs()
        self.add_new_func()
        
        if alert:
            self.alert_new_file()
    
    def open_file(self, filename=None):
        if filename:
            self.set_filename(filename)
        else:
            f = QtWidgets.QFileDialog.getOpenFileName(self, "Open File")[0] 
            
            if not f: return 0
        
            self.set_filename(f)
        
        self.clear_funcs()
        
        try:
            for line in open(self.filename):
                name = line.split("=")[0].strip()
                context = line.split("=")[1].strip()
                self.add_new_func(name, context)
        except IndexError:
            self.alert_invalid_file(line)
    
    def save_file(self):
        if not self.filename:
            self.save_file_as()
            return 0
        
        context = ""
        for foo in self.get_funcs():
            context += foo.get_name() + "=" + foo.get_text() + "\n"
        
        with open(self.filename, "w") as file:
            file.write(context)
    
    def save_file_as(self, filename=None):
        if not filename:
            f = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')[0]
            
            if not f: return 0
            self.set_filename(f)
        else:
            self.filename = filename
            
        self.save_file()
        
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
    
    def alert_invalid_file(self, line):
        alrt = QtWidgets.QMessageBox()
        alrt.setWindowTitle("Failed to open the file")
        alrt.setText(f"The file is invalid:\n{line}")
        alrt.exec_()        
        
    def alert_new_file(self):
        alrt = QtWidgets.QMessageBox()
        alrt.setWindowTitle("New file created")
        alrt.setText("  You created a new file  ")
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

    def add_new_func(self, name="", context=""):
        if not name:
            name = f"f{len(self.app_funcs)+1}(x)"

        func = AppFunc(name, self)
        func.set_text(context)
        self.main_layout.add_app_func(func)
        self.app_funcs.append(func)
        func.focus()

    def delete_func(self, foo):
        foo.delete()
    
    def clear_funcs(self):
        for f in self.get_funcs()[:]:
            self.delete_func(f)

    def update_funcs_names(self):
        count = 0
        for f in self.app_funcs:
            count += 1
            name = f"f{count}(x)"
            f.set_name(name)
    
    def set_filename(self, new):
        self.filename = new
        
        if new == None:
            new = "untiteld"
        else:
            new = os.path.split(new)[-1]
        
        new += " - LDV-plt"
        
        self.setWindowTitle(new)
        

app = QtWidgets.QApplication(sys.argv)

x = MainWindow()
x.show()
sys.exit(app.exec_())
