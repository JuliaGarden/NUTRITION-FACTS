#!/usr/bin/env python3
import sys
from recipes import NutritionFacts, RecipeFinder

def main():
    if len(sys.argv) < 2:
        print("Usage: ./nutritionist.py ingredient1, ingredient2, ...")
        return
    input_str = " ".join(sys.argv[1:])
    user_ingredients = [i.strip() for i in input_str.split(',') if i.strip()]
    user_ingredients = list(dict.fromkeys(user_ingredients))

    try:
        #Раздел I
        nf = NutritionFacts()
        nutrition_report = nf.get_report(user_ingredients)
        print(nutrition_report)
        #Раздел II
        rf = RecipeFinder()
        all_ingredients_known = all(nf.is_known(i) for i in user_ingredients)
        similar_recipes = rf.find_top_3(user_ingredients, all_known=all_ingredients_known)
        if similar_recipes:
            print(similar_recipes)

    except FileNotFoundError as e:
        print(f"Error: file not found. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()