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

# print(data)
# print(ingredients_list)


def get_basic_ingredient():
    '''
    Welcomes user
    Explains what the app is for
    Asks for user input - basic ingredient - (chicken, potato, pie, brocoli)

    '''
    print("\nWelcome to inFridge\n")
    print("This app helps you choose a meal based on infridge ingredients")

    print("You have to choose a basic ingredient")
    print("Example: chicken, potatos, pie, brocoli\n")

    while True:
        basic_ingredient = input("Please choose a basic ingredient: ")

        # print(f"The basic ingredient you chose is: {basic_ingredient}")
        if basic_ingredient.isalpha():
            print(f"{basic_ingredient} is all letters"+"\n")
            print(f"Check if {basic_ingredient} is in list of ingredients")
            if validate_basic_ingredient(basic_ingredient):
                print(f"{basic_ingredient} is valid")
                break
        else:
            print("The basic ingredient must be all letters\n")
    return basic_ingredient


def validate_basic_ingredient(value):
    if value in ingredients_list:
        print(f"{value} is in the list of ingredients"+"\n")
    else:
        print(f"{value} is not in the list of ingredients"+"\n")
        return False
    return True


get_basic_ingredient()
