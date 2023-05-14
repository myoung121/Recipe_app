"""DATABASE QUERY FUNCTIONS"""

import random as ran
import sqlite3
from PIL import Image, ImageTk
import  io




"""RETURN MULTIPLE RECIPE RECORDS"""

def getRowsAll(table_name: str, db_connection_str:str) -> list:
    """ return all rows in a table """
    execute_script = f'SELECT * FROM ' + str(table_name)
    db_connection_str = sqlite3.connect(db_connection_str)
    with db_connection_str:
        all_rows = db_connection_str.execute(execute_script)
    return all_rows.fetchall()
def getFilteredRecipes(search_txt, db_connection_str:str, excluded_ingreds:tuple =(),
                       user_filter: str= 'name', return_all:bool=False):
    """returns recipes based off filter"""
    allowed_filters = ('name', 'recipe_id', 'ingredient', 'instruction')
    blank_box = False # if user press enter with empty search box
    if user_filter in allowed_filters:
        db_connection_str = sqlite3.connect(db_connection_str) # connect to database
        execute_script = f'SELECT DISTINCT Recipe.recipe_id,recipe_name,prep_time,cook_time ' \
                         f'FROM Recipe' # query base template
        if user_filter == allowed_filters[0]:  # filter by name
            if return_all and excluded_ingreds:
                blank_box = True
            else:
                search_txt = search_txt.replace(' ', '_')
                # build rest of query
                execute_script += ' WHERE recipe_name ' \
                                  'LIKE '
                placeholder = f'\'%{search_txt.lower()}%\''
                execute_script += placeholder

        elif user_filter == allowed_filters[1]:  # filter by recipe_id
            execute_script += ' WHERE recipe_id ' \
                              'LIKE '
            placeholder = f'\'%{search_txt}%\''
            execute_script += placeholder # build rest of query

        elif user_filter == allowed_filters[2]:  # filter byingredients
            execute_script += ' JOIN RecipeIngredient ON Recipe.recipe_id=RecipeIngredient.recipe_id ' \
                              'JOIN Ingredient ON RecipeIngredient.ingred_id=Ingredient.ingred_id ' \
                              'WHERE ingred_name ' \
                              'LIKE '
            placeholder = f'\'%{search_txt}%\''
            execute_script += placeholder # build rest of query

        elif user_filter == allowed_filters[3]:  # filter by instructions
            execute_script += ' WHERE instr ' \
                              'LIKE '
            placeholder = f'\'%{search_txt}%\''
            execute_script += placeholder # build rest of query
    else:
        exit(f'{user_filter} Filter not Allowed')
    if excluded_ingreds: # if user has banned ingredients in display
        if blank_box: # excluded ingreds and empty search box
            execute_script += ' WHERE Recipe.recipe_id NOT IN (' # expand query
        if not blank_box: # have user input ingred
            execute_script += ' AND Recipe.recipe_id NOT IN ('
        for ingred in excluded_ingreds: # build subset to check recipe_ids against
            execute_script += f'SELECT RecipeIngredient.recipe_id ' \
                              'FROM RecipeIngredient ' \
                              'JOIN Ingredient ON RecipeIngredient.ingred_id=Ingredient.ingred_id ' \
                              f'WHERE Ingredient.ingred_name LIKE \'%{ingred}%\' UNION '
        execute_script = execute_script.rstrip(' UNION ') # clean extra
        execute_script += ')' # close for query
    # execute query
    with db_connection_str:
        values = db_connection_str.execute(execute_script)
        values = values.fetchall()
    return values

def getFavorites(db_connection_str):
    """returns favorite recipes"""
    execute_script = 'SELECT recipe_id,recipe_name FROM Recipe WHERE favorite = True' # query to get favorite recipes from table
    db_conn =  sqlite3.connect(db_connection_str)
    with db_conn:
        all_rows = db_conn.execute(execute_script)
    return all_rows.fetchall()

