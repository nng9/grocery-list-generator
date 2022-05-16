
## Have a list of recipes

## You can add recipes

## You can edit recipes

## Needs to have a section where you add recipes to a list

## Send you an email with your shopping list and meal plan

## Import Recipes using JSON or CSV

## Export Recipes using JSON or CSV

## Ingredients need name, unit, and quantity    

## Have it such that I can add text into text fields and click a button and it will print out to terminal success

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

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

        layout = QVBoxLayout()
        layout.addWidget(self.recipe_name_label)
        layout.addWidget(self.recipe_name_input)
        layout.addWidget(self.recipe_servings_label)
        layout.addWidget(self.recipe_servings_input)
        layout.addWidget(self.submit_button)
        
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

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
            self.recipe_name_input.clear()
            self.recipe_servings_input.clear()

if __name__ == '__main__':

   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()

   ## Initiates the event loop 
   app.exec_()


'''
class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients
    
    def get_ingredients(self):
        return self.ingredients
    
    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)
    
    def remove_ingredient(self, ingredient):
        try:
            self.ingredients.remove(ingredient)
        except ValueError:
            print("{} not in list".format(ingredient))

'''