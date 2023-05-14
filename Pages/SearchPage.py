"""SEARCH PAGE"""
import tkinter as tk
from tkinter import messagebox
from Functions import db_query_functions
from Widgets import NavBar

class Search(tk.Frame):
    rows = [] # current search results
    banned_ingreds = [] # current banned ingredients
    user_last_search_str = ''  # users last searched words
    user_last_filter = 'name'  # users last filter applied

    def __init__(self, parent, controller, page_info):
        tk.Frame.__init__(self, parent)
        # parent is the root window
        # controller switches the pages
        # page_info is all info needed to build this page
        self.BG_COLOR =page_info['bg_color'] # page background color
        self.config(bg=self.BG_COLOR) # set page to color
        DB_STR = page_info['db_str'] # recipe database location
        MAX_PAGES = page_info['max_pages'] # number of pages that can be open at one time
        RECIPE_PAGE = page_info['recipe_page'] # recipe page object
        open_recipe_windows = page_info['open_pages'] # track recipes pages opened
        image_info = db_query_functions.getImageRandom(DB_STR)[0] # random image to display
        self.image_name = image_info[0].replace('_',' ') # clean image name / set to page
        self.image = image_info[1] # keeps image showing on page

        # FUNCTIONS
        def checkBoxControl(box_var: tk.Checkbutton):
            """this function makes sure only one check box is selected at a time"""
            chk_boxes = [x for x in (chk_bx_recipe_id, chk_bx_name, chk_bx_ingred, chk_bx_instrs) if x != box_var] # all check boxes except the one clicked
            for x in chk_boxes:
                if x: # if selected
                    x.deselect()
                    x.config(fg='white') # change text color back to white
            box_var.select() # select clicked check box
            box_var.config(fg='green') # change text color to green
        def checkBoxStatus():
            """this function returns name of which text box is selected or None"""
            chk_boxes = {'recipe_id': recipe_toggle, 'name': title_toggle,
                         'ingredient': ingred_toggle, 'instruction': instrs_toggle} # check box variables used to track if selected
            for column, boxy in chk_boxes.items():
                if boxy.get():
                    return column # the key/column is passed to the query function
            return None

        def search(event=None):
            """uses input from search box to get recipes from db"""
            global rows
            l_box_search.delete(0, tk.END) # clear the search display box
            if not entry_search_text.get():  # if user pressed enter with no entry text
                checkBoxControl(chk_bx_name)  # set default search field to recipe id number
                rows = db_query_functions.getFilteredRecipes(search_txt='', db_connection_str=DB_STR,
                                                             user_filter=checkBoxStatus(),
                                                             return_all=True,  # return all recipes
                                                             excluded_ingreds = l_box_banned.get(0, tk.END)) # get all recipes
            else:
                rows = db_query_functions.getFilteredRecipes(search_txt=entry_search_text.get(),
                                                             db_connection_str=DB_STR,
                                                             user_filter=checkBoxStatus(),
                                                             excluded_ingreds=l_box_banned.get(0,tk.END))  # return filtered recipes
            for item in rows:# Add items to the search listbox
                item = list(item)
                item[1]=item[1].replace('_',' ')
                l_box_search.insert(tk.END, f'{item[0]}. {item[1].title()}')
            if entry_search_text.get():
                Search.user_last_search_str = entry_search_text.get()  # save last searched word
                Search.user_last_filter = checkBoxStatus()  # save last used filter
            entry_search_text.select_range(0,tk.END) # highlight user text for quick deletion

        def checkPages(name, recipe_pages: list, max_pages_open:int):
            """checks if pass conditions to open a new RecipePage """
            can_open = True # tracks if can open a new recipe page
            cant_open_str = f'cant open {name} - ' # user message
            if name in recipe_pages:  # if recipe page already open
                can_open = False
                cant_open_str += 'recipe already open/ '
            if len(recipe_pages) == max_pages_open:  # if max number of pages open
                can_open = False
                cant_open_str += 'max number of recipes opened/ close a window to see recipe'
            if not can_open: # if it failed any condition
                print(cant_open_str + ' -F')
            return can_open

        def recipeSelect(event):
            """opens selected recipe"""
            selected_item = l_box_search.curselection()# Get the selected item in the list
            try:
                selected_recipe = db_query_functions.getRecipeInfo(recipe_id=rows[selected_item[0]][0],
                                                                   db_connection_str=DB_STR) # gather the recipe information / returns tuple (recipe_info-dict,image-bytes)
                check_passed = checkPages(selected_recipe[0]['name'], open_recipe_windows,MAX_PAGES)  # check if allowed to open a new window
                if check_passed:  # can show recipe
                    recipe_page = RECIPE_PAGE(selected_recipe[0], selected_recipe[1],open_recipe_windows,DB_STR) # new recipe page
                    open_recipe_windows.append(recipe_page.recipe_name) #add open window to tracker / tracks if recipe already op and how many are open
                    print(f'opened #{recipe_page.recipe_id}-{recipe_page.recipe_name} <-')
            except IndexError:  # if go button pressed while curser isnt on a recipe
                pass

        def randomRecipe():
            """opens a window with a random recipe"""
            selected_item = db_query_functions.getRecipeInfoRandom(db_connection_str=DB_STR) # get a random recipe
            check_passed = checkPages(selected_item[0]['name'],open_recipe_windows,
                                          MAX_PAGES)  # check if allowed to open a new window
            if check_passed:  # can show recipe
                recipe_page = RECIPE_PAGE(selected_item[0], selected_item[1],open_recipe_windows,DB_STR) # make recipe window
                open_recipe_windows.append(recipe_page.recipe_name) # add to tracker
                print(f'opened {recipe_page.recipe_id}-{recipe_page.recipe_name} <-')

        def getFavs():
            """returns recipes that are favorited"""
            global rows
            rows = db_query_functions.getFavorites(DB_STR) # get favorite recipes from database
            l_box_search.delete(0, tk.END) # clear the displayed recipes
            for item in rows:
                item = list(item) # change type to edit elements
                item[1]=item[1].replace('_',' ')
                l_box_search.insert(tk.END, f'{item[0]}. {item[1].title()}') # add recipe info to display
        def deleteRecipe():
            """permanently delete recipe from database"""
            selected_item = l_box_search.curselection() # get the selected recipe
            try:
                recipe_db_id = rows[selected_item[0]][0] # get recipe_id
                recipe_name = rows[selected_item[0]][1].replace("_", " ")
                if len(recipe_name) <= 25: # edit how name is displayed in the title to control size of popup
                    title_str = recipe_name.title()
                else:
                    title_str = f'{recipe_name.title():.25}...'
                confirmed = messagebox.askquestion(title=title_str,
                                                   message=f'DELETE\n{rows[selected_item[0]][1].replace("_", " ").title()}?')  # prompt user to confirm recipe deletion
                if confirmed == 'yes':
                    db_query_functions.deleteRecipe(recipe_id=int(recipe_db_id),
                                                    db_connection_str=DB_STR)  # delete recipe from db
                    rows.pop(selected_item[0])  # delete recipe from stored recipe search
                    l_box_search.delete(selected_item[0])  # delete recipe from listbox
            except IndexError:  # if delete button pressed while curser isnt on a recipe
                pass


        def addBanned(event):
            """add ingredient to banned list"""
            ingred_txt = entry_banned.get().lower().strip() # banned ingredient text box text
            if ingred_txt: # if text isnt blank
                if ingred_txt not in l_box_banned.get(0,tk.END): # if text not already in the box
                    l_box_banned.insert(0,ingred_txt) # add text to the box
            entry_banned.delete(0,tk.END) # clear text box

        def deleteBanned(event):
            """delete ingredient from banned list"""
            try:
                l_box_banned.delete(l_box_banned.curselection()) # delete selected txt from box
            except IndexError: # if item isnt fully highlighted will raise a tkinter error, can ignore
                pass
        # --------------------------------------------------------------------------------------
        # NAVIGATION BAR
        NavBar.NavBar(self,controller,2,self.BG_COLOR,('help','add','home','quit'))  # navigation frame / buttons

        # BANNED INGREDIENTS FRAME WIDGETS
        frame_banned_ingreds = tk.LabelFrame(self,bg=self.BG_COLOR) # MAIN FRAME
        frame_banned_ingreds.grid(row=0,rowspan=3,column=0,padx=4)
        lbl_banned_ingreds = tk.Label(frame_banned_ingreds,width=15,bg=self.BG_COLOR,fg='white',text='Excluded') # TET ABOVE BANNED ENTRY WIDGET
        lbl_banned_ingreds.grid(row=0,column=0)
        entry_banned = tk.Entry(frame_banned_ingreds,width=15) # TEXT ENTRY
        entry_banned.grid(row=1, column=0,pady=4)
        entry_banned.bind('<Return>', addBanned) # PRESS ENTER TO ADD INGREDIENT TO BANNED LISTBOX
        l_box_banned = tk.Listbox(frame_banned_ingreds,width=15,height=4)  # DISPLAYS BANNED INGREDIENTS
        l_box_banned.grid(row=3,column=0,pady=4)
        l_box_banned.bind('<Double-1>',deleteBanned) #double click deletes text from box
        l_box_banned.bind('<Return>', deleteBanned) # enter deletes text from box

        # RECIPE SEARCH AND PICTURE FRAME
        frame_search_pic = tk.Frame(self,bg=self.BG_COLOR)# MAIN FRAME
        frame_search_pic.grid(row=1, column=1, columnspan=2,)
        lbl_image = tk.Label(frame_search_pic, image=self.image, padx=5, bg=self.BG_COLOR) # DISPLAYS THE IMAGE
        lbl_image.grid(row=0, column=1)
        lbl_image_name = tk.Label(frame_search_pic, bg=self.BG_COLOR, fg='white', text=self.image_name[:25],
                                  font=('Times New Roman', 10)) # IMAGE NAME TEXT
        lbl_image_name.grid(row=0, column=1, sticky='se')
        l_box_search = tk.Listbox(frame_search_pic, width=50) # DISPLYS SEARCH RESULTS
        l_box_search.grid(row=0, column=0, padx=2)
        l_box_search.bind('<Double-1>', recipeSelect) # DOUBLE CLICK OPENS RECIPE PAGE
        l_box_search.bind('<Return>', recipeSelect) # PRESS ENTER TO OPEN RECIPE PAGE

        # CHECK BOX FRAME
        frame_toggles = tk.Frame(self,bg=self.BG_COLOR) # MAIN FRAME
        frame_toggles.grid(row=2, column=1,pady=4)
        recipe_toggle = tk.IntVar()  # tracks if toggle is selected
        chk_bx_recipe_id = tk.Checkbutton(frame_toggles, text='Recipe #',
                                       variable=recipe_toggle, bg=self.BG_COLOR, fg='white',
                                       command=lambda: checkBoxControl(chk_bx_recipe_id)) # FILTER RECIPES BY RECIPE ID
        chk_bx_recipe_id.grid(row=0, column=1, padx=5)
        title_toggle = tk.IntVar()  # tracks if toggle is selected
        chk_bx_name = tk.Checkbutton(frame_toggles, text='Name',
                                      variable=title_toggle, bg=self.BG_COLOR, fg='white',
                                      command=lambda: checkBoxControl(chk_bx_name)) # FILTER RECIPES BY RECIPE NAME
        chk_bx_name.grid(row=0, column=0, padx=5)
        ingred_toggle = tk.IntVar()  # tracks if toggle is selected
        chk_bx_ingred = tk.Checkbutton(frame_toggles, text='Ingredients',
                                       variable=ingred_toggle, bg=self.BG_COLOR, fg='white',
                                       command=lambda: checkBoxControl(chk_bx_ingred)) # FILTER RECIPES BY INGREDIENT
        chk_bx_ingred.grid(row=0, column=2, padx=5)
        instrs_toggle = tk.IntVar()  # tracks if toggle is selected
        chk_bx_instrs = tk.Checkbutton(frame_toggles, text='Steps', bg=self.BG_COLOR, fg='white',
                                       variable=instrs_toggle, command=lambda: checkBoxControl(chk_bx_instrs)) # FILTER RECIPES BY INSTRUCTION
        chk_bx_instrs.grid(row=0, column=3, padx=5)

        # SEARCH BAR FRAME
        frame_entry_w_btn = tk.Frame(self,bg=self.BG_COLOR) # MAIN FRAME
        frame_entry_w_btn.grid(row=3, column=1,pady=4)
        btn_delete = tk.Button(frame_entry_w_btn, text='Delete',bg=self.BG_COLOR,fg='white',command=deleteRecipe)  # deletes recipe from database
        btn_delete.grid(row=0, column=0,padx=4)
        entry_search_text = tk.Entry(frame_entry_w_btn) # USER ENTRY TEXT BOX
        entry_search_text.grid(row=0, column=1, padx=4)
        entry_search_text.bind('<Return>', search) # PRESS ENTER TO SEARCH DATABASE BY KEYWORD
        btn_entry = tk.Button(frame_entry_w_btn, text='Enter',bg=self.BG_COLOR,fg='white',command=search) # SEARCH DATABASE BY KEYWORD
        btn_entry.grid(row=0, column=2,padx=4)

        # ACTION BUTTONS FRAME
        frame_side_btns = tk.Frame(self,bg=self.BG_COLOR) # MAIN FRAME
        frame_side_btns.grid(row=3, column=2)
        btn_go = tk.Button(frame_side_btns, text='Go', bg=self.BG_COLOR,fg='white',
                           command=lambda: recipeSelect(event=None)) # OPEN SELECTED RECIPE
        btn_go.grid(row=0, column=0,padx=3)
        btn_random = tk.Button(frame_side_btns, text='Random',bg=self.BG_COLOR,fg='white',
                               command=randomRecipe) # OPEN A RANDOM RECIPE FROM ENTIRE DATABASE
        btn_random.grid(row=0, column=1,padx=3)
        btn_favorites = tk.Button(frame_side_btns,text='Favs',bg=self.BG_COLOR,fg='white',
                                  command=getFavs) # DISPLAYS FAVORITE RECIPES
        btn_favorites.grid(row=0,column=2,padx=3)

        # SPACER FRAME (NO ITEMS)
        frame_filler = tk.Frame(self,bg=self.BG_COLOR) # MAIN FRAME / INBETWEEN IMAGE AND BOTTOM BUTTONS
        frame_filler.grid(row=2,column=2)
#----------------------------------------------------------------------
        search()  # LOAD RECIPES IN SEARCH BOX WHEN PAGE IS BUILT