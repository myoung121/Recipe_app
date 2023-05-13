"""USER HELP/INFO SHOWN ON HELP PAGE"""


navigation_widget_title = 'Navigation Bar (top right buttons on screen)'
navigation_widget_desc = ('Go to different pages or quit the application.',)
# explain what the navigation buttons do
navigation_widget_fields = {'Help Button': ('open the Help/Info window.',),
                           'Search Button': ('go to the Search Recipe page.',),
                           'Add Button': ('go to the Add Recipe page.',),
                           'Home Button': ('go to the Home page.',),
                           'Quit Button': ('close the application.',)}

def makeTxtBlock(widget_title_location:str,widget_desc:tuple,fields:dict[str,tuple]):
    """returns widget info in a formatted string"""
    all_text = ''
    all_text += f'\n  {widget_title_location}:\n'
    for desc in widget_desc:
        all_text += f'    {desc}\n'
    all_text += '    Fields:\n'
    for widget in fields.keys(): # go over keys
        all_text += f'      {widget}:\n'
        for widget_desc in fields[widget]:
            all_text += f'        - {widget_desc}\n'

    return all_text


def getNavBarInfo(navigation_text=navigation_widget_title,navigation_desc:tuple=navigation_widget_desc,navigation_page_info:dict=navigation_widget_fields):
    """returns Navigation Bar widget info text shown on the HelpPage"""
    return makeTxtBlock(widget_title_location=navigation_text,
                                widget_desc=navigation_desc,
                                fields=navigation_page_info)


def getHomeTxt():
    """returns HomePage info text shown on the HelpPage"""
    page_info = 'Gives access to app pages\n' \
                'Displays 3 random recipe images with the image title.\n'
    all_txt = f'{page_info}\nFields:\n'
    all_txt += getNavBarInfo()
    return all_txt



def getSearchTxt():
    """returns SearchPage info text shown on the HelpPage"""
    page_info = 'Search for and Delete recipes.\n' \
                'Image on page is random.\n'
    all_txt = f'{page_info}\nFields:\n'

    info_banned_ingreds = makeTxtBlock(widget_title_location='Excluded Ingredients (left most boxes)',
                                       widget_desc=(
                                       'Recipe search results will exclude recipes with ingredients in the bottom field.',
                                       'Does not apply to favorite recipes.'),
                                       fields={'Top Entry Bar': (
                                                                 'input ingredients and press enter to add to excluded list display.',
                                                                 'input can only be added to display once / no repeats'),
                                               'Bottom Display': ('shows all ingredients excluded from recipe search',
                                                                  'double click item to remove it from the display')})
    info_search_display = makeTxtBlock(widget_title_location='Search Results (center of screen)',
                                       widget_desc=(
                                       'Display the recipe search results.',),
                                       fields={'Display Area': ('display the recipe search results',
                                                                 'press enter or double click to open selected recipe')})
    info_chk_buttons = makeTxtBlock(widget_title_location='Recipe Search Filters (center screen below recipe display area)',
                                       widget_desc=('Select the filter applied when searching recipes for a keyword.',
                                       'Only one can be selected at a time',
                                       'Selected filter is highlighted'),
                                       fields={'Name': ('search by recipe name',),
                                               'Recipe #':('search by recipe # (default)',),
                                               'Ingredients':('search by recipe Ingredients',),
                                               'Steps':('search by recipe steps / instructions',)})
    info_delete_button = makeTxtBlock(widget_title_location='Delete Recipe Button (center screen, left of Search Bar)',
                                       widget_desc=(
                                       'Remove saved recipe and its image from database',
                                       'Doesnt remove the recipes ingredients form the database (others might need it)'),
                                       fields={'Delete Button': ('remove saved recipe and its image from database',)})
    info_search_bar = makeTxtBlock(widget_title_location='Recipe Search Bar (center screen below Recipe Search Filters)',
                                       widget_desc=('Input keywords to search for recipes',
                                       'If input is blank, it list the default (Recipe #) in order'),
                                       fields={'Search Bar': ('takes search text input',
                                                                 'can press enter to search'),
                                               'Enter Button': ('submits search text',)})
    info_image = makeTxtBlock(widget_title_location='Food Image (right screen below navigation buttons)',
                                       widget_desc=('Food image and name',),
                                       fields={'Image': ('shows a different random recipe image whenever the application is opened',),
                                               'Image Name': ('display the random recipe image\'s name',)})
    info_btm_buttons = makeTxtBlock(widget_title_location='Bottom Buttons (right side of screen below image)',
                                       widget_desc=('Action buttons',),
                                       fields={'Go': ('open selected recipe in a new window',),
                                               'Random': ('open a random saved recipe in a new window',),
                                                'Favs': ('displays all favorite recipes in the center display',)})
    all_txt += getNavBarInfo() +info_banned_ingreds +info_search_display +info_chk_buttons +info_delete_button +info_search_bar +info_image + info_btm_buttons
    return  all_txt

