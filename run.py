"""
This app connects to a Google Sheet file with two worksheets.
The worksheets store favorite recipes and infridge ingredients.
The app generates a recipe based on infridge ingredients or a shopping list
if no recipe is available.
"""

# Write your code to expect a terminal of 80 characters wide and 24 rows high

# Code copied and adapted from "CI Love sandwiches" project

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
ingredients_list = ingredients_worksheet.col_values(1)  # List of ingredients
ingredients_cuantity = ingredients_worksheet.col_values(2)

# print(data)
# print(ingredients_list)


def get_basic_ingredient():
    '''
    Welcomes user
    Explains what the app is for
    Asks for user input - basic ingredient - (chicken, potato, pie, broccoli)
    '''
    print("You have to choose a basic ingredient")
    print("Example: chicken, potatos, pie, broccoli\n")

    while True:
        basic_ingredient = input("Please choose a basic ingredient: ")
        # print(f"The basic ingredient you chose is: {basic_ingredient}")
        if basic_ingredient.isdigit():
            print("The basic ingredient can't be a number. Try again\n")
        elif basic_ingredient == "":
            print("The basic ingredient can't empty. Try again\n")
        else:
            # print(f"{basic_ingredient} is a string"+"\n")
            if validate_basic_ingredient(basic_ingredient):
                # print(f"'{basic_ingredient}' is valid")
                break
    return basic_ingredient


def validate_basic_ingredient(value):
    '''
    Checks if basic ingredient is in list of ingredients
    '''
    if value in ingredients_list:
        print(f"'{value}' is in the list of ingredients"+"\n")
    else:
        print(f"'{value}' is not in the list of ingredients"+"\n")
        return False
    return True


def check_fridge():
    """Checks if the fridge is empty"""
    if not ingredients_cuantity:
        print("Fridge is empty. Time to fill it!!")
    else:
        print(ingredients_cuantity)


def generate_available_recipes_list(value):
    '''Generate a list of recipes that contains the chosen basic ingredient'''
    print(f"Generating the list of recipes based on {value} ..."+"\n")
    all_recipes = recipes.col_values(1)
    # print(all_recipes)
    print(f"Your recipes with {value} are:")
    ingredient_recipes = [
        recipes.cell(num, 1).value
        for num in range(1, len(all_recipes)+1)
        if value in recipes.row_values(num)
        ]
    # print(ingredient_recipes)

    return ingredient_recipes


def print_available_recipes(value):
    """Prints a list of available recipes"""
    num = len(value)
    recipes_dict = {}
    for ind in range(num):
        print(f"{ind+1} {value[ind]}")
        recipes_dict.update({ind+1: value[ind]})
        # print(recipes_dict)
    print(recipes_dict)
    return recipes_dict


def choose_recipe(value):
    '''Asks the user to choose a recipe'''
    recipe_num = input("\nChoose a recipe by number: ")
    result = value[int(recipe_num)]
    print(result)
    return result


print("\nWelcome to inFridge")
print("This app helps you choose a meal based on infridge ingredients\n")

check_fridge()
basic_ing = get_basic_ingredient()
available_recipes = generate_available_recipes_list(basic_ing)
dict_available_recipes = print_available_recipes(available_recipes)
choose_recipe(dict_available_recipes)
