from PyQt6 import QtCore,  QtWidgets
import sys
import os
# Add the project's root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.construct_tableau import construct_tableau
from functions.simplex_iteration import simpleximplementation
from functions.BigM import BigM
from functions.TwoPhase import two_phase_simplex


class Ui_Dialog(object):

    def setupUi(self, Dialog, main_app):

        self.lineEdits_obj = [] 
        self.constraintRows = [] 
        self.lineEdits_vec = []  
        self._2Darray = []  
        self.simplex = 1

        Dialog.setObjectName("Dialog")
        Dialog.resize(600, 600)
        Dialog.setStyleSheet("background-color: rgba(220, 220, 220, 0.5);")
        self.main_app = main_app
        
        self.widget = QtWidgets.QWidget(parent=Dialog)
        self.widget.setGeometry(QtCore.QRect(20, 20, 560, 560))
        self.widget.setStyleSheet("""
            background-color: rgba(245, 245, 245, 0.7);  /* Semi-transparent gray */

        """)
        
        self.label = QtWidgets.QLabel("Enter the number of variables in the objective function:", parent=self.widget)
        self.label.setGeometry(QtCore.QRect(20, 10, 400, 30))
        self.label.setStyleSheet("border-radius: 2px;font-size: 14px; font-weight: bold; color: #333;")
          
        self.lineEdit = QtWidgets.QLineEdit(parent=self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 45, 180, 30))
        self.lineEdit.setPlaceholderText("Enter Here")
        self.lineEdit.setStyleSheet("border: 0.5px solid rgba(150, 150, 150, 0.9);border-radius: 2px;font-size: 14px; font-weight: bold; color: #334;")
        
        self.pushButton_setVars = QtWidgets.QPushButton("Set", parent=self.widget)
        self.pushButton_setVars.setGeometry(QtCore.QRect(220, 45, 100, 30))
        self.pushButton_setVars.setStyleSheet("border-radius: 2px; background-color: #008CBA; color: white;")
         
        self.label_2 = QtWidgets.QLabel("Enter the coefficients of the objective function:", parent=self.widget)
        self.label_2.setGeometry(QtCore.QRect(20, 88, 520, 30))
        self.label_2.setStyleSheet("border-radius: 2px;font-size: 14px; font-weight: bold; color: #333;")

        self.widget_2 = QtWidgets.QWidget(parent=self.widget)
        self.widget_2.setGeometry(QtCore.QRect(20, 121, 520, 40))
        self.widget_2.setStyleSheet("border: 0.5px solid rgba(150, 150, 150, 0.9);border-radius: 2px;font-size: 14px; font-weight: bold; color: #333;")
        self.layout_obj = QtWidgets.QHBoxLayout(self.widget_2)

        self.dropdown1 = QtWidgets.QComboBox(parent=self.widget_2)
        self.dropdown1.addItems(["Maximize", "Minimize"])
        self.layout_obj.addWidget(self.dropdown1)

        self.pushButton = QtWidgets.QPushButton("Add a constraint row", parent=self.widget)
        self.pushButton.setGeometry(QtCore.QRect(20, 174, 200, 30))
        self.pushButton.setStyleSheet("border-radius: 2px; background-color:#008CBA; color: white;")

        self.dropdown2 = QtWidgets.QComboBox(parent=self.widget)
        self.dropdown2.addItems(["Big M", "Two Phase"])
        self.dropdown2.setGeometry(QtCore.QRect(340, 174, 200, 30))
        self.dropdown2.setStyleSheet("border: 0.5px solid rgba(150, 150, 150, 0.9);border-radius: 2px;font-size: 14px; font-weight: bold; color: #333;")


        self.scrollArea = QtWidgets.QScrollArea(parent=self.widget)
        self.scrollArea.setGeometry(QtCore.QRect(20, 210, 520, 200))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.constraintsLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)

        self.label_3 = QtWidgets.QLabel("Enter decision variables' constraints (≤ restricted,- unrestricted)", parent=self.widget)
        self.label_3.setGeometry(QtCore.QRect(20, 419, 520, 30))
        self.label_3.setStyleSheet("border-radius: 2px;font-size: 14px; font-weight: bold; color: #333;")


        self.widget_3 = QtWidgets.QWidget(parent=self.widget)
        self.widget_3.setGeometry(QtCore.QRect(20, 450, 520, 40))
        self.widget_3.setStyleSheet("border: 0.5px solid rgba(150, 150, 150, 0.9);border-radius: 2px;font-size: 14px; font-weight: bold; color: #333;")
        self.layout_vec = QtWidgets.QHBoxLayout(self.widget_3)

         

        self.pushButton_2 = QtWidgets.QPushButton("Submit", parent=self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(380, 510, 161, 30))
        self.pushButton_2.setStyleSheet("border-radius: 2px; background-color:#008CBA; color: white;")

        self.pushButton_3 = QtWidgets.QPushButton("Back", parent=self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 510, 161, 30))
        self.pushButton_3.setStyleSheet("border-radius: 2px; background-color: #008CBA; color: white;")


        self.pushButton.clicked.connect(self.addConstraintRow)
        self.pushButton_setVars.clicked.connect(self.updateVariables)
        self.pushButton_2.clicked.connect(self.onSubmit)



    def updateVariables(self):
        num_vars = int(self.lineEdit.text()) if self.lineEdit.text().isdigit() else 4

        for lineEdit in self.lineEdits_obj:
            lineEdit.deleteLater()
        self.lineEdits_obj.clear()

        for lineEdit, constraint_type in self.lineEdits_vec:
            lineEdit.deleteLater()
            constraint_type.deleteLater()
        self.lineEdits_vec.clear()

        for i in reversed(range(self.constraintsLayout.count())):
            item = self.constraintsLayout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()

        self.constraintRows.clear()

        for i in range(num_vars):
            lineEdit = QtWidgets.QLineEdit()
            lineEdit.setPlaceholderText(f"x{i+1}")
            self.layout_obj.insertWidget(i, lineEdit)
            self.lineEdits_obj.append(lineEdit)

        for i in range(num_vars):
            label = QtWidgets.QLabel(f"x{i+1}")
            self.layout_vec.insertWidget(i*2, label)

            constraint_type = QtWidgets.QComboBox()
            constraint_type.addItems(["≤", "-"])
            self.layout_vec.insertWidget(i * 2 + 1,constraint_type)

            self.lineEdits_vec.append((label, constraint_type))
    

    def extractValues(self):
        self._2Darray.clear()
        row = []

        for lineEdit in self.lineEdits_obj:
            text = lineEdit.text().strip()
            try:
                row.append(float(text))  
            except ValueError:
                row.append(0)  

        # print(self.dropdown1.currentText()  +"jjj")

        row.append(0)    
        row.append(0)

        self._2Darray.append(row)

    def addConstraintRow(self):
        row_widget = QtWidgets.QWidget()
        row_layout = QtWidgets.QHBoxLayout(row_widget)

        num_vars = len(self.lineEdits_obj)
        row = []

        for i in range(num_vars):
            lineEdit = QtWidgets.QLineEdit()
            lineEdit.setPlaceholderText(f"x{i+1}")
            row_layout.addWidget(lineEdit)
            row.append(lineEdit)

        constraint_type = QtWidgets.QComboBox()
        constraint_type.addItems(["≤", "=", "≥"])
        row_layout.addWidget(constraint_type)

        rhs = QtWidgets.QLineEdit()
        rhs.setPlaceholderText("RHS")
        row_layout.addWidget(rhs)

        self.constraintsLayout.addWidget(row_widget)
        self.constraintRows.append((row, constraint_type, rhs)) 

    def extractConstraints(self):
        """extract values from constraint rows on submit."""
        constraint_map = {"=": 0, "≤": -1, "≥": 1}

        for row_inputs, constraint_type, rhs in self.constraintRows:
            row_values = []

            for edit in row_inputs:
                text = edit.text().strip()
                try:
                    row_values.append(float(text))  
                except ValueError:
                    row_values.append(0)

            row_values.append(constraint_map[constraint_type.currentText()])
            if(constraint_map[constraint_type.currentText()] == 1):
                self.simplex = 0
                print(constraint_map[constraint_type.currentText()],self.simplex)

            rhs_text = rhs.text().strip()
            try:
                row_values.append(float(rhs_text))  
            except ValueError:
                row_values.append(0)

            self._2Darray.append(row_values)

        # print("2Darray:", self._2Darray)

    def onSubmit(self):

        self.extractValues()  
        self.extractConstraints()

        vec = []

        for _, constraint_type in self.lineEdits_vec:
            vec.append(1 if constraint_type.currentText() == "≤" else -1)

        constraints = (int)(len(self._2Darray) -1)
        varnum = (int)(self.lineEdit.text())

        tableau,vararr,basic_vars = construct_tableau(self._2Darray,vec,varnum,constraints)
        maxi = 1 if self.dropdown1.currentText() == "Maximize" else 0       
        # print("maxi", maxi)
        # print("maxi",self.dropdown2.currentText() )
        # print("self.simplex", self.simplex)

        if(self.simplex == 1):
            tableau[0] *= -1
            self.output_text, _, _, _ = simpleximplementation(tableau,vararr,basic_vars,maxi)

            # print(self.output_text)

            # if hasattr(self, 'main_app'):  # ensure main_app exists
            #     self.main_app.go_to_output(self.output_text)
            #     print("jaanr: hereee") 
            # else:
            #     print("Error: main_app is not set in Ui_Dialog") 

        elif(self.dropdown2.currentText() == "Big M"):
            # print("maxi", "jjjjj")
            self.output_text = BigM(tableau,vararr,basic_vars,maxi)

        elif(self.dropdown2.currentText() == "Two Phase"):
            # print("maxi", "jjjjj")
            self.output_text = two_phase_simplex(self._2Darray,tableau,vararr,basic_vars,maxi)

        self.main_app.go_to_output(self.output_text)   


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Linear Programming Solver"))
        self.label.setText(_translate("Dialog", "Linear Programming Solver"))
        self.pushButton.setText(_translate("Dialog", "Linear Programming Solver"))
