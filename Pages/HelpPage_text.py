"""USER HELP/INFO SHOWN ON HELP PAGE"""
from typing import Dict

# explain functions
navigation_widget_text = 'Navigation Bar (top right buttons on screen):\n' \
                         '    Go to different pages or quit the application.'
# explain what the navigation buttons do
navigation_buttons_info= {'help':'Help: Open the Help/Info window.',
                           'search': 'Search: Go to the Search Recipe page.',
                           'add':'Add: Go to the Add Recipe page.',
                           'home':'Home: Go to the Home page.',
                           'quit':'Quit: Close the application.\n'}

# navigation buttons common on all pages(nav always has help 1st and quit last, an unless on home, home button is 2nd to last)
all_tabs_shared_nav_text = [navigation_buttons_info['help'],navigation_buttons_info['quit']]

def getHomeTxt(navigation_text=navigation_widget_text,navigation_page_info:dict=navigation_buttons_info):
    """returns HomePage info text shown on the HelpPage"""
    page_info = 'Displays 3 random recipe images with the image title.\n\nFields:\n  '
    nav_info_text = (navigation_text,navigation_page_info['help'],navigation_page_info['search'],
                     navigation_page_info['add'],navigation_page_info['quit'])
    nav_info_text = '\n      '.join(nav_info_text)

    all_text=  f'{page_info}' +nav_info_text # all text and info that is displayed
    return all_text

def getSearchTxt(navigation_text=navigation_widget_text,navigation_page_info:dict=navigation_buttons_info):
    """returns HomePage info text shown on the HelpPage"""
    all_txt = ''
    info_nav = (navigation_text,navigation_page_info['help'],navigation_page_info['add'],navigation_page_info['home'],navigation_page_info['quit'])
    page_info = 'Search for and Delete recipes.\n\nFields:\n  ' # explain purpose of search page
    nav_info_text = (navigation_text,navigation_page_info['help'],navigation_page_info['add'],
                     navigation_page_info['home'],navigation_page_info['quit'])
    nav_info_text = '\n      '.join(nav_info_text)

    info_banned_ingeds = '\n  Excluded Ingredients (left most boxes):\n' \
                         '    Recipe search results will exclude recipes with ingredients in the bottom field.\n' \
                         '    Does not apply to favorite recipes.\n' \
                         '    Fields:\n' \
                         '      Top Entry Bar - input ingredients and press enter to add to excluded list display.\n' \
                         '                    - input can only be added to display once / no repeats\n'\
                         '      Bottom Display - shows all ingredients excluded from recipe search\n' \
                         '                     - double click item to remove it from the display\n'

    info_search_display = '\n  Search Results (center of screen):\n' \
                            '    Display the recipe search results.\n' \
                            '    Fields:\n'\
                            '      Display Area - display the recipe search results\n'\
                            '                   - press enter or double click to open selected recipe\n'

    info_chk_buttons = '\n  Recipe Search Filters (center screen below recipe display area):\n'\
                         '    Select the filter applied when searching recipes for a keyword.\n'\
                         '    Only one can be selected at a time\n' \
                         '    Selected filter is highlighted\n' \
                         '    Fields:\n' \
                         '      Name - Search by recipe name\n' \
                         '      Recipe # - Search by recipe # (default)\n' \
                         '      Ingredients - Search by recipe Ingredients\n' \
                         '      Steps - Search by recipe steps / instructions\n'

    info_delete_button = '\n  Delete Recipe Button (center screen, left of Search Bar):\n' \
                         '      Remove saved recipe and its image from database\n' \
                         '      Doesnt remove the recipes ingredients form the database (others might need it)\n' \
                         '      Fields:\n' \
                         '        Delete Button - remove saved recipe and its image from database\n'


    info_search_bar = '\n  Recipe Search Bar (center screen below Recipe Search Filters):\n' \
                      '      Input keywords to search for recipes\n' \
                      '      If input is blank, it list the default (Recipe #) in order\n' \
                      '      Fields:\n' \
                      '        Search Bar - takes search text input\n' \
                      '                   - can press enter to search\n' \
                      '        Enter Button - submits search text\n' \
                                              

    info_image = '\n  Food Image (right screen below navigation buttons):\n' \
                 '      Food image and name\n' \
                 '      Fields:\n' \
                 '        Image - shows a different random recipe image whenever the application is opened\n' \
                 '        Image Name - display the random recipe image\'s name\n'

    info_btm_buttons = '\n  Bottom Buttons (right side of screen below image):\n' \
                       '      Action buttons\n' \
                       '      Fields:\n' \
                       '        Go - open selected recipe in a new window\n' \
                       '        Random - open a random saved recipe in a new window\n' \
                       '        Favs - displays all favorite recipes in the center display\n'

    all_txt += page_info +nav_info_text +info_banned_ingeds + info_search_display +info_chk_buttons \
               +info_delete_button +info_search_bar +info_image + info_btm_buttons
    return  all_txt

if __name__ == '__main__':
    info = getHomeTxt()
    print(info)
'''

def getAddTxt(navogation_text,navigation_page_info:dict):
    """returns HomePage info text shown on the HelpPage"""
    nav_info_text = (navigation_page_info['help'],navigation_page_info['quit'])
def getHelpTxt(navogation_text,navigation_page_info:dict):
    """returns HomePage info text shown on the HelpPage"""
    nav_info_text = (navigation_page_info['help'],navigation_page_info['quit'])
def getAppInfoTxt(navogation_text,navigation_page_info:dict):
    """returns HomePage info text shown on the HelpPage"""
    nav_info_text = (navigation_page_info['help'],navigation_page_info['quit'])
def getLogsTxt(navogation_text,navigation_page_info:dict):
    """returns HomePage info text shown on the HelpPage"""
    nav_info_text = (navigation_page_info['help'],navigation_page_info['quit'])'''
