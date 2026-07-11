# Meal Ingredients Database
# Write a program that creates two tables, one for meals and of for ingredients, using these SQL queries:
#   CREATE TABLE IF NOT EXISTS meals (name TEXT) STRICT
#   CREATE TABLE IF NOT EXISTS ingredients (name TEXT, meal_id INTEGER, FOREIGN KEY(meal_id) REFERENCES meals (rowid)) STRICT
# Then, write a program that prompts the user for input. If the user enters 'quit', the program should exit. The user can also enter a new meal
# name, followed by a colon and a comma-delimited list of ingredients: 'meal:ingredeient1,ingredeint2'. Save the meal and its ingredients in the mals and ingredients tables.
# Finally, the user can enter the name of a meal or ingredient. If the name appears in the meals table, the program sould list the meal's ingredients.
# If the name appears in the ingredients table, the program should list every meal that uses this ingredient.

import sqlite3, sys

conn = sqlite3.connect('yummy.db', isolation_level=None)
conn.execute("PRAGMA foreign_keys = ON")
conn.execute('CREATE TABLE IF NOT EXISTS meals (id INTEGER PRIMARY KEY, name TEXT) STRICT')
conn.execute('CREATE TABLE IF NOT EXISTS ingredients (name TEXT, meal_id INTEGER, FOREIGN KEY(meal_id) REFERENCES meals (id)) STRICT')

print("What do you want? If meal's ingeredients, specify name of the meal. If meals that contain a paricular ingredient, specify the ingredient. If you want to exit the program, type \'quit\'")
while True:
    answer = input()
    if not answer:
        continue
    if answer == "quit":
        sys.exit(0);
    if answer == "help":
        print("What do you want? If meal's ingeredients, specify name of the meal. If meals that contain a paricular ingredient, specify the ingredient. If you want to exit the program, type \'quit\'")
        continue
    parts = answer.split(":")
    if len(parts) == 2:
        # Split meal's name and ingredients
        meal_name = parts[0].strip()
        # We add square brackets to Evaluate this expression for every item and collect the results into a list.
        #ingredient_list = [ingredient.stip() for ingredient in parts[1].split(",")] # Removing white spaces

        ingredient_list = []
        for ingredient in parts[1].split(","):
            ingredient_list.append(ingredient.strip())
        
        # Insert meal's name and obtain its rowid
        cursor = conn.execute('INSERT INTO meals (name) VALUES (?)', (meal_name,))
        meal_id = cursor.lastrowid

        for ingredient in ingredient_list:
            conn.execute('INSERT INTO ingredients (name, meal_id) VALUES (?, ?)', (ingredient, meal_id))
        print(f"Meal {parts[0]} added.")

        continue
        
    cursor = conn.execute('SELECT rowid FROM meals WHERE name = ?', (answer,))
    meal_result = cursor.fetchone()
    if meal_result:
        meal_id = meal_result[0]
        cursor = conn.execute('SELECT name FROM ingredients WHERE meal_id = ?', (meal_id,))
        ingredients = cursor.fetchall()
        for ingredient in ingredients:
            print(f"*{ingredient[0]}")
        continue
        
    
    cursor = conn.execute('SELECT meal_id from ingredients WHERE name = ?', (answer,))
    ingredients_name = cursor.fetchall()
    if ingredients_name:
        for meals_id in ingredients_name:
            cursor = conn.execute('SELECT name FROM meals WHERE rowid = ?', (meals_id[0],))
            meal = cursor.fetchone()
            print(f"#{meal[0]}")

    else:
        print("No such meal or ingredredient in the database, try something else")



