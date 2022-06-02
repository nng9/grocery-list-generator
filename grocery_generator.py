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

from recipe import *

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, \
    QVBoxLayout, QWidget, QLineEdit, QTableWidget, QTableWidgetItem, QComboBox, \
    QListWidget, QHBoxLayout, QVBoxLayout, QTextBrowser, QStackedLayout, QListWidgetItem, \
    QAbstractItemView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grocery List App")
        self.setMinimumSize(700, 500)

        self.recipe_master = {}
        self.active_recipe = ""
        self.active_ingredient = ""

        self.add_test_data()
        self.build_gui()
        
        self.connect_signals_to_slots()
    
    def build_gui(self):
        self.actionList = ["Recipes"]
        recipe_page = self.build_recipe_widget()
        self.page_switcher = QStackedLayout()
        self.page_switcher.addWidget(recipe_page)     
        container = QWidget()
        container.setLayout(self.page_switcher)
        self.setCentralWidget(container)
        
    
    def build_recipe_widget(self):
        #Widgets
        self.add_actionMenu = QComboBox()
        self.add_actionMenu.addItems(self.actionList)
        self.add_recipeList = QListWidget()
        self.add_recipeList.addItems(list(self.recipe_master.keys()))
        self.recipe_name_input = QLineEdit()
        self.author_name_input = QLineEdit()
        self.servings_input = QLineEdit()
        self.ingredient_name_input = QLineEdit()
        self.ingredient_unit_input = QLineEdit()
        self.ingredient_quantity_input = QLineEdit()
        self.ingredient_table = QListWidget()
        self.add_ingredient_btn = QPushButton("New Ingredient")
        self.edit_ingredient_btn = QPushButton("Edit Ingredient")
        self.delete_ingredient_btn = QPushButton("Delete Ingredient")
        self.new_recipe_btn = QPushButton("New Recipe")
        self.edit_ingredients_list_btn = QPushButton("Edit Ingredients")

        # Left Panel
        left_panel = QVBoxLayout()
        left_panel.addWidget(self.add_actionMenu)
        left_panel.addWidget(self.new_recipe_btn)
        left_panel.addWidget(self.add_recipeList)
        
        # Right Panel
        right_panel = QVBoxLayout()
        recipe_line = QHBoxLayout()
        recipe_line.addWidget(QLabel("Recipe Name: "))
        recipe_line.addWidget(self.recipe_name_input)
        
        author_line = QHBoxLayout()
        author_line.addWidget(QLabel("Author Name: "))
        author_line.addWidget(self.author_name_input)

        servings_line = QHBoxLayout()
        servings_line.addWidget(QLabel("Servings:          "))
        servings_line.addWidget(self.servings_input)

        ingredient_label_line = QHBoxLayout()
        ingredient_label_line.addWidget(QLabel("Ingredients"))
        ingredient_label_line.addWidget(self.edit_ingredients_list_btn)
        
        edit_delete_ingred_line = QHBoxLayout()
        edit_delete_ingred_line.addWidget(self.edit_ingredient_btn)
        edit_delete_ingred_line.addWidget(self.delete_ingredient_btn)

        ingredient_line = QHBoxLayout()
        ingredient_line.addWidget(QLabel("Ingredient Name:"))
        ingredient_line.addWidget(self.ingredient_name_input)

        units_line = QHBoxLayout()
        units_line.addWidget(QLabel("Measurement Unit:"))
        units_line.addWidget(self.ingredient_unit_input)

        quantity_line = QHBoxLayout()
        quantity_line.addWidget(QLabel("Quantity:"))
        quantity_line.addWidget(self.ingredient_quantity_input)

        editing_ingredient_box = QVBoxLayout()
        editing_ingredient_box.addWidget(self.add_ingredient_btn)
        editing_ingredient_box.addLayout(ingredient_line)
        editing_ingredient_box.addLayout(units_line)
        editing_ingredient_box.addLayout(quantity_line)
        editing_ingredient_box.addLayout(edit_delete_ingred_line)

        self.edit_ingred_container = QWidget()
        self.edit_ingred_container.setLayout(editing_ingredient_box)

        right_panel.addLayout(recipe_line)
        right_panel.addLayout(author_line)
        right_panel.addLayout(servings_line)
        right_panel.addLayout(ingredient_label_line)
        right_panel.addWidget(self.ingredient_table)
        right_panel.addWidget(self.edit_ingred_container)
        self.edit_ingred_container.hide()

        combined_layout = QHBoxLayout()
        combined_layout.addLayout(left_panel)
        combined_layout.addLayout(right_panel)

        self.ingredient_table.setSelectionMode(QAbstractItemView.NoSelection)

        widget = QWidget()
        widget.setLayout(combined_layout)
        return widget

    def connect_signals_to_slots(self):
        #self.recipeList.itemPressed.connect(self.view_recipe_pressed)
        #self.actionMenu.activated.connect(self.change_page)
    
        ## Add/Edit Page
        self.add_recipeList.currentItemChanged.connect(self.add_edit_page_recipe_selected)
        self.add_actionMenu.activated.connect(self.change_page)
        self.ingredient_table.itemSelectionChanged.connect(self.ingredient_selected)
        self.add_ingredient_btn.pressed.connect(self.add_ingredient_btn_slot)
        self.edit_ingredient_btn.pressed.connect(self.edit_ingredient_btn_slot)
        self.edit_ingredients_list_btn.pressed.connect(self.edit_ingredients_list_btn_slot)

    def edit_ingredients_list_btn_slot(self):
        
        if self.edit_ingredients_list_btn.text()[0] == "E":
            self.edit_ingredients_list_btn.setText("Finish Editing")
            self.edit_ingred_container.show()
            self.ingredient_table.setSelectionMode(QAbstractItemView.SingleSelection)
        else:
            self.edit_ingredients_list_btn.setText("Edit Ingredients")
            self.edit_ingred_container.hide()
            self.ingredient_table.setCurrentRow(100)
            self.ingredient_table.setSelectionMode(QAbstractItemView.NoSelection)

    
    def add_test_data(self):
        test_recipe = Recipe("Ribs and Cauliflower", "2", "Susan Xie")
        test_recipe.add_ingredient("ribs", "lb", "1")
        test_recipe.add_ingredient("cauliflower", "bunch", "1")
        test_recipe.add_instruction("Turn the stove to medium heat and place ribs in.")
        test_recipe.add_instruction("Sear the meat until all sides are brown")
        self.recipe_master.update({test_recipe.name: test_recipe})

    ## Function that handles switching between the different pages when the actionBox changes
    def change_page(self, index):
        self.page_switcher.setCurrentIndex(index)    

    ## Function that handles the event when a recipe is clicked in the recipe list
    def view_recipe_pressed(self, item):
        recipe = self.recipe_master[item.text()]
        self.view_recipe_label.setText(recipe.name)
        self.view_author_label.setText("By: {}".format(recipe.author))
        self.view_servings_label.setText("Servings: {}".format(recipe.servings))
        self.view_ingredient_list.clear()
        self.view_instructions.clear()
        
        for ingredient in list(recipe.ingredients.values()):
            self.view_ingredient_list.addItem("{quantity} {unit} of {ingredient}".format(\
                quantity=ingredient.quantity, unit=ingredient.unit, ingredient=ingredient.name))
        count = 1
        for step in recipe.instructions:
            self.view_instructions.addItem("Step {count}: {step}.".format(count=count, step=step))
            count += 1
    
    ## This function is activated when a user selects a recipe from the list
    ## It fills in the recipe information on the right hand side of the panel
    def add_edit_page_recipe_selected(self, item):
        recipe = self.recipe_master[item.text()]
        self.active_recipe = recipe
        self.recipe_name_input.setText(recipe.name)
        self.author_name_input.setText(recipe.author)
        self.servings_input.setText(recipe.servings)
        self.adding_new_ingredient = False

        self.add_edit_page_update_ingredient_list()

        # TODO: add instructions stuff
    
    # Helper function that clears the ingredient table and then re-populates it
    def add_edit_page_update_ingredient_list(self):
        self.ingredient_table.clear()
        for ingredient in list(self.active_recipe.ingredients.values()):
            self.ingredient_table.addItem("{quantity} {unit} of {ingredient}".format(\
                quantity=ingredient.quantity, unit=ingredient.unit, ingredient=ingredient.name))
    
    ## This function is activated when a user selects an ingredient in the ingredient table
    ## The function fills in the appropriate LineEdits with the ingredient's info for the user to edit
    ## or delete
    def ingredient_selected(self):
        try:
            item = self.ingredient_table.selectedItems()[0]
            ingredient_name = self.get_last_word(item.text())
        except:
            return

        self.ingredient_inputs_mode("ON")
        if not ingredient_name == "Ingredient*":
            if self.adding_new_ingredient:
                self.ingredient_table.takeItem(self.ingredient_table.row(self.new_ingredient_holder))
                self.adding_new_ingredient = False
            
            self.active_ingredient = self.active_recipe.ingredients[ingredient_name]
            self.ingredient_name_input.setText(self.active_ingredient.name)
            self.ingredient_quantity_input.setText(self.active_ingredient.quantity)
            self.ingredient_unit_input.setText(self.active_ingredient.unit)
        
    # Helper function that accepts a string and returns the last word in the string
    def get_last_word(self, string):
        return string.split()[-1]

    def ingredient_inputs_mode(self, mode):
        if mode == "ON":
            self.ingredient_name_input.setReadOnly(False)
            self.ingredient_quantity_input.setReadOnly(False)
            self.ingredient_unit_input.setReadOnly(False)
        else:
            self.ingredient_name_input.setReadOnly(True)
            self.ingredient_quantity_input.setReadOnly(True)
            self.ingredient_unit_input.setReadOnly(True)
    
    ## This function is activated when the new Ingredient button is pressed
    ## This function adds "*New Ingredient" to the ingredient list
    def add_ingredient_btn_slot(self):
        if not self.adding_new_ingredient:
            self.new_ingredient_holder = QListWidgetItem("*New Ingredient*")
            self.ingredient_table.addItem(self.new_ingredient_holder)
            self.ingredient_table.setCurrentItem(self.new_ingredient_holder)
            self.adding_new_ingredient = True
            self.clear_ingredient_inputs()
    
    ## This function is activated when the Edit Ingredient Button is pressed
    ## This functions checks the inputs for validity, updates the active recipe's
    ## internal ingredient list and then re-populates the ingredient list
    def edit_ingredient_btn_slot(self):
        name = self.ingredient_name_input.text()
        unit = self.ingredient_unit_input.text()
        quantity = self.ingredient_quantity_input.text()

        # Check inputs are not blank and quantity is numeric
        if len(name) > 0 and len(unit) > 0 and \
            len(quantity) > 0 and quantity.isnumeric():
            if self.adding_new_ingredient: # New ingredient
                self.adding_new_ingredient = False
                self.active_recipe.add_ingredient(name, unit, quantity)
            else: # Existing ingredient
                self.active_ingredient.name = name
                self.active_ingredient.unit = unit
                self.active_ingredient.quantity = quantity
            self.add_edit_page_update_ingredient_list()
            self.active_ingredient = None
            self.clear_ingredient_inputs()
            self.ingredient_inputs_mode("OFF")
        else:
            print("ingredient inputs are invalid")
            return
    
    def clear_ingredient_inputs(self):
        self.ingredient_name_input.setText("")
        self.ingredient_quantity_input.setText("")
        self.ingredient_unit_input.setText("")
    
if __name__ == '__main__':

   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec_()



# Archive
'''
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
    '''        