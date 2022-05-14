
## Have a list of recipes

## You can add recipes

## You can edit recipes

## Needs to have a section where you add recipes to a list

## Send you an email with your shopping list and meal plan

## Import Recipes using JSON or CSV

## Export Recipes using JSON or CSV

## Ingredients need name, unit, and quantity    
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def window():
   app = QApplication(sys.argv) # What is the purpose of this line?
   w = QWidget()
   b = QLabel(w)
   c = QLineEdit(w)
   b.setText("Hello World!")
   w.setGeometry(100,100,200,50)
   b.move(50,20)
   c.move(100, 0)
   w.setWindowTitle("Grocery List Generator")
   w.show()
   sys.exit(app.exec_())

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

chicken_rice = Recipe("Chicken and Rice", ["1 lb Chicken", "1 cup Rice"])

if __name__ == '__main__':
   window()


