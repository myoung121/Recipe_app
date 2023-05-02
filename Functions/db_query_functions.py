import random as ran
import sqlite3
from PIL import Image, ImageTk
import  io
""" FUNCTIONS THAT RETURN A SINGLE FORMATTED RECIPE"""


def getRecipeInfo(recipe_id: int, db_connection_str:str) -> (dict, bytes):  # show recipe button
    table_names: tuple = ('Recipe', 'RecipeIngredient', 'Image')
    recipe_info = {}
    unique_ingreds = getRowsAll('Ingredient',db_connection_str)
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
                recipe_info['favorite'] = stats[8]
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


def getRecipeInfoRandom(db_connection_str:str) -> (dict, bytes):  # random recipe button
    # todo - chech todo.txt
    # get all recipe_ids in table
    execute_script = 'SELECT recipe_id FROM Recipe'
    db_connection = sqlite3.connect(db_connection_str)
    with db_connection:
        all_ids = db_connection.execute(execute_script)
    all_ids = all_ids.fetchall()
    # pick a random recipe_id and get the id number alone
    ran_recipe_num = ran.sample(all_ids,1)[0][0]
    # pass recipe_id into function to get recipe info
    return getRecipeInfo(recipe_id=ran_recipe_num, db_connection_str=db_connection_str)


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
    """ return all rows in table """
    execute_script = f'SELECT * FROM ' + str(table_name)
    db_connection_str = sqlite3.connect(db_connection_str)
    with db_connection_str:
        all_rows = db_connection_str.execute(execute_script)
    return all_rows.fetchall()

def getImageRandom(db_connection_str:str,num_of_images:int=1)->list:
    """ return one or multiple random image and image name"""
    # get all image_ids
    execute_script = 'SELECT image_id from Image'
    db_connection = sqlite3.connect(db_connection_str)
    with db_connection:
        image_ids = db_connection.execute(execute_script)
    image_ids=image_ids.fetchall()
    # get the number of random image_ids requested
    ran_image_ids = ran.sample(image_ids,num_of_images)
    # make new script to get images based on the selected image_ids
    execute_script = 'SELECT image_name,image_blob FROM Image WHERE image_id IN '
    # add placeholder for each image_id
    placeholders_str = "(" + '?,' * num_of_images
    placeholders_str = placeholders_str[:-1] + ")"
    # put the script together
    execute_script += placeholders_str
    #db_connection_str = sqlite3.connect(db_connection_str)
    with db_connection:
        random_images = db_connection.execute(execute_script,tuple(x[0] for x in ran_image_ids))
    random_images = random_images.fetchall()
    #random_images = ran.sample(all_images,num_of_images)
    # convert binary images to images tkinter can use
    random_jpeg_images =[]
    for image_pair in random_images:
        sub_list = [image_pair[0]]
        # convert image bytes to PIL image format(jpeg)
        pic = Image.open(io.BytesIO(image_pair[1]))
        sub_list.append(ImageTk.PhotoImage(pic))
        random_jpeg_images.append(tuple(sub_list))
    return random_jpeg_images
    # todo - check if this runs correctly

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

