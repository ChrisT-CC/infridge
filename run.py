"""
This app connects to a Google Sheet file with two worksheets.
The worksheets store favorite recipes and infridge ingredients.
The app generates a recipe based on infridge ingredients or a shopping list
if no recipe is available.
"""

# Code copied and adapted from "CI Love sandwiches" project
# Lines 13, 16, 20-24 and 29-32

# Import the entire "gspread" library
# So I can access any function, class or method within it
import gspread
# Import the "Credentials" class which is part of the "service_account"
# function from the "google.oauth2" library
from google.oauth2.service_account import Credentials

# Set the scope
# The scope lists the API's that the program should acces in order to run
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Create another constant variable named "CREDS"
# Call the "from_service_account_file" method of the "Credentials" class
# and pass it "creds.json"
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("infridge")

recipes = SHEET.worksheet("recipes")

data = recipes.get_all_values()

ingredients_worksheet = SHEET.worksheet("ingredients")  # Ingredients worksheet
ingredients = ingredients_worksheet.col_values(1)  # List of ingredients
ingredients_quantity = ingredients_worksheet.col_values(2)


def get_basic_ingredient():
    '''
    Welcomes user
    Explains what the app is for
    Asks for user input - basic ingredient - (chicken, potato, pie, broccoli)
    '''
    print("You have to choose a basic ingredient")
    print("Example: chicken, potatoes, eggs, broccoli\n")

    while check_fridge():
        basic_ingredient = input("Please choose a basic ingredient: ").lower()
        if basic_ingredient.isdigit():
            print("The basic ingredient can't be a number. Try again\n")
        elif basic_ingredient == "":
            print("The basic ingredient can't empty. Try again\n")
        else:
            if validate_basic_ingredient(basic_ingredient):
                break

    return basic_ingredient


def validate_basic_ingredient(value):
    '''
    Checks if basic ingredient is in list of ingredients
    '''
    if value in ingredients:
        print(f"'{value}' is in the list of ingredients"+"\n")
    else:
        print(f"'{value}' is not in the list of ingredients"+"\n")
        return False

    return True


def check_fridge():
    """Checks if the fridge is empty"""
    if not ingredients_quantity:
        print("Fridge is empty. Time to fill it!!")
    else:
        return True


def generate_available_recipes_list(value):
    '''Generate a list of recipes that contains the chosen basic ingredient'''
    print(f"Generating the list of recipes based on {value} ..."+"\n")
    all_recipes = recipes.col_values(1)
    print(f"Your recipes with {value} are:")
    ingredient_recipes = [
        recipes.cell(num, 1).value
        for num in range(1, len(all_recipes)+1)
        if value in recipes.row_values(num)
        ]

    return ingredient_recipes


def print_available_recipes(value):
    """Prints a list of available recipes"""
    num = len(value)
    recipes_dict = {}
    for ind in range(num):
        print(f"{ind+1} {value[ind]}")
        recipes_dict.update({ind+1: value[ind]})

    return recipes_dict


def choose_recipe(value):
    '''Asks the user to choose a recipe'''
    while True:
        recipe_num = input("\nChoose a recipe by number: ")
        if validate_choice(recipe_num, len(value)):
            break
    result = value[int(recipe_num)]
    print(result)
    return result


def validate_choice(choice_num, max_num):
    """
    Inside try, converts the string choice_num value to integer.
    Raises ValueError if the choice_num cannot be converted into int,
    or if the choice_num value is bigger the max number of choices.
    """
    try:
        int(choice_num)
        if int(choice_num) > max_num:
            raise ValueError(f"Choose a number lower then {max_num+1}")
    except ValueError as error:
        print(f"Invalid data: {error}, please try again.\n")
        return False

    return True


def get_ingredients(rec_r):
    """Get ingredients for chosen recipe"""
    ing_list = rec_r[1:-1]

    return ing_list


def ingredients_infridge(ing_list):
    """Check ingredients for chosen recipe exist"""
    print("Checking ingredients...\n")
    missing_ingredients = []
    for ing in ing_list:
        ing_cell_num = ingredients_worksheet.find(ing).row
        ing_quant = ingredients_quantity[ing_cell_num-1]
        if ing_quant == "0":
            missing_ingredients.append(ing)
        else:
            continue
    if missing_ingredients == []:
        print("All ingredients available\n")
        print("Printing recipe...\n")
        print_recipe()
        remove_ingredients(ing_list)
    else:
        print("Recipe not available\n")
        print("You can:\n")
        print("1 Print a shopping list with the missing ingredients")
        print("2 Add ingredients")
        while True:
            option_num = input(
                "\nPlease choose one of the above options by number: ")
            if validate_choice(option_num, 2):
                break
        result = int(option_num)
        if result == 1:
            print_shopping_list(missing_ingredients)
        elif result == 2:
            print("\nAdd ingredients")
            while True:
                add_ingredients()
                while True:
                    option = input("Add more? (1 = yes, 2 = no) ")
                    if validate_choice(option, 2):
                        break
                rez = int(option)
                if rez == 2:
                    print("\nGood bye!\n")
                    break


def get_recipe_row(rec_choice):
    """Find the recipe row in recipes worksheet"""
    recipe_cell_num = recipes.find(rec_choice).row
    rec_row = recipes.row_values(recipe_cell_num)

    return rec_row


def print_recipe():
    """Prints chosen recipe"""
    print(recipe_row[0]+"\n")
    print("Ingredients:\n")
    for ing in recipe_row[1:-1]:
        print(ing)
    print("\nCoocking method:\n")
    print(recipe_row[-1]+"\n")


def remove_ingredients(ing):
    """Remove ingredients"""
    print("Removing used ingredients...\n")
    for i in ing:
        ing_cell_num = ingredients_worksheet.find(i).row
        ing_quant = ingredients_quantity[ing_cell_num-1]
        update = int(ing_quant)-1
        ingredients_worksheet.update_cell(ing_cell_num, 2, update)
    print("Ingredients removed successfully\n")
    print("Good bye!\n")


def print_shopping_list(value):
    """Printing a shopping list with missing ingredients"""
    print("\nShopping list\n")
    for val in value:
        print(val)


def add_ingredients():
    """Adding ingredients to ingredients worksheet"""
    ingredient = input("\nIngredient name: ")
    ing_val = input("Ingredient quantity: ")
    if ingredient in ingredients:
        ing_cell_num = ingredients_worksheet.find(ingredient).row
        ing_quant = ingredients_quantity[ing_cell_num-1]
        update = int(ing_quant) + int(ing_val)
        ingredients_worksheet.update_cell(ing_cell_num, 2, update)
    else:
        ingredients_worksheet.append_row([ingredient, int(ing_val)])
    print("\nIngredient added\n")


def main():
    '''Runs all the function'''
    check_fridge()
    basic_ing = get_basic_ingredient()
    available_recipes = generate_available_recipes_list(basic_ing)
    dict_available_recipes = print_available_recipes(available_recipes)
    recipe_choice = choose_recipe(dict_available_recipes)
    global recipe_row
    recipe_row = get_recipe_row(recipe_choice)
    ingredients_list = get_ingredients(recipe_row)
    ingredients_infridge(ingredients_list)


print("\nWelcome to inFridge")
print("This app helps you choose a meal based on infridge ingredients\n")
main()
