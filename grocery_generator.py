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
class Instruction:
    def __init__(self):
        self.instruction = {}
        self.highest_step = 0
    
    def add_step(self, step):
        self.highest_step += 1
        self.instruction[self.highest_step] = step
    
    def return_instructions(self):
        instructions = ""
        counter = 0


# data structure that holds name, units, and quantity of an ingredient
class Ingredient:
    def __init__(self, name, unit, quantity):
        self.name = name
        self.unit = unit
        self.quantity = quantity

## Class for storing recipe information ##
class Recipe:
    def __init__(self, recipe_name, servings, author):
        self.name = recipe_name
        self.servings = servings
        self.author = author
        self.ingredients = {}
        self.instructions = []
    
    def add_ingredient(self, ingredient, unit, quantity):
        ##TODO add some error checking of inputs

        if ingredient in self.ingredients:
            self.ingredients[ingredient].unit = unit
            self.ingredients[ingredient].quantity = quantity
        else:
            self.ingredients[ingredient] = Ingredient(ingredient, unit, quantity)
        
    def add_instruction(self, step):
        self.instructions.append(step)

    def print_instructions(self):
        counter = 1
        for step in self.instructions:
            print("Step {count}: {step}".format(count=counter, step=step))
            counter += 1
    
    
    
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
        test_recipe.add_instruction("Turn the stove to medium heat and place ribs in.")
        test_recipe.add_instruction("Sear the meat until all sides are brown")
        test_recipe.print_instructions()
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
        self.instructions = QListWidget()

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
            self.ingredient_list.addItem("{quantity} {unit} of {ingredient}".format(\
                quantity=ingredient.quantity, unit=ingredient.unit, ingredient=ingredient.name))
        count = 1
        for step in recipe.instructions:
            self.instructions.addItem("Step {count}: {step}.".format(count=count, step=step))
            count += 1
        
    
if __name__ == '__main__':

   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec_()




        