def getImageRandom(db_connection_str:str,num_of_images:int=1)->list:
    """ return one or multiple random image names with images in jpeg format"""
    # get all image_ids
    execute_script = 'SELECT image_id from Image'
    db_connection = sqlite3.connect(db_connection_str)
    with db_connection:
        image_ids = db_connection.execute(execute_script) # get all image ids
    image_ids=image_ids.fetchall()
    ran_image_ids = ran.sample(image_ids,num_of_images)# get the number of random image_ids requested
    execute_script = 'SELECT image_name,image_blob FROM Image WHERE image_id IN '# make new script to get images based on the selected image_ids
    # add placeholder for each image_id
    placeholders_str = "(" + '?,' * num_of_images
    placeholders_str = placeholders_str[:-1] + ")"
    # put the script together
    execute_script += placeholders_str
    with db_connection:
        random_images = db_connection.execute(execute_script,tuple(x[0] for x in ran_image_ids))# get the images based off the ids
    random_images = random_images.fetchall()
    # convert binary images to images tkinter can use
    random_jpeg_images =[]
    for image_pair in random_images:
        sub_list = [image_pair[0]]
        # convert image bytes to PIL image format(jpeg)
        pic = Image.open(io.BytesIO(image_pair[1]))
        sub_list.append(ImageTk.PhotoImage(pic))
        random_jpeg_images.append(tuple(sub_list))
    return random_jpeg_images
#-----------------------------------------------------------------------------------------------------------------------


"""RETURN A SINGLE RECORD """
def getRecipeInfo(recipe_id: int, db_connection_str:str) -> (dict, bytes):  # show recipe button
    """return all recipe info needed to build recipe page"""
    table_names: tuple = ('Recipe', 'RecipeIngredient', 'Image') # IMAGE MUST BE LAST!!!
    recipe_info = {} # all recipe record info
    unique_ingreds = getRowsAll('Ingredient',db_connection_str) # all ingredients in the table / recipe ingredients are stored as ingred table id number
    db_connection = sqlite3.connect(db_connection_str) # database connection
    for item_rows in table_names: # collect record info from all tables
        try:
            execute_script_str = f'SELECT * ' \
                                 f'FROM  {item_rows} ' \
                                 f'WHERE recipe_id = {recipe_id}'
            if item_rows == 'Recipe': # get info from recipe table
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

            elif item_rows == 'RecipeIngredient': # get recipe ingredients
                recipe_info['ingredients'] = []
                with db_connection:
                    stats = db_connection.execute(execute_script_str)
                    stats = stats.fetchall()
                for num, food in enumerate(stats):
                    recipe_info['ingredients'].append(unique_ingreds[int(food[1])][1]) # get ingredients name based off ingred table id numbers/index

            elif item_rows == 'Image': # get recipe image
                with db_connection:
                    stats = db_connection.execute(execute_script_str)
                    stats = stats.fetchall()[0]
                recipe_info['image_name'] = stats[2].replace('_', " ").title()
                image_blob = stats[3]
        except Exception as e:
            if 'list index' in str(e): # ignore index error here. It throws if recipe has no image and is handled at end of iteration
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
    execute_script = 'SELECT recipe_id FROM Recipe' # query
    db_connection = sqlite3.connect(db_connection_str) # db connection
    with db_connection:
        all_ids = db_connection.execute(execute_script)
    all_ids = all_ids.fetchall()
    # pick a random recipe_id and get the id number alone
    ran_recipe_num = ran.sample(all_ids,1)[0][0] # pick a random recipe from id numbers
    return getRecipeInfo(recipe_id=ran_recipe_num, db_connection_str=db_connection_str)# pass recipe_id into function to get recipe info

# ----------------------------------------------------------------------------------------------------------------------

"""FUNCTIONS THAT RETURN TABLE INFO / CHECK COLUMN,TABLE INFO"""
def getMaxIdNum(db_connection,column:str,table:str):
    """return the highest id number(primary key)"""
    execute_script = f"SELECT MAX({column}) FROM {table}" # script to get the highest number
    db_connection = sqlite3.connect(db_connection) # connect to database
    with db_connection:
        highest_id_num = db_connection.execute(execute_script) # execute the command
    return highest_id_num.fetchone()[0] # return the highest id number

def validRecipeName(db_connection,recipe_name):
    """"return True if recipe name already exist, else return False"""
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
    """returns (True,None) if ingredient isn't in database, returns (False,ingred_id) if it is"""
    execute_script = f'SELECT ingred_id FROM Ingredient WHERE ingred_name LIKE ?' # make the query
    db_connection = sqlite3.connect(db_connection)  # connect to database
    with db_connection:
        results = db_connection.execute(execute_script,(str(ingredient.lower()),))  # execute the command
    results = results.fetchone()
    if results: # if ingrient is in database (not unique)
        return False,results[0]
    else: # ingredient is unique
        return True,None

