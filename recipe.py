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
    
    # Function that adds an ingredient to the recipe or edits an ingredient
    # if it already exists
    def add_ingredient(self, ingredient, unit, quantity):
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