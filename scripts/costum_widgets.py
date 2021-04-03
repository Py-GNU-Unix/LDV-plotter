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


from PySide2 import QtWidgets, QtCore, QtGui
import sys
import os

class MainMenu(QtWidgets.QMenuBar):
    def __init__(self, main_window):
        QtWidgets.QMenuBar.__init__(self, main_window)
        self.main_window = main_window

        self.create_actions()
        self.connect_actions()
        self.add_actions()

    def create_actions(self):
        self.new_action = QtWidgets.QAction("New")
        self.open_action = QtWidgets.QAction("Open")
        self.save_action = QtWidgets.QAction("Save")
        self.save_as_action = QtWidgets.QAction("Save as")
        self.quit_action = QtWidgets.QAction("Quit")

    def connect_actions(self):
        self.new_action.triggered.connect(lambda: self.main_window.new_file())
        self.open_action.triggered.connect(self.main_window.open_file)
        self.save_action.triggered.connect(self.main_window.save_file)
        self.save_as_action.triggered.connect(self.main_window.save_file_as)
        self.quit_action.triggered.connect(lambda: sys.exit(0))

    def add_actions(self):
        self.addAction(self.new_action)
        self.addAction(self.open_action)
        self.addAction(self.save_action)
        self.addAction(self.save_as_action)
        self.addAction(self.quit_action)

class VerticalCostumLayout(QtWidgets.QVBoxLayout):
    def __init__(self, parent):
        QtWidgets.QVBoxLayout.__init__(self)
        self.parent = parent
        self.config()

    def config(self):
        self.create_widgets()
        self.configure_widgets()
        self.add_widgets()

    def create_widgets(self):
        raise NotImplementedError

    def configure_widgets(self):
        raise NotImplementedError

    def add_widgets(self):
        raise NotImplementedError

class CostumEntry(QtWidgets.QLineEdit):
    def __init__(self, value):
        self.__value = str(value)
        QtWidgets.QLineEdit.__init__(self, self.__value)
        self.setReadOnly(True)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    def value(self):
        return self.__value

    def setValue(self, new_value):
        self.__value = new_value

        shown = str(new_value)
        if len(shown) >= 15:
            shown = shown[:15] + "..."


        self.setText(shown)

class AppFunc(QtWidgets.QHBoxLayout):
    def __init__(self, name, master):
        QtWidgets.QHBoxLayout.__init__(self)
        self.name = name
        self.master = master
        self.configure()

    def configure(self):
        self.create_widgets()
        self.add_widgets()
        self.set_focus_policy()

    def add_widgets(self):
        self.addWidget(self.entry_doc)
        self.addWidget(self.entry)
        self.addWidget(self.close_button)

    def set_focus_policy(self):
        self.entry.setFocusPolicy(QtCore.Qt.StrongFocus)

    def create_widgets(self):
        self.entry = QtWidgets.QLineEdit()
        self.entry_doc = QtWidgets.QLabel(f"{self.name} = ")
        self.create_close_button()

    def create_close_button(self):
        self.close_button = QtWidgets.QPushButton("X")
        self.close_button.clicked.connect(self.delete)


        installationfolder = os.path.dirname(os.path.dirname(__file__))
        css = open(f"{installationfolder}/stylesheets/close_button_stylesheet.css","r").read()
        self.close_button.setStyleSheet(css)

    def delete(self):
        self.master.remove_from_app_funcs_list(self)
        self.master.update_funcs_names()
        self.delete_widgets()

    def delete_widgets(self):
        self.entry.deleteLater()
        self.entry_doc.deleteLater()
        self.close_button.deleteLater()

    def focus(self):
        self.entry.setFocus()

    def set_name(self, name):
        self.name = name
        self.entry_doc.setText(f"{name} = ")

    def set_text(self, text):
        self.entry.setText(text)

    def get_name(self):
        return self.name

    def get_text(self):
        return self.entry.text()