# ----------------------------------------------------------------------------------------------------------------------
"""FUNCTIONS THAT ALTER A RECORD"""

def addComment(recipe_id:int,db_connection,comment:str)->None:
    """add comment text to recipe record"""
    execute_script = 'UPDATE Recipe ' \
                     'SET comment=? ' \
                     'WHERE recipe_id=?' # query
    db_connection = sqlite3.connect(db_connection)
    with db_connection:
        db_connection.execute(execute_script,(str(comment),recipe_id))
    print(f'+{recipe_id} comment updated+')

def removeComment(recipe_id:int,db_connection)->None:
    """sets recipe comment to empty string"""
    print(f'+{recipe_id} comment removed +')
    return addComment(recipe_id=recipe_id,db_connection=db_connection,comment='')


def toggleFav(recipe_id:int,db_connection)-> None:
    """toggle recipe fav value between True and False"""
    execute_script = f'SELECT favorite from Recipe WHERE recipe_id = {recipe_id}'# get current fav value
    db_connection = sqlite3.connect(db_connection) # database connection
    with db_connection:
        current_fav_value = db_connection.execute(execute_script)
    current_fav_value = current_fav_value.fetchall()[0][0] # current fav value
    new_fav_value = not current_fav_value
    execute_script = 'UPDATE Recipe ' \
                     f'SET favorite = {new_fav_value} ' \
                     f'WHERE recipe_id = {recipe_id}'
    with db_connection:
        db_connection.execute(execute_script) # execute
    print(f'+{recipe_id} favorite updated+')

# ----------------------------------------------------------------------------------------------------------------------
"""FUNCTIONS THAT ALTER A TABLE"""

