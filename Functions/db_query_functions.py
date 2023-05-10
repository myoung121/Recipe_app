import pprint
import random as ran
import sqlite3
from PIL import Image, ImageTk
import  io




"""FUNCTIONS THAT RETURN RECIPE RECORD INFO"""


def getFilteredRecipes(search_txt, db_connection_str:str, user_filter: str= 'name', return_all:bool=False):  # search box / toggle buttons
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

def getImageRandom(db_connection_str:str,num_of_images:int=1,screen_sized=False,screen_w_h:tuple=(600,500))->list:
    """ return one or multiple random image names with images in jpeg format"""
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
    print('Images: ',end='')
    for j in random_jpeg_images:
        print(j[0],end='/ ')
    print()
    return random_jpeg_images

# --------------------------------------------------------------

""" FUNCTIONS THAT RETURN A SINGLE FORMATTED RECIPE RECORD / INFO"""
def getRecipeInfo(recipe_id: int, db_connection_str:str) -> (dict, bytes):  # show recipe button
    table_names: tuple = ('Recipe', 'RecipeIngredient', 'Image') # IMAGE MUST BE LAST!!!
    recipe_info = {}
    unique_ingreds = getRowsAll('Ingredient',db_connection_str)
    db_connection = sqlite3.connect(db_connection_str)
    for item_rows in table_names:
        try:

            execute_script_str = f'SELECT * ' \
                                 f'FROM  {item_rows} ' \
                                 f'WHERE recipe_id = {recipe_id}'
            if item_rows == 'Recipe':
                with db_connection:
                    stats = db_connection.execute(execute_script_str)
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
                with db_connection:
                    stats = db_connection.execute(execute_script_str)
                    stats = stats.fetchall()
                for num, food in enumerate(stats):
                    recipe_info['ingredients'].append(unique_ingreds[int(food[1])][1])
            elif item_rows == 'Image':
                with db_connection:
                    stats = db_connection.execute(execute_script_str)
                    stats = stats.fetchall()[0]
                recipe_info['image_name'] = stats[2].replace('_', " ").title()
                image_blob = stats[3]
        except Exception as e:
            if 'list index' in str(e): # ignore index error here. It throws if no image and is handled at end of iteration
                pass
            else:
                print(f'Error in getRecipeInfo():\n{e}')
    try:
        return recipe_info, image_blob
    except UnboundLocalError: # catch if recipe doesnt have an image
        # GET a random image
        ran_image = getImageRandom(db_connection_str)[0]
        recipe_info['image_name'] = ran_image[0].replace('_', " ").title() # add image name to info
        image_blob = ran_image[1]# save image
        return recipe_info,image_blob# return recipe info and dict


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

"""FUNCTIONS THAT ALTER TABLE"""

