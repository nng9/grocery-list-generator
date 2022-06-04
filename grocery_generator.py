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
    QAbstractItemView, QTabWidget

from PySide6.QtCore import Qt

class ListItem(QListWidgetItem):
    def __init__(self, text, customData):
        super().__init__(text)
        self.customData = customData

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grocery List App")
        self.setMinimumSize(700, 500)

        self.recipe_master = {}
        self.active_recipe = None
        self.active_ingredient = None

        self.add_data()
        self.build_gui()
        self.connect_signals_to_slots()
    
    def build_gui(self):
        self.actionList = ["Recipes"]
        recipe_page = self.build_recipe_widget()
        shopping_page = QWidget()
        self.page_switcher = QTabWidget()
        self.page_switcher.addTab(recipe_page, "Recipes")
        self.page_switcher.addTab(shopping_page, "Shopping List")
        self.setCentralWidget(self.page_switcher)
        
    
    def build_recipe_widget(self):
        self.recipe_list = QListWidget()
        self.recipe_list.addItems(list(self.recipe_master.keys()))
        self.recipe_name_input = QLineEdit()
        self.author_name_input = QLineEdit()
        self.servings_input = QLineEdit()
        self.ingredient_name_input = QLineEdit()
        self.unit_input = QLineEdit()
        self.quantity_input = QLineEdit()
        self.ingredient_list = QListWidget()
        self.new_ingredient_btn = QPushButton("New Ingredient")
        self.save_ingredient_btn = QPushButton("Save")
        self.delete_ingredient_btn = QPushButton("Delete")
        self.new_recipe_btn = QPushButton("New Recipe")
        self.edit_ingredients_list_btn = QPushButton("Edit")
        self.edit_info_btn = QPushButton("Edit")
        self.recipe_name_lbl = QLabel()
        self.author_lbl = QLabel()
        self.servings_lbl = QLabel()

        left_panel = QVBoxLayout()
        left_panel.addWidget(self.new_recipe_btn)
        left_panel.addWidget(self.recipe_list)
        
        right_panel = QVBoxLayout()

        info_line = QHBoxLayout()
        info_line.addWidget(QLabel("<b>Information</b>"))
        info_line.addWidget(self.edit_info_btn)
        right_panel.addLayout(info_line)
        
        recipe_line = QHBoxLayout()
        recipe_line.addWidget(QLabel("Recipe Name: "))
        recipe_line.addWidget(self.recipe_name_lbl)
        recipe_line.addWidget(self.recipe_name_input)
        self.recipe_name_input.hide()
        right_panel.addLayout(recipe_line)
        
        author_line = QHBoxLayout()
        author_line.addWidget(QLabel("Author Name: "))
        author_line.addWidget(self.author_lbl)
        author_line.addWidget(self.author_name_input)
        self.author_name_input.hide()
        right_panel.addLayout(author_line)

        servings_line = QHBoxLayout()
        servings_line.addWidget(QLabel("Servings:          "))
        servings_line.addWidget(self.servings_lbl)
        servings_line.addWidget(self.servings_input)
        self.servings_input.hide()
        right_panel.addLayout(servings_line)
        
        ingredient_label_line = QHBoxLayout()
        ingredient_label_line.addWidget(QLabel("<b>Ingredients</b>"))
        ingredient_label_line.addWidget(self.edit_ingredients_list_btn)
        right_panel.addLayout(ingredient_label_line)

        right_panel.addWidget(self.ingredient_list)
        self.ingredient_list.setSelectionMode(QAbstractItemView.NoSelection)

        editing_ingredient_layout = QVBoxLayout()
        editing_ingredient_layout.addWidget(self.new_ingredient_btn)

        ingredient_line = QHBoxLayout()
        ingredient_line.addWidget(QLabel("Ingredient Name:"))
        ingredient_line.addWidget(self.ingredient_name_input)
        editing_ingredient_layout.addLayout(ingredient_line)

        units_line = QHBoxLayout()
        units_line.addWidget(QLabel("Measurement Unit:"))
        units_line.addWidget(self.unit_input)
        editing_ingredient_layout.addLayout(units_line)

        quantity_line = QHBoxLayout()
        quantity_line.addWidget(QLabel("Quantity:"))
        quantity_line.addWidget(self.quantity_input)
        editing_ingredient_layout.addLayout(quantity_line)

        edit_delete_ingred_line = QHBoxLayout()
        edit_delete_ingred_line.addWidget(self.save_ingredient_btn)
        edit_delete_ingred_line.addWidget(self.delete_ingredient_btn)
        editing_ingredient_layout.addLayout(edit_delete_ingred_line)

        self.edit_ingred_box = QWidget()
        self.edit_ingred_box.setLayout(editing_ingredient_layout)

        right_panel.addWidget(self.edit_ingred_box)
        self.edit_ingred_box.hide()

        directions_line = QHBoxLayout()
        directions_line.addWidget(QLabel("<b>Directions</b>"))
        self.directions_editor_btn = QPushButton("Edit")
        directions_line.addWidget(self.directions_editor_btn)
        right_panel.addLayout(directions_line)

        self.directions_list = QListWidget()
        self.directions_list.setWordWrap(True)
        right_panel.addWidget(self.directions_list)

        combined_layout = QHBoxLayout()
        combined_layout.addLayout(left_panel, 1)
        combined_layout.addLayout(right_panel, 2)

        widget = QWidget()
        widget.setLayout(combined_layout)
        return widget

    def connect_signals_to_slots(self):
        self.recipe_list.currentItemChanged.connect(self.recipe_selected)
        self.ingredient_list.itemSelectionChanged.connect(self.ingredient_selected)
        self.new_ingredient_btn.pressed.connect(self.add_new_ingredient)
        self.save_ingredient_btn.pressed.connect(self.change_ingredient)
        self.edit_ingredients_list_btn.pressed.connect(self.toggle_ingredient_editor)
        self.edit_info_btn.pressed.connect(self.toggle_information_editor)
        self.delete_ingredient_btn.pressed.connect(self.delete_ingredient)

    ### Slots ###
    
    '''
    Function: Slot for delete ingredient button press signal. Deletes the currently selected ingredient
    Args: None
    Output: Void
    '''
    def delete_ingredient(self):    
        if self.adding_new_ingredient:
            self.ingredient_list.setCurrentRow(100)
            self.remove_new_ingredient()
        else:
            self.active_recipe.ingredients.pop(self.active_ingredient.name)
            self.update_ingredient_list()
        self.ingredient_inputs_mode("OFF")
        self.clear_ingredient_inputs()

    '''
    Function:
    Args:
    Output:
    '''
    def toggle_information_editor(self):
        if self.active_recipe == None:
            return
        if self.edit_info_btn.text()[0] == "E":
            self.edit_info_btn.setText("Save")
            self.recipe_name_lbl.hide()
            self.author_lbl.hide()
            self.servings_lbl.hide()
            self.recipe_name_input.show()
            self.author_name_input.show()
            self.servings_input.show()
        else:
            # Check for validity of inputs
            name = self.recipe_name_input.text()
            author = self.author_name_input.text()
            servings = self.servings_input.text()
            if len(name) > 0 and len(author) > 0 and \
                len(servings) > 0 and servings.isnumeric():
                self.edit_info_btn.setText("Edit")
                self.active_recipe.name = name
                self.active_recipe.author = author
                self.active_recipe.servings = servings
                self.recipe_name_lbl.setText(name)
                self.author_lbl.setText(author)
                self.servings_lbl.setText(servings)
                self.recipe_name_lbl.show()
                self.author_lbl.show()
                self.servings_lbl.show()
                self.recipe_name_input.hide()
                self.author_name_input.hide()
                self.servings_input.hide()
            else:
                print("Check your inputs")
            
    # Shows the ingredient input box, changes button text, and changes selection type #
    def toggle_ingredient_editor(self):
        if self.active_recipe == None:
            return
        if self.edit_ingredients_list_btn.text()[0] == "E":
            self.edit_ingredients_list_btn.setText("Save")
            self.edit_ingred_box.show()
            self.ingredient_list.setSelectionMode(QAbstractItemView.SingleSelection)
            self.ingredient_inputs_mode("OFF")
        else:
            self.edit_ingredients_list_btn.setText("Edit")
            self.edit_ingred_box.hide()
            self.ingredient_list.setCurrentRow(100)
            self.ingredient_list.setSelectionMode(QAbstractItemView.NoSelection)
            self.remove_new_ingredient()    
    
    ## This function is activated when a user selects a recipe from the list
    ## It fills in the recipe information on the right hand side of the panel
    def recipe_selected(self, item):
        recipe = self.recipe_master[item.text()]
        self.active_recipe = recipe
        self.recipe_name_lbl.setText(recipe.name)
        self.author_lbl.setText(recipe.author)
        self.servings_lbl.setText(recipe.servings)
        self.recipe_name_input.setText(recipe.name)
        self.author_name_input.setText(recipe.author)
        self.servings_input.setText(recipe.servings)
        self.adding_new_ingredient = False

        self.update_ingredient_list()

        # TODO: add instructions stuff
        self.update_directions_list()
            
    ## This function is activated when a user selects an ingredient in the ingredient table
    ## The function fills in the appropriate LineEdits with the ingredient's info for the user to edit
    ## or delete
    def ingredient_selected(self):
        try:
            item = self.ingredient_list.selectedItems()[0]
            ingredient_name = self.get_last_word(item.text())
        except:
            return

        self.ingredient_inputs_mode("ON")
        if not ingredient_name == "Ingredient*":
            self.remove_new_ingredient()
            self.active_ingredient = self.active_recipe.ingredients[ingredient_name]
            self.ingredient_name_input.setText(self.active_ingredient.name)
            self.quantity_input.setText(self.active_ingredient.quantity)
            self.unit_input.setText(self.active_ingredient.unit)
    
    ## This function is activated when the new Ingredient button is pressed
    ## This function adds "*New Ingredient" to the ingredient list
    def add_new_ingredient(self):
        if not self.adding_new_ingredient:
            self.new_ingredient_holder = QListWidgetItem("*New Ingredient*")
            self.ingredient_list.addItem(self.new_ingredient_holder)
            self.ingredient_list.setCurrentItem(self.new_ingredient_holder)
            self.adding_new_ingredient = True
            self.clear_ingredient_inputs()
    
    ## This function is activated when the Edit Ingredient Button is pressed
    ## This functions checks the inputs for validity, updates the active recipe's
    ## internal ingredient list and then re-populates the ingredient list
    def change_ingredient(self):
        name = self.ingredient_name_input.text()
        unit = self.unit_input.text()
        quantity = self.quantity_input.text()    
        if len(name) > 0 and len(unit) > 0 and \
            len(quantity) > 0 and quantity.isnumeric():
            if self.adding_new_ingredient: # New ingredient
                self.adding_new_ingredient = False
                self.active_recipe.add_ingredient(name, unit, quantity)
            else: # Existing ingredient
                self.active_ingredient.name = name
                self.active_ingredient.unit = unit
                self.active_ingredient.quantity = quantity
            self.update_ingredient_list()
            self.clear_ingredient_inputs()
            self.ingredient_inputs_mode("OFF")
        else:
            print("ingredient inputs are invalid")
            return
    
    #### Helper Functions ###

    ## Helper that clears the ingredient editor inputs ##
    def clear_ingredient_inputs(self):
        self.ingredient_name_input.setText("")
        self.quantity_input.setText("")
        self.unit_input.setText("")
        self.active_ingredient = None
    
    ## Helper that returns the last word in the string ##
    def get_last_word(self, string):
        return string.split()[-1]
    
    ## Helper that makes ingredient inputs read-only or editable
    def ingredient_inputs_mode(self, mode):
        if mode == "ON":
            self.ingredient_name_input.setReadOnly(False)
            self.quantity_input.setReadOnly(False)
            self.unit_input.setReadOnly(False)
        else:
            self.ingredient_name_input.setReadOnly(True)
            self.quantity_input.setReadOnly(True)
            self.unit_input.setReadOnly(True)
    
    ## Helper that clears  and updates the ingredients table ##
    def update_ingredient_list(self):
        self.ingredient_list.clear()
        for ingredient in list(self.active_recipe.ingredients.values()):
            self.ingredient_list.addItem("{quantity} {unit} of {ingredient}".format(\
                quantity=ingredient.quantity, unit=ingredient.unit, ingredient=ingredient.name))
                
    
    def remove_new_ingredient(self):
        if self.adding_new_ingredient:
                self.ingredient_list.takeItem(self.ingredient_list.row(self.new_ingredient_holder))
                self.adding_new_ingredient = False
    
    def update_directions_list(self):
        count = 1
        for direction in self.active_recipe.instructions:
            string = "<b>Test </b>"
            self.directions_list.addItem(ListItem(string, [direction]))
            count +=1
            #"Step {}: {}".format(count, direction)
        print(self.directions_list.item(0).customData)
        print(self.directions_list.item(1).customData)
    
    ## Helper that adds recipes for testing ##
    def add_data(self):
        test_recipe = Recipe("Ribs and Cauliflower", "2", "Susan Xie")
        test_recipe.add_ingredient("ribs", "lb", "1")
        test_recipe.add_ingredient("cauliflower", "bunch", "1")
        test_recipe.add_instruction("Turn the stove to medium heat and place ribs in. Maybe this will overflow.")
        test_recipe.add_instruction("Sear the meat until all sides are brown")
        self.recipe_master.update({test_recipe.name: test_recipe})
    
    
if __name__ == '__main__':

   app = QApplication(sys.argv)
   window = MainWindow()
   window.show()
   app.exec_()
