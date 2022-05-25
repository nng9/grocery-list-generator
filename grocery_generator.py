## TODO

# Create a view area for people to see their recipe after selecting it in the table
# Want a push button for "Add Recipe"
# A comboBox with the recipes and an "Edit Recipe" push button
# Send you an email with your shopping list and meal plan
# Import Recipes using a JSON or CSV
# Export Recipes using JSON or CSV
# Ingredients need name, unit, and quantity
# Adding a database will allow users to share recipes with one another    

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, \
    QVBoxLayout, QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QComboBox, \
    QListWidget, QHBoxLayout, QVBoxLayout, QTextBrowser

# Ingredient data structure that holds name, units, and quantity of an ingredient
class Ingredient:
    def __init__(self, name, unit, quantity):
        self.name = name
        self.unit = unit
        self.quantity = quantity

## Class for storing recipe information ##
## Recipe Name, Servings, Author Name, Ingredients List, Instructions
class Recipe:
    def __init__(self, recipe_name, servings, author):
        self.name = recipe_name
        self.servings = servings
        self.author = author
        self.ingredients = {}
        self.instructions = {}
    
    def add_ingredient(self, ingredient, unit, quantity):
        ##TODO add some error checking of inputs

        if ingredient in self.ingredients:
            self.ingredients[ingredient].unit = unit
            self.ingredients[ingredient].quantity = quantity
        else:
            self.ingredients[ingredient] = Ingredient(ingredient, unit, quantity)
        
    
    def print_ingredients(self):
        for ingredient in list(self.ingredients.values()):
            print("{quantity} {unit} of {ingredient}".format(quantity=ingredient.quantity\
                , unit=ingredient.unit, ingredient=ingredient.name))
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.recipe_master = {}
        test_recipe = Recipe("Ribs and Cauliflower", 2, "Susan Xie")
        test_recipe.add_ingredient("Ribs", "lb", "1")
        test_recipe.add_ingredient("Cauliflower", "bunch", "1")
        test_recipe.print_ingredients()
        self.recipe_master.update({test_recipe.name: test_recipe})

        ### Widgets ###
        self.setWindowTitle("Grocery List App")
        self.setFixedSize(700, 500)

        self.actionMenu = QComboBox()
        self.actionMenu.addItems(["View Recipe", "Add Recipe", "Edit Recipe"])

        self.recipeList = QListWidget()
        self.recipeList.addItems(list(self.recipe_master.keys()))

        self.recipe_label = QLabel()
        self.author_label = QLabel()

        self.servings_label = QLabel("Servings: ")

        self.ingredient_label = QLabel("Ingredients")
        self.ingredient_list = QListWidget()
    
        self.instruction_label = QLabel("Instructions")
        self.instructions = QTextBrowser()

        #self.instructions.setSource("./instructions.txt")

        ### Create Left and Right Panel ###
        h_layout = QHBoxLayout()
        v_layout_left = QVBoxLayout()
        v_layout_right = QVBoxLayout()
        h_layout.addLayout(v_layout_left)
        h_layout.addLayout(v_layout_right)
        layout = h_layout

        ### Add Widgets to Left Panel ##
        v_layout_left.addWidget(self.actionMenu)
        v_layout_left.addWidget(self.recipeList)

        ## Add Widgets to Right Panel - View Recipes ##
        header_bar = QHBoxLayout()
        header_bar.addWidget(self.recipe_label)
        header_bar.addWidget(self.author_label)
        v_layout_right.addLayout(header_bar)
        v_layout_right.addWidget(self.servings_label)
        v_layout_right.addWidget(self.ingredient_label)
        v_layout_right.addWidget(self.ingredient_list)
        v_layout_right.addWidget(self.instruction_label)
        v_layout_right.addWidget(self.instructions)
                
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        ### Signals ###
        self.recipeList.itemPressed.connect(self.recipe_pressed)
        #self.submit_button.clicked.connect(self.submit_pushed)
    
    ## Function that handles the event when a recipe is clicked in the recipe list
    def recipe_pressed(self, item):
        print("{} was selected".format(item.text()))
        recipe = self.recipe_master[item.text()]
        self.recipe_label.setText(recipe.name)
        self.author_label.setText("By: {}".format(recipe.author))
        self.servings_label.setText("Servings: {}".format(recipe.servings))
        ## Add each ingredient to the list
        for ingredient in list(recipe.ingredients.values()):
            self.ingredient_list.addItem("{quantity} {unit}(s) of {ingredient}".format(\
                quantity=ingredient.quantity, unit=ingredient.unit, ingredient=ingredient.name))
        
    
if __name__ == '__main__':

   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec_()




        