def addRecipe(db_connection,recipe_name:str,instructions,
              ingredients,cook_time_minutes=0,comment:str='',favorite=True):

    pre_load_checks ={'id_ok':False,'name_ok':False,
                      'ingred_ok' : False,'instrs_ok' : False,
                      'cktime_ok' : False,'comment_ok': False
                      }


    # CUSTOM EXCEPTIONS
    input_error_str = 'RECIPE INPUT ERROR: '
    data_error_str = 'RECIPE DATA ERROR: '

    class EntryError(Exception):
        """INPUT ERRORS EXCEPTION WRAPPER"""
        pass
    class DataError(Exception):
        """DATA LOAD,PREP, SEARCH, OTHER DATA ERRORS EXCEPTION WRAPPER"""
        pass

    #########################################################
    # FUNCTIONS THAT ADD TO TABLES
    def addIngredient(db_connection1,ingred_id_ingred_pair:tuple|str):
        #print('\tadding NEW ingred to Ingredient table...')
        execute_script = 'INSERT INTO Ingredient (ingred_id,ingred_name) VALUES (?,?)'
        db_connection1 = sqlite3.connect(db_connection1)
        with db_connection1:
            db_connection1.execute(execute_script,(*ingred_id_ingred_pair,))
            print(f'\t+ ingredient added +')

    def addRecipeIngredient(db_connection1,recipe_ingred_ids_pair:tuple|str):
        """add recipe_id and ingred_id to database"""
        #print('\tadding NEW recipe,ingred to RecipeIngredient table...')
        execute_script = 'INSERT INTO RecipeIngredient (recipe_id,ingred_id) VALUES (?,?)'
        db_connection1 = sqlite3.connect(db_connection1)
        with db_connection1:
            db_connection1.execute(execute_script,(*recipe_ingred_ids_pair,))
            print(f'\t+ recipe ingredient added +')

    def addRecipeInfo(db_connection1,record_values:tuple|str):
        """add values to columns recipe_id, recipe_name, instr, cook_time, comment, favorite to recipe table"""
        #print('\tadding NEW recipe to Recipe table...')
        execute_script = 'INSERT INTO Recipe(recipe_id, recipe_name, instr, cook_time, comment, favorite) VALUES'
        placeholders_str = "(" + '?,' * len(record_values)
        placeholders_str = placeholders_str[:-1] + ")"
        execute_script += placeholders_str
        db_connection1 = sqlite3.connect(db_connection1)
        with db_connection1:
            db_connection1.execute(execute_script, (*record_values,))
            print(f'\t+ recipe info added +')
    #########################################################
    #----------------------------------------------------------------------------------------
    # VALIDATE INPUTS

    print('CHECKING RECIPE INFO...')
    # CHECK RECIPE ID
    recipe_id = getMaxIdNum(db_connection,'recipe_id','Recipe') + 1 # set the recipe_id to the largest recipe_id in table + 1
    try:
        assert isinstance(recipe_id,int)
        pre_load_checks['id_ok'] = True
        print(f'\trecipe id-{recipe_id}-ok')
    except AssertionError:
        raise EntryError(input_error_str + 'RECIPE ID SHOULD BE AN INTEGER')

    # CHECK RECIPE NAME
    if recipe_name:
        try:
            assert isinstance(recipe_name,str)
            recipe_name = recipe_name.lower()
        except AssertionError:
            raise EntryError(input_error_str + 'RECIPE NAME SHOULD BE A STRING')
        try:
            assert validRecipeName(db_connection,recipe_name) == True
            pre_load_checks['name_ok'] = True
            print(f'\trecipe name-{recipe_name[:10]}-ok')
        except AssertionError:
            raise EntryError(input_error_str + 'RECIPE NAME ALREADY IN USE')
    else: # recipe name is blank
        raise EntryError(input_error_str + 'RECIPE NAME IS BLANK')

    # CHECK COOKTIME
    if not cook_time_minutes:
        cook_time_minutes = 0
    try:
        cook_time_minutes = int(cook_time_minutes)
        assert cook_time_minutes >=0
        pre_load_checks['cktime_ok'] = True
        print(f'\tcook time-{cook_time_minutes}-ok')
    except ValueError:
        raise EntryError(input_error_str + 'COOK TIME SHOULD BE AN INTEGER')
    except AssertionError:
        raise EntryError(input_error_str + 'COOK TIME SHOULD BE GREATER THAN 0 MINUTES')

    # CHECK COMMENT
    if comment: # if user entered a comment
        try:
            assert isinstance(comment, str) # check if in correct data type
            pre_load_checks['comment_ok'] = True
            print(f'\tcomment-{comment[:10]}-ok')
        except AssertionError:
            raise EntryError(input_error_str + 'COMMENT SHOULD BE A STRING')

    # CHECK INSTRUCTIONS
    try:
        assert isinstance(instructions,str)
        pre_load_checks['instrs_ok'] = True
        print(f'\tinstrs-{instructions[:10]}...-ok')
    except AssertionError:
        raise EntryError(input_error_str + 'INSTRUCTIONS SHOULD BE A STRING')

    # CHECK INGREDIENTS
    try:
        assert isinstance(ingredients,tuple) # make sure ingedients are in tuple
    except AssertionError:
        raise EntryError(input_error_str + 'INGREDIENTS SHOULD BE IN A TUPLE')
    ingredients_ids = [] # store the ingred_id nums to add to database later
    highest_ingred_id = int(getMaxIdNum(db_connection,'ingred_id','Ingredient'))# get the ingred_id ( same way as got recipe_id)
    ingreds_made= 0 # track how many new ingreds made
    for num,food in enumerate(ingredients): # check each item in the sequence
        food_unique = isUniqueIngred(db_connection,food)
        if food_unique[0]: # if ingredient not in database
            ingreds_made += 1
            ingred_id  =  highest_ingred_id + ingreds_made # get the primary key (id_num) for new imgred
            ingredients_ids.append(ingred_id)
        else:
            ingredients_ids.append(food_unique[1])  # add id num to list
    try:
        ingreds_loadable = tuple(zip(ingredients_ids,ingredients))
        assert len(ingredients_ids) == len(ingreds_loadable)
        pre_load_checks['ingreds_ok'] = True
        print(f'\tingreds--ok')
    except AssertionError:
        raise DataError(data_error_str + 'COULDN\'T MATCH ALL INGREDIENTS TO IDS')

    # ADD RECIPE INFO
    row_values = (recipe_id, recipe_name, instructions, cook_time_minutes, comment, True)
    try:
        addRecipeInfo(db_connection, row_values)
    except Exception as e:
        raise DataError(f'ADDING RECIPE INFO-{data_error_str}{e}')

    # ADD INGREDIENTS
    for new_ingred_pair in ingreds_loadable: #
        if new_ingred_pair[0] > highest_ingred_id: # if ingred has new id number
            try:
                addIngredient(db_connection,new_ingred_pair)
            except Exception as e:
                raise DataError(f'ADDING INGREDIENTS-{data_error_str}{e}')

    # ADD RECIPE INGREDIENTS
    for item in ingreds_loadable:
        try:
            addRecipeIngredient(db_connection,(recipe_id,item[0])) # add to table using recipe_id,ingred_id
        except Exception as e:
            raise DataError(f'ADDING RECIPE INGREDIENTS-{data_error_str}{e}')

    print('RECIPE SUCCESSFULLY ADDED')
    #----------------------------------------------------------------------------------------


