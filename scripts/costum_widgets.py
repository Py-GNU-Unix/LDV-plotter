from PySide2 import QtWidgets, QtCore, QtGui

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

        css = open("../stylesheets/close_button_stylesheet.css","r").read()
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
    
