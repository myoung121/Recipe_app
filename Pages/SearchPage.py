"""SEARCH PAGE"""
import tkinter as tk
from tkinter import messagebox
from Functions import db_query_functions as dbFuncs
from Functions import db_query_functions
from Widgets import NavBar

# todo- when opening a newly created recipe  throws error b/c it doesnt have an image. handle errors in the db func calls/ maybe could return a random image instead
class Search(tk.Frame):
    rows = []
    user_last_search_str = ''  # users last searched words
    user_last_filter = 'name'  # users last filter applied

    def __init__(self, parent, controller, page_info):
        # dict needs: homePage,helpPage,addPage,db_str
        tk.Frame.__init__(self, parent)
        self.BG_COLOR =page_info['bg_color']
        self.config(bg=self.BG_COLOR)
        DB_STR = page_info['db_str']
        MAX_PAGES = page_info['max_pages'] # number of pages that can be open at one time
        open_recipe_windows = page_info['open_pages'] # track recipes pages opened
        # get a background image
        def checkBoxControl(box_var: tk.Checkbutton):  # search page
            """this function makes sure only one check box is selected at a time"""
            chk_boxes = [chk_bx_recipe, chk_bx_title, chk_bx_ingred, chk_bx_instrs]
            chk_boxes = [x for x in chk_boxes if x != box_var]
            for x in chk_boxes:
                if x:
                    x.deselect()
                    x.config(fg='white')
            box_var.select()
            box_var.config(fg='green')
        def checkBoxStatus(getToggle: bool = False, toggleKey: str = ''):  # search page
            """this function returns name of which text box is selected or None"""
            chk_boxes = {'recipe_id': recipe_toggle, 'name': title_toggle,
                         'ingredient': ingred_toggle, 'instruction': instrs_toggle}
            for column, boxy in chk_boxes.items():
                if boxy.get():
                    return column
            return None

        def search(event=None):  # search page
            """uses input from search box to get recipes from db"""
            global rows
            l_box_search.delete(0, tk.END)
            if not entry_search_text.get():  # empty entry
                pass
                checkBoxControl(chk_bx_title)  # set default search field to recipe name
                rows = db_query_functions.getFilteredRecipes(search_txt='', db_connection_str=DB_STR,
                                                             user_filter=checkBoxStatus(),
                                                             return_all=True)  # return all recipes
            else:
                rows = db_query_functions.getFilteredRecipes(search_txt=entry_search_text.get(),
                                                             db_connection_str=DB_STR,
                                                             user_filter=checkBoxStatus())  # return filtered recipes
            # Add items to the search listbox
            for item in rows:
                item = list(item)
                item[1]=item[1].replace('_',' ')
                l_box_search.insert(tk.END, f'{item[0]}. {item[1].title()}')
            if entry_search_text.get():
                Search.user_last_search_str = entry_search_text.get()  # save last searched word
                Search.user_last_filter = checkBoxStatus()  # save last used filter
            entry_search_text.delete(0, tk.END)  # clear search box

        def checkPages(name, recipe_pages: list, max_pages_open):
            can_open = True
            cant_open_str = f'cant open {name} - '
            if name in recipe_pages:  # if recipe page already open or
                can_open = False
                cant_open_str += 'recipe already open/ '
            if len(recipe_pages) == max_pages_open:  # if max number of pages open
                can_open = False
                cant_open_str += 'max number of recipes opened/ close a window to see recipe'
            if not can_open:
                print(cant_open_str + ' -F')
            return can_open

        def recipeSelect(event):  # search page
            """ opens recipe clicked"""  # opens to recipe screen

            # Get the selected item in the list
            selected_item = l_box_search.curselection()
            # Do something with the selected item
            try:
                selected_recipe = db_query_functions.getRecipeInfo(recipe_id=rows[selected_item[0]][0],
                                                                   db_connection_str=DB_STR)
                # pp.pprint(selected_recipe[0])
                # SET UP RECIPE SCREEN
                # using toplevel screens
                open_recipe_page = checkPages(selected_recipe[0]['name'], open_recipe_windows,MAX_PAGES)  # check if allowed to open a new window
                if open_recipe_page:  # can show recipe
                    recipe_page = page_info['recipe_page'](selected_recipe[0], selected_recipe[1])
                    open_recipe_windows.append(recipe_page.recipe_name)
                    print(f'opened {recipe_page.recipe_id}-{recipe_page.recipe_name} <-')
            except IndexError as e:  # if go button pressed while curser isnt on a recipe
                pass

        def randomRecipe():
            selected_item = db_query_functions.getRecipeInfoRandom(db_connection_str=DB_STR)
            open_recipe_page = checkPages(selected_item[0]['name'], page_info['open_pages'],
                                          page_info['max_pages'])  # check if allowed to open a new window
            if open_recipe_page:  # can show recipe
                recipe_page = page_info['recipe_page'](selected_item[0], selected_item[1])
                open_recipe_windows.append(recipe_page.recipe_name)
                print(f'opened {recipe_page.recipe_id}-{recipe_page.recipe_name} <-')

        def getFavs():
            """when fav button pressed queries db for favorite recipes and ads to search box"""
            favs = dbFuncs.getFavorites(DB_STR) # get favorite recipes from database
            l_box_search.delete(0, tk.END) # clear the displayed recipes
            for item in favs:
                item = list(item) # change type to edit elements
                item[1]=item[1].replace('_',' ')
                l_box_search.insert(tk.END, f'{item[0]}. {item[1].title()}') # add recipe info to display
        def deleteRecipe():
            selected_item = l_box_search.curselection()
            try:
                recipe_db_id = rows[selected_item[0]][0]
                recipe_name = rows[selected_item[0]][1].replace("_", " ")
                if len(recipe_name) <= 25:
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
                    print(f'deleted {recipe_db_id}-{recipe_name} -X')
            except IndexError as e:  # if delete button pressed while curser isnt on a recipe
                print(e)
                pass
        # --------------------------------------------------------------------------------------

        # FRAME

        NavBar.NavBar(self,controller,2,self.BG_COLOR,('help','add','home','quit'))  # navigation frame / buttons


        frame_banned_ingreds = tk.Frame(self,bg=self.BG_COLOR)
        frame_banned_ingreds.grid(row=1, column=0)

        frame_search_pic = tk.Frame(self,bg=self.BG_COLOR)
        frame_search_pic.grid(row=1, column=1, columnspan=2,)

        frame_toggles = tk.Frame(self,bg=self.BG_COLOR)
        frame_toggles.grid(row=2, column=1)

        frame_entry_w_btn = tk.Frame(self,bg=self.BG_COLOR)
        frame_entry_w_btn.grid(row=3, column=1)  # ,columnspan=2)

        frame_side_btns = tk.Frame(self,bg=self.BG_COLOR)
        frame_side_btns.grid(row=2, column=2)

        # BUTTONS
        btn_banned = tk.Button(frame_banned_ingreds, text='-',bg=self.BG_COLOR,fg='white')
        btn_banned.grid(row=0, column=1)

        btn_go = tk.Button(frame_side_btns, text='go', bg=self.BG_COLOR,fg='white',command=lambda: recipeSelect(event=None))
        btn_go.grid(row=0, column=0)
        btn_random = tk.Button(frame_side_btns, text='random',bg=self.BG_COLOR,fg='white',command=randomRecipe)
        btn_random.grid(row=0, column=1)
        btn_favorites = tk.Button(frame_side_btns,text='favs',bg=self.BG_COLOR,fg='white',command=getFavs)
        btn_favorites.grid(row=0,column=2)

        btn_entry = tk.Button(frame_entry_w_btn, text='enter',bg=self.BG_COLOR,fg='white',command=search)
        btn_entry.grid(row=0, column=1)
        # confirm before deleting
        btn_delete = tk.Button(self, text='delete',bg=self.BG_COLOR,fg='white',command=deleteRecipe)  # deletes recipe from database
        btn_delete.grid(row=2, column=0)

        # LABEL
        lbl_banned = tk.Label(frame_banned_ingreds,
                              text=f'{"*" * 10}\nbanned\ningrdients\ngo\nhere\n^\n|\n{"*" * 10}',padx=5)
        lbl_banned.grid(row=1, column=1, columnspan=2)
        print('Search Page ', end='')
        image_info = dbFuncs.getImageRandom(DB_STR)[0]
        self.image_name = image_info[0]
        self.image = image_info[1]
        lbl_pic = tk.Label(frame_search_pic, image=self.image,padx=5)
        lbl_pic.grid(row=0, column=1)

        lbl_btm_blank = tk.Label(frame_side_btns, text='')
        lbl_btm_blank.grid(row=0, column=1, padx=15)

        # LISTBOX
        l_box_search = tk.Listbox(frame_search_pic,width=50)
        l_box_search.grid(row=0, column=0)
        # Bind selection function to the listbox
        l_box_search.bind('<Double-1>', recipeSelect)
        l_box_search.bind('<Return>', recipeSelect)

        # ENTRY
        entry_search_text = tk.Entry(frame_entry_w_btn)  # needs to be a text box
        entry_search_text.grid(row=0, column=0, pady=0)
        entry_search_text.bind('<Return>', search)

        # CHECKBOX
        recipe_toggle = tk.IntVar()
        chk_bx_recipe = tk.Checkbutton(frame_toggles, text='recipe_id',
                                       variable=recipe_toggle, bg=self.BG_COLOR,fg='white',command=lambda: checkBoxControl(chk_bx_recipe))
        chk_bx_recipe.grid(row=0, column=1, padx=5)

        title_toggle = tk.IntVar()
        chk_bx_title = tk.Checkbutton(frame_toggles, text='name',
                                      variable=title_toggle, bg=self.BG_COLOR,fg='white',command=lambda: checkBoxControl(chk_bx_title))
        chk_bx_title.grid(row=0, column=0, padx=5)
        chk_bx_title.select()  # this box is selected by default

        ingred_toggle = tk.IntVar()
        chk_bx_ingred = tk.Checkbutton(frame_toggles, text='ingredient',
                                       variable=ingred_toggle, bg=self.BG_COLOR,fg='white',command=lambda: checkBoxControl(chk_bx_ingred))
        chk_bx_ingred.grid(row=0, column=2, padx=5)

        instrs_toggle = tk.IntVar()
        chk_bx_instrs = tk.Checkbutton(frame_toggles, text='instruction',bg=self.BG_COLOR,fg='white',
                                       variable=instrs_toggle, command=lambda: checkBoxControl(chk_bx_instrs))
        chk_bx_instrs.grid(row=0, column=3, padx=5)

        search()  # loads all recipes into  search box