def deleteRecipe(recipe_id:int,db_connection_str:str):
    """delete recipe record from database"""
    db_connection_str = sqlite3.connect(db_connection_str)
    delete_tables = ('Recipe','RecipeIngredient','Image')
    for table in delete_tables:
        execute_script = f'DELETE FROM {str(table)} WHERE recipe_id={recipe_id}'
        with db_connection_str:
            db_connection_str.execute(execute_script)



"""FUNCTIONS THAT ALTER A RECORD"""
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

def toggleFav(recipe_id:int,db_connection)-> None:
    """toggle recipe fav value between True and False"""
    # get current fav value
    execute_script = f'SELECT favorite from Recipe WHERE recipe_id = {recipe_id}'
    db_connection = sqlite3.connect(db_connection)
    with db_connection:
        current_fav_value = db_connection.execute(execute_script)
    current_fav_value = current_fav_value.fetchall()[0][0]
    print(f'#{recipe_id} - current fav value is {current_fav_value}')
    if current_fav_value:
        new_fav_value = False
    else:
        new_fav_value = True
    execute_script = 'UPDATE Recipe ' \
                     f'SET favorite = {new_fav_value} ' \
                     f'WHERE recipe_id = {recipe_id}'
    with db_connection:
        db_connection.execute(execute_script)
    if new_fav_value:
        print('recipe favorited')
    else:
        print('recipe un-favorited')

"""FUNCTIONS THAT RETURN TABLE INFO / CHECK COLUMN,TABLE INFO"""
def getMaxIdNum(db_connection,column:str,table:str):
    execute_script = f"SELECT MAX({column}) FROM {table}" # script to get the highest number
    db_connection = sqlite3.connect(db_connection) # connect to database
    with db_connection:
        highest_id_num = db_connection.execute(execute_script) # execute the command

    return highest_id_num.fetchone()[0] # return the highest recipe_id number

def validRecipeName(db_connection,recipe_name):
    execute_script = "SELECT recipe_id,recipe_name FROM Recipe WHERE recipe_name = ?"  # script to get recipe / recipe_name
    db_connection = sqlite3.connect(db_connection)  # connect to database
    recipe_name = recipe_name.lower().replace(' ','_')
    with db_connection:
        record = db_connection.execute(execute_script,(recipe_name,))  # execute the command
    if record.fetchone():  # recipe name already exist
        return False
    else: # recipe name is unique
        return True

def isUniqueIngred(db_connection, ingredient):
    """returns True,None if ingredient isnt in database, returns False,ingred_id if it is"""
    execute_script = f'SELECT ingred_id FROM Ingredient WHERE ingred_name LIKE ?' # make the query
    placeholder = ''
    execute_script += placeholder
    db_connection = sqlite3.connect(db_connection)  # connect to database
    with db_connection:
        results = db_connection.execute(execute_script,(str(ingredient.lower()),))  # execute the command
    results = results.fetchone()
    if results: # if ingrient is in database (not unique)
        return False,results[0]
    else: # ingredient is unique
        return True,None