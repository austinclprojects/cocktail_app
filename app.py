import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config["DEBUG"] = True

def row_to_dict(row):
    return row.to_dict()

recipes = pd.read_json('recipes.json')
recipes['dict'] = recipes.apply(row_to_dict,axis=1)
   
@app.route('/', methods=['GET'])
def home():
    return f"""<h1>Cocktail API</h1>
    <p>This API gives cocktail recipes courtesy of Liquor.com.</p>
    <p> /recipes Gets all recipes with a given ingredient or title. If no ingredient or title given returns all recipes.</p>
    <p> ex. /recipes?ingredient=whiskey  /recipes?ingredient=whiskey&title=hot  </p>
    <p></p>
    <p>/search Searches all recipes for several ingredients and returns recipes using all given ingredients.
    <p> ex. /search?ingredient=whiskey+cherry+grenadine</p>
    """

@app.route('/recipes', methods=['GET'])
#Gets all recipes with a given ingredient. If no ingredient given returns all recipes.
def get_recipes():
    _recipes = recipes
    _recipes['ingredients'] = _recipes['ingredients'].astype(str).apply(lambda x: x.lower())
    _recipes['title'] = _recipes['title'].astype(str).apply(lambda x: x.lower())
    params = request.args
    ingredient = params.get('ingredient')
    title = params.get('title')
    if ingredient:
        _recipes = _recipes[_recipes['ingredients'].str.contains(r'\b{ingredient}\b'.format(ingredient=ingredient))].reset_index(drop=True)
    if title:
        _recipes = _recipes[_recipes['title'].str.contains(r'\b{title}\b'.format(title=title))].reset_index(drop=True)
        

    return jsonify(_recipes['dict'].to_dict())

@app.route('/search', methods=['GET'])
#Searches all recipes for several ingredients and returns recipes using all given ingredients
def search_recipes():
    _recipes = recipes
    _recipes['ingredients'] = _recipes['ingredients'].astype(str).apply(lambda x: x.lower())
    params = request.args
    ingredients = params.get('ingredients')
    if ingredients:
        ing_list = ingredients.split(' ')
        for ingredient in ing_list:
            _recipes = _recipes[_recipes['ingredients'].str.contains(r'\b{ingredient}\b'.format(ingredient=ingredient))].reset_index(drop=True)
    return jsonify(_recipes['dict'].to_dict())





if __name__ == "__main__":
    app.run()