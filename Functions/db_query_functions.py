import random as ran
import sqlite3
""" FUNCTIONS THAT RETURN A SINGLE FORMATED RECIPE"""


def getRecipeInfo(recipe_id: int, db_connection_str:str, unique_ingreds: list) -> (dict, bytes):  # show recipe button
    table_names: tuple = ('Recipe', 'RecipeIngredient', 'Image')
    recipe_info = {}
    db_connection_str = sqlite3.connect(db_connection_str)
    for item_rows in table_names:
        try:

            execute_script_str = f'SELECT * ' \
                                 f'FROM  {item_rows} ' \
                                 f'WHERE recipe_id = {recipe_id}'
            if item_rows == 'Recipe':
                with db_connection_str:
                    stats = db_connection_str.execute(execute_script_str)
                    stats = stats.fetchall()[0]
                recipe_info['recipe_id'] = stats[0]
                recipe_info['name'] = stats[1].replace('_', ' ').title()
                recipe_info['instr'] = stats[2]
                recipe_info['prep_time'] = stats[3]
                recipe_info['cook_time'] = stats[4]
                recipe_info['comment'] = stats[5]
                recipe_info['created_time'] = stats[6]
                recipe_info['updated_time'] = stats[7]
            elif item_rows == 'RecipeIngredient':
                recipe_info['ingredients'] = []
                with db_connection_str:
                    stats = db_connection_str.execute(execute_script_str)
                    stats = stats.fetchall()
                for num, food in enumerate(stats):
                    recipe_info['ingredients'].append(unique_ingreds[int(food[1])][1])
            elif item_rows == 'Image':
                with db_connection_str:
                    stats = db_connection_str.execute(execute_script_str)
                    stats = stats.fetchall()[0]
                recipe_info['image_name'] = stats[2].replace('_', " ").title()
                image_blob = stats[3]
        except Exception as e:
            print(f'Error in getRecipeInfo():\n{e}')
    return recipe_info, image_blob


def getRecipeInfoRandom(num_recipes: int, db_connection_str:str, unique_ingreds: list) -> (dict, bytes):  # random recipe button
    ran_recipe_num = ran.randint(0, int(num_recipes))
    return getRecipeInfo(recipe_id=ran_recipe_num, db_connection_str=db_connection_str, unique_ingreds=unique_ingreds)


# -------------------------------------------------------------------------------
"""FUNCTIONS THAT RETURN RECIPE INFO"""


def getRowsFiltered(search_txt, db_connection_str:str, user_filter: str= 'name',return_all:bool=False):  # search box / toggle buttons
    """can search by name, recipe_id, ingredient, instruction"""
    column_names = ('Recipe.recipe_id', 'recipe_name', 'prep_time', 'cook_time')
    allowed_filters = ('name', 'recipe_id', 'ingredient', 'instruction')
    if user_filter in allowed_filters:
        db_connection_str = sqlite3.connect(db_connection_str)
        execute_script = f'SELECT DISTINCT {",".join(column_names).rstrip(",")} ' \
                         f'FROM Recipe '
        if user_filter == allowed_filters[0]:  # name
            if return_all:
                pass
            else:
                search_txt = search_txt.replace(' ', '_')
                execute_script += 'WHERE recipe_name ' \
                                  'LIKE '
                placeholder = f'\'%{search_txt.lower()}%\''
                execute_script += placeholder
        elif user_filter == allowed_filters[1]:  # recipe_id
            execute_script += 'WHERE recipe_id ' \
                              'LIKE '
            placeholder = f'\'%{search_txt}%\''
            execute_script += placeholder
        elif user_filter == allowed_filters[2]:  # ingredients
            execute_script += 'JOIN RecipeIngredient ON Recipe.recipe_id=RecipeIngredient.recipe_id ' \
                              'JOIN Ingredient ON RecipeIngredient.ingred_id=Ingredient.ingred_id ' \
                              'WHERE ingred_name ' \
                              'LIKE '
            placeholder = f'\'%{search_txt}%\''
            execute_script += placeholder
        elif user_filter == allowed_filters[3]:  # instructions
            execute_script += 'WHERE instr ' \
                              'LIKE '
            placeholder = f'\'%{search_txt}%\''
            execute_script += placeholder
    else:
        exit(f'{user_filter} Filter not Allowed')
    with db_connection_str:
        values = db_connection_str.execute(execute_script)
        values = values.fetchall()
    return values


def getRowsAll(table_name: str, db_connection_str:str) -> list:
    """ return all rows in database """
    execute_script = f'SELECT * FROM ' + str(table_name)
    db_connection_str = sqlite3.connect(db_connection_str)
    with db_connection_str:
        all_rows = db_connection_str.execute(execute_script)
    return all_rows.fetchall()


# --------------------------------------------------------------
"""FUNCTIONS THAT ALTER DB INFO"""


def addRecipe(recipe_name:str,db_connection, instructions:str,
              unique_ingreds:tuple,
              cook_time_minutes:int=0,comment:str=''):
    def addIngredients(recipe_id: int, ingredients: tuple) -> None:

        pass
    # todo - should auto update the created_at and updated_at columns
    # todo - include addIngredients()
    recipe_id = len(getRowsAll('Recipe',db_connection)) # this wont work when start deleting rows, should use the max recipe_id number + 1instead
    table_columns_str = 'Recipe(recipe_id, recipe_name, instr, cook_time, comment) VALUES'
    row_values = (recipe_id,recipe_name,instructions,cook_time_minutes,comment)
    placeholders_str = "(" + '?,' * len(row_values)
    placeholders_str = placeholders_str[:-1] + ")"
    execute_script_str = "INSERT INTO " + str(table_columns_str + placeholders_str)
    with db_connection:
        db_connection.execute(execute_script_str,row_values)
    print('recipe added')

def deleteRecipe(recipe_id:int,db_connection_str:str):
    """delete recipe record from database"""
    db_connection_str = sqlite3.connect(db_connection_str)
    delete_tables = ('Recipe','RecipeIngredient','Image')
    for table in delete_tables:
        execute_script = f'DELETE FROM {str(table)} WHERE recipe_id={recipe_id}'
        with db_connection_str:
            db_connection_str.execute(execute_script)
    print('Recipe Deleted')
def addComment(recipe_id:int,db_connection,comment:str)->None:
    # todo- should auto update the updated_at column
    execute_script = 'UPDATE Recipe ' \
                     'SET comment=? ' \
                     'WHERE recipe_id=?'
    with db_connection:
        db_connection.execute(execute_script,(str(comment),recipe_id))
    print('row updated')

def removeComment(recipe_id:int,db_connection)->None:
    # todo- should auto update the updated_at column
    return addComment(recipe_id=recipe_id,db_connection=db_connection,comment='')

