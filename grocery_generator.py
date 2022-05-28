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
    QListWidget, QHBoxLayout, QVBoxLayout, QTextBrowser, QStackedLayout
    
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
        self.setWindowTitle("Grocery List App")
        self.setMinimumSize(700, 500)

        self.recipe_master = {}
        self.add_test_data()
        self.build_gui()
        self.connect_signals_to_slots()
    
    def build_gui(self):
        self.actionList = ["View", "Add", "Edit"]
        view_widget = self.build_view_widget()
        add_widget = self.build_add_widget()
        
        self.page_switcher = QStackedLayout()
        self.page_switcher.addWidget(view_widget)
        self.page_switcher.addWidget(add_widget)     
        container = QWidget()
        container.setLayout(self.page_switcher)
        self.setCentralWidget(container)
 
    def build_view_widget(self):
        #Widgets
        self.actionMenu = QComboBox()
        self.actionMenu.addItems(self.actionList)
        self.recipeList = QListWidget()
        self.recipeList.addItems(list(self.recipe_master.keys()))
        self.view_recipe_label = QLabel()
        self.view_author_label = QLabel()
        self.view_servings_label = QLabel()
        self.view_ingredient_list = QListWidget()
        self.view_instructions = QListWidget() #TODO Change to textedit
        instruction_label = QLabel("Instructions")
        ingredient_label = QLabel("Ingredients")
        
        # Left Panel 
        left_panel = QVBoxLayout()
        left_panel.addWidget(self.actionMenu)
        left_panel.addWidget(self.recipeList)

        # Right Panel
        right_panel = QVBoxLayout()
        header_bar = QHBoxLayout()
        header_bar.addWidget(self.view_recipe_label)
        header_bar.addWidget(self.view_author_label)
        right_panel.addLayout(header_bar)
        right_panel.addWidget(self.view_servings_label)
        right_panel.addWidget(ingredient_label)
        right_panel.addWidget(self.view_ingredient_list)
        right_panel.addWidget(instruction_label)
        right_panel.addWidget(self.view_instructions)
        
        combined_layout = QHBoxLayout()
        combined_layout.addLayout(left_panel)
        combined_layout.addLayout(right_panel)
        view_widget = QWidget()
        view_widget.setLayout(combined_layout)

        return view_widget
    
    def build_add_widget(self):
        #Widgets
        recipe_label = QLabel("Recipe Name:")
        author_label = QLabel("Author Name:")
        servings_label = QLabel("Servings:")
        ingredient_name_label = QLabel("Ingredient Name:")
        ingredient_units_label = QLabel("Measurement Unit:")
        ingredient_quantity_label = QLabel("Quantity:")
        ingredient_label = QLabel("Ingredients")

        self.add_actionMenu = QComboBox()
        self.add_actionMenu.addItems(self.actionList)
        self.add_recipeList = QTextBrowser()
        temp_string = ""
        for recipe_name in list(self.recipe_master.keys()):
            temp_string += recipe_name
            temp_string += "\n"
        self.add_recipeList.setText(temp_string)

        self.recipe_name_input = QLineEdit()
        self.author_name_input = QLineEdit()
        self.servings_input = QLineEdit()
        self.ingredient_name_input = QLineEdit()
        self.ingredient_unit_input = QLineEdit()
        self.ingredient_quantity_input = QLineEdit()
        self.ingredient_table = QTextBrowser()
        self.add_ingredient_btn = QPushButton("Add Ingredient")
        self.delete_ingredient_btn = QPushButton("Delete Ingredient")
        self.submit_button = QPushButton("Submit")

        # Left Panel
        left_panel = QVBoxLayout()
        left_panel.addWidget(self.add_actionMenu)
        left_panel.addWidget(self.add_recipeList)
        
        # Right Panel
        right_panel = QVBoxLayout()
        recipe_line = QHBoxLayout()
        recipe_line.addWidget(recipe_label)
        recipe_line.addWidget(self.recipe_name_input)
        
        author_line = QHBoxLayout()
        author_line.addWidget(author_label)
        author_line.addWidget(self.author_name_input)

        servings_line = QHBoxLayout()
        servings_line.addWidget(servings_label)
        servings_line.addWidget(self.servings_input)
        
        add_delete_ingred_line = QHBoxLayout()
        add_delete_ingred_line.addWidget(self.add_ingredient_btn)
        add_delete_ingred_line.addWidget(self.delete_ingredient_btn)

        ingredient_line = QHBoxLayout()
        ingredient_line.addWidget(ingredient_name_label)
        ingredient_line.addWidget(self.ingredient_name_input)

        units_line = QHBoxLayout()
        units_line.addWidget(ingredient_units_label)
        units_line.addWidget(self.ingredient_unit_input)

        quantity_line = QHBoxLayout()
        quantity_line.addWidget(ingredient_quantity_label)
        quantity_line.addWidget(self.ingredient_quantity_input)

        right_panel.addLayout(recipe_line)
        right_panel.addLayout(author_line)
        right_panel.addLayout(servings_line)
        right_panel.addWidget(ingredient_label)
        right_panel.addWidget(self.ingredient_table)
        right_panel.addLayout(ingredient_line)
        right_panel.addLayout(units_line)
        right_panel.addLayout(quantity_line)
        right_panel.addLayout(add_delete_ingred_line)
        right_panel.addWidget(self.submit_button)

        combined_layout = QHBoxLayout()
        combined_layout.addLayout(left_panel)
        combined_layout.addLayout(right_panel)

        widget = QWidget()
        widget.setLayout(combined_layout)
        return widget

    def connect_signals_to_slots(self):
        self.recipeList.itemPressed.connect(self.recipe_pressed)
        self.actionMenu.activated.connect(self.change_page)
        self.add_actionMenu.activated.connect(self.change_page)
        #self.submit_button.clicked.connect(self.submit_pushed)

    def change_page(self, index):
        self.page_switcher.setCurrentIndex(index)    

    def add_test_data(self):
        test_recipe = Recipe("Ribs and Cauliflower", 2, "Susan Xie")
        test_recipe.add_ingredient("Ribs", "lb", "1")
        test_recipe.add_ingredient("Cauliflower", "bunch", "1")
        test_recipe.print_ingredients()
        test_recipe.add_instruction("Turn the stove to medium heat and place ribs in.")
        test_recipe.add_instruction("Sear the meat until all sides are brown")
        test_recipe.print_instructions()
        self.recipe_master.update({test_recipe.name: test_recipe})

    ## Function that handles the event when a recipe is clicked in the recipe list
    def recipe_pressed(self, item):
        print("{} was selected".format(item.text()))
        recipe = self.recipe_master[item.text()]
        self.view_recipe_label.setText(recipe.name)
        self.view_author_label.setText("By: {}".format(recipe.author))
        self.view_servings_label.setText("Servings: {}".format(recipe.servings))
        ## Add each ingredient to the list
        for ingredient in list(recipe.ingredients.values()):
            self.view_ingredient_list.addItem("{quantity} {unit} of {ingredient}".format(\
                quantity=ingredient.quantity, unit=ingredient.unit, ingredient=ingredient.name))
        count = 1
        for step in recipe.instructions:
            self.view_instructions.addItem("Step {count}: {step}.".format(count=count, step=step))
            count += 1
        
    
if __name__ == '__main__':

   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec_()




        