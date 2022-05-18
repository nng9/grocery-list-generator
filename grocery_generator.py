## TODO

# Remove the ability to edit directly in the table (do not want Spreadsheet style)
# Want a push button for "Add Recipe"
# A comboBox with the recipes and an "Edit Recipe" push button
# Send you an email with your shopping list and meal plan
# Import Recipes using a JSON or CSV
# Export Recipes using JSON or CSV
# Ingredients need name, unit, and quantity    

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, \
 QVBoxLayout, QWidget, QLineEdit, QTableWidget, QTableWidgetItem

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ### Build GUI Elements ###
        self.setWindowTitle("Grocerly List App")

        self.recipe_name_label = QLabel("Recipe Name")
        self.recipe_name_label.setFixedHeight(25)
        self.recipe_name_label.setFixedWidth(100)

        self.recipe_name_input = QLineEdit()
        self.recipe_name_input.setFixedHeight(30)
        self.recipe_name_input.setFixedWidth(100)

        self.recipe_servings_label = QLabel("Number of servings")
        self.recipe_servings_label.setFixedHeight(25)
        self.recipe_servings_label.setFixedWidth(150)

        self.recipe_servings_input = QLineEdit()
        self.recipe_servings_input.setFixedHeight(30)
        self.recipe_servings_input.setFixedWidth(100)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedHeight(30)
        self.submit_button.setFixedWidth(65)

        self.recipe_table = QTableWidget(0, 2)
        self.recipe_table.setHorizontalHeaderLabels(["Recipe", "Servings"])

        ### Organize Layout of GUI Elements
        layout = QVBoxLayout()
        layout.addWidget(self.recipe_name_label)
        layout.addWidget(self.recipe_name_input)
        layout.addWidget(self.recipe_servings_label)
        layout.addWidget(self.recipe_servings_input)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.recipe_table)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        ### Initialize Global Variables ###
        self.recipe_name_master = {}

        ### Signals ###
        self.submit_button.clicked.connect(self.submit_pushed)

    def submit_pushed(self):
        print("submit button pushed")
        name = self.recipe_name_input.text()
        servings = self.recipe_servings_input.text()
        valid_entries = True

        if len(name) == 0:
            print("Recipe name field is empty. Please enter value.")
            valid_entries = False
        
        if len(servings) == 0:
            print("Servings field is empty. Please enter value")
            valid_entries = False
        
        if not servings.isnumeric():
            print("Servings value is not a number. Please enter a number.")
            valid_entries = False
        
        if valid_entries:
            print("Recipe name is: {} and it serves {} people".format(name, servings))

            self.add_recipe(name, servings)
            self.recipe_name_input.clear()
            self.recipe_servings_input.clear()

    def add_recipe(self, name, servings):
    
        if self.recipeDoesNotExist(name):
            recipe_name = QTableWidgetItem(name)
            recipe_servings = QTableWidgetItem(servings)
            self.recipe_name_master.update({name: True})

            self.recipe_table.setRowCount(self.recipe_table.rowCount()+1)
            self.recipe_table.setItem(self.recipe_table.rowCount()-1, 0, recipe_name)
            self.recipe_table.setItem(self.recipe_table.rowCount()-1, 1, recipe_servings)
        else:
            print("You have attempted to add a recipe name that already exists. The recipe was not added.")
    
    def recipeDoesNotExist(self, recipe):
        if recipe in self.recipe_name_master:
            return False
        return True

if __name__ == '__main__':

   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec_()
