import pandas as pd
import urllib.parse

class NutritionFacts:
    def __init__(self, csv_path='data/ingredients_with_nutrition.csv'):
        self.df = pd.read_csv(csv_path, index_col=0)

    def is_known(self, ingredient):
        return ingredient.strip().lower() in self.df.index

    def get_report(self, ingredients):
        report = "I. NUTRITION FACTS\n"
        for ing in ingredients:
            name = ing.strip().lower()
            report += f"{ing.strip().capitalize()}\n"

            if name in self.df.index:
                row = self.df.loc[name]
                for col, val in row.items():
                    nutrient_name = col.replace('_dv', '').replace('_', ' ').capitalize()
                    report += f"{nutrient_name} - {int(round(val))}% of Daily Value\n"
            else:
                report += "No nutrition data available.\n"
            report += "\n"
        return report


class RecipeFinder:
    def __init__(self, search_csv='data/searchable_recipes.csv'):
        self.df = pd.read_csv(search_csv)

    def find_top_3(self, user_ingredients, all_known=True):
        if not all_known:
            return ""
        user_ings = [i.strip().lower() for i in user_ingredients]

        def calculate_score(row):
            score = 0
            ing_text = str(row['ingredients_text']).lower()
            for ing in user_ings:
                if ing in ing_text:
                    score += 1
            return score

        temp_df = self.df.copy()
        temp_df['match_score'] = temp_df.apply(calculate_score, axis=1)
        top_3 = temp_df.sort_values(by=['match_score', 'rating'], ascending=False).head(3)
        top_3 = top_3[top_3['match_score'] > 0]

        res = "II. TOP-3 SIMILAR RECIPES:\n"
        if top_3.empty:
            res += "No similar recipes found for these ingredients.\n"
        else:
            for _, row in top_3.iterrows():
                res += f"- {row['title'].strip()}, rating: {row['rating']:.1f}, URL: {row['url']}\n"

        search_query = ", ".join(user_ingredients)
        encoded_query = urllib.parse.quote_plus(search_query)
        common_url = f"https://www.epicurious.com/search?q={encoded_query}"

        res += f"\nFind other similar dishes here:\n{common_url}\n"
        return res