def getAppInfoTxt():
    """returns application info text shown on the HelpPage"""
    author = 'M. Young'
    date = '05/14/2023'
    app_name = 'CookBook App'
    page_info = f'{app_name} Information.\n'
    all_txt = f'{page_info}\nAuthor: {author}\nDate: {date}'
    return all_txt
def getAddTxt():
    """returns AddPage info text shown on the HelpPage"""
    page_info = 'Save a recipe.\n'
    all_txt = f'{page_info}\nFields:\n'
    info_recipe_info = makeTxtBlock(widget_title_location='Recipe Input Area (right 2 columns)',
                                       widget_desc=('Includes name,notes,cooktime,ingredients, and instructions entries',
                                                    'Only the name, 1 ingredient, and 1 instruction step required to save a recipe',
                                                    'Entry fields are not case sensitive'),
                                       fields={'Name': ('recipe name entry','REQUIRED','no duplicates allowed'),
                                               'Cooktime': ('store the time it takes to cook recipe in minutes',),
                                               'Notes': ('store notes and comments about a recipe',),
                                               'Ingredients': ('add a ingredient to the recipe',
                                                               'press enter to add input',
                                                               'input is displayed to the right of entry',
                                                               'each ingredient can only be added to a recipe once'),
                                               'Instructions': ('add instruction steps to the recipe',
                                                                'press enter to add input',
                                                                'input is displayed to the right of entry',
                                                                'each step can only be added to a recipe once')})
    info_ingreds_display = makeTxtBlock(widget_title_location='Ingredients Display (3rd column display area)',
               widget_desc=('display all added ingredients','remove an added ingredient',),
               fields={'Display': ('display all added ingredients',),
                       '\'X\' Button': ('remove selected added ingredient',)
                      })
    info_instrs_display = makeTxtBlock(widget_title_location='Instructions Display (4th column display area)',
               widget_desc=('display all added instructions','remove an added ingredient',),
               fields={'Display': ('display all added instructions',),
                       '\'X\' Button': ('remove selected added instruction',)
                      })
    info_save_button = makeTxtBlock(widget_title_location='Save Button (top left of screen)',
               widget_desc=('Save the recipe',),
               fields={'Save Button': ('save the recipe',)})
    all_txt += getNavBarInfo() +info_save_button +info_recipe_info +info_ingreds_display +info_instrs_display
    return all_txt


def getRecipeTxt():
    """returns RecipePage info text shown on the HelpPage"""
    page_info = 'Display the selected recipe.\n' \
                'Only 5 unique recipes can be open at one time.\n' \
                'Recipe number and name displayed in the title\n' \
                'Background colors are random.\n'

    all_txt = f'{page_info}\nFields:\n'

    info_top_buttons = makeTxtBlock(widget_title_location='Add recipe to Favorites / close window (top right of screen)',
               widget_desc=('mark the displayed recipe as a favorite','close the recipe window'),
               fields={'Fav': ('mark the displayed recipe as a favorite',),
                       u"\u2B50\uFE0F(star)": ('when displayed, the selected recipe is a favorite',),
                      'Close':('close selected recipe window',)})

    info_ingreds_display = makeTxtBlock(widget_title_location='Ingredients Display (top display left of screen)',
               widget_desc=('display the selected recipe ingredients',),
               fields={'Ingredients': ('display the selected recipe ingredients',)})
    info_instrs_display = makeTxtBlock(widget_title_location='Instructions Display (bottom display left of screen)',
                                        widget_desc=('display the selected recipe instructions',),
                                        fields={'Instructions': ('display the selected recipe instructions',)})

    info_recipe_image = makeTxtBlock(widget_title_location='Recipe Image and name (left of screen below close button)',
               widget_desc=('display selected recipe image and name','if recipe was added by a user, the image and name will be a random recipe\'s image and name'),
               fields={'Image': ('display selected recipe\'s image',),
                       'Image name': ('selected recipe\'s image',)
                      })

    info_comment_area = makeTxtBlock(widget_title_location='Recipe comment (right of screen below recipe image)',
               widget_desc=('view/edit/save recipe comment',),
               fields={'Comment Display': ('display recipe comments',
                                           'read-only until edit button is pressed'),
                       'Edit Button': ('allows editing of the recipe comment',),
                       'Save Button': ('save the recipe comment',)})
    return all_txt +info_top_buttons +info_ingreds_display +info_instrs_display +info_recipe_image +info_comment_area