def addRecipe(db_connection,recipe_name:str,instructions,
              ingredients,cook_time_minutes=0,comment:str=''):
    pre_load_checks ={'id_ok':False,'name_ok':False,
                      'ingreds_ok' : False,'instrs_ok' : False,
                      'cktime_ok' : False,'comment_ok': False
                      } # checks must be passed be fore recipe is added
    # CUSTOM EXCEPTIONS OUTPUT TEMPLATES
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
        """ADD INGREDIENTS TO INGREDIENT TABLE"""
        execute_script = 'INSERT INTO Ingredient (ingred_id,ingred_name) VALUES (?,?)'
        db_connection1 = sqlite3.connect(db_connection1)
        with db_connection1:
            db_connection1.execute(execute_script,(*ingred_id_ingred_pair,))
            print(f'\t+{recipe_id} ingredient added +')

    def addRecipeIngredient(db_connection1,recipe_ingred_ids_pair:tuple|str):
        """add recipe_id and ingred_id to database"""
        execute_script = 'INSERT INTO RecipeIngredient (recipe_id,ingred_id) VALUES (?,?)'
        db_connection1 = sqlite3.connect(db_connection1)
        with db_connection1:
            db_connection1.execute(execute_script,(*recipe_ingred_ids_pair,))
            print(f'\t+{recipe_id} recipe ingredient added +')

    def addRecipeInfo(db_connection1,record_values:tuple|str):
        """add values to columns recipe_id, recipe_name, instr, cook_time, comment, favorite to recipe table"""
        print(record_values)
        execute_script = 'INSERT INTO Recipe(recipe_id, recipe_name, instr, cook_time, comment, favorite) VALUES'
        placeholders_str = "(" + '?,' * len(record_values)
        placeholders_str = placeholders_str[:-1] + ")"
        execute_script += placeholders_str
        db_connection1 = sqlite3.connect(db_connection1)
        with db_connection1:
            db_connection1.execute(execute_script, (*record_values,))
            print(f'\t+{recipe_id} recipe info added +')
    #########################################################
    #----------------------------------------------------------------------------------------
    # VALIDATE INPUTS

    print('CHECKING RECIPE INFO...')
    # CHECK RECIPE ID - REQUIRED COLUMN
    recipe_id = getMaxIdNum(db_connection,'recipe_id','Recipe') + 1 # set the recipe_id to the largest recipe_id in table + 1
    try:
        assert isinstance(recipe_id,int) # should be an int
        pre_load_checks['id_ok'] = True
    except AssertionError:
        raise EntryError(input_error_str + 'RECIPE ID SHOULD BE AN INTEGER')

    # CHECK RECIPE NAME - REQUIRED COLUMN
    if recipe_name:
        try:
            assert isinstance(recipe_name,str) # must be a str
            recipe_name = recipe_name.lower() # in lower case
        except AssertionError:
            raise EntryError(input_error_str + 'RECIPE NAME SHOULD BE A STRING')
        try:
            assert validRecipeName(db_connection,recipe_name) == True # check that recipe name is unique
            pre_load_checks['name_ok'] = True
        except AssertionError:
            raise EntryError(input_error_str + 'RECIPE NAME ALREADY IN USE')
    else: # recipe name is blank
        raise EntryError(input_error_str + 'RECIPE NAME IS BLANK')

    # CHECK COOKTIME
    if not cook_time_minutes:
        cook_time_minutes = 0
    try:
        cook_time_minutes = int(cook_time_minutes)
        assert cook_time_minutes >=0 #MUST BE AN INT GREATER THAN OR EQUAL TO 0
        pre_load_checks['cktime_ok'] = True
    except ValueError:
        raise EntryError(input_error_str + 'COOK TIME SHOULD BE AN INTEGER')
    except AssertionError:
        raise EntryError(input_error_str + 'COOK TIME SHOULD BE GREATER THAN 0 MINUTES')

    # CHECK COMMENT
    try:
        assert isinstance(comment, str) # check if in correct data type
        pre_load_checks['comment_ok'] = True
    except AssertionError:
        raise EntryError(input_error_str + 'COMMENT SHOULD BE A STRING')


    # CHECK INSTRUCTIONS
    try:
        assert isinstance(instructions,str)
        #print(instructions)
        instructions = instructions # input is show in stack in display
        pre_load_checks['instrs_ok'] = True
    except AssertionError:
        raise EntryError(input_error_str + 'INSTRUCTIONS SHOULD BE A STRING')

    # CHECK INGREDIENTS
    try:
        assert isinstance(ingredients,tuple) # make sure ingredients are in tuple
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
        ingreds_loadable = tuple(zip(ingredients_ids,ingredients)) # make sure every ingred has an id number and none are left out
        assert len(ingredients_ids) == len(ingreds_loadable)
        ingreds_loadable = ingreds_loadable # input is show in stack in display
        pre_load_checks['ingreds_ok'] = True
    except AssertionError:
        raise DataError(data_error_str + 'COULDN\'T MATCH ALL INGREDIENTS TO IDS')
    #===================================================================================================================
    # AFTER ALL CHECKS ARE PASSED
    for check in pre_load_checks: # make sure all checks were passed
        try:
            assert pre_load_checks[check] == True
        except AssertionError as e:
            raise DataError(f'PRELOAD CHECKS NOT PASSED-{data_error_str}{e}\n{pre_load_checks}')
    # ADD RECIPE INFO TO RECIPE TABLE
    print('\tALL CHECKS PASSED')
    row_values = (recipe_id, recipe_name, instructions, cook_time_minutes, comment, True)
    try:
        addRecipeInfo(db_connection, row_values)
    except Exception as e:
        raise DataError(f'ADDING RECIPE INFO-{data_error_str}{e}')

    # ADD INGREDIENTS TO INGREDIENT TABLE
    for new_ingred_pair in ingreds_loadable: #
        if new_ingred_pair[0] > highest_ingred_id: # if ingred has new id number
            try:
                addIngredient(db_connection,new_ingred_pair)
            except Exception as e:
                raise DataError(f'ADDING INGREDIENTS-{data_error_str}{e}')

    # ADD RECIPE INGREDIENTS TO RECIPEINGREDIENT TABLE ADD
    for item in ingreds_loadable:
        try:
            addRecipeIngredient(db_connection,(recipe_id,item[0])) # add to table using recipe_id,ingred_id
        except Exception as e:
            raise DataError(f'ADDING RECIPE INGREDIENTS-{data_error_str}{e}')

    print(f'\t+recipe {recipe_id} successfully added +')
    #----------------------------------------------------------------------------------------


def deleteRecipe(recipe_id:int,db_connection_str:str):
    """delete recipe record from database"""
    db_connection_str = sqlite3.connect(db_connection_str)
    delete_tables = ('Recipe','RecipeIngredient','Image') # look for recipe id in these tables
    for table in delete_tables:
        execute_script = f'DELETE FROM {str(table)} WHERE recipe_id={recipe_id}'
        with db_connection_str:
            db_connection_str.execute(execute_script) # execute
    print(f'+{recipe_id} deleted +')

