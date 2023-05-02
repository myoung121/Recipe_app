"""SEARCH PAGE"""
import tkinter as tk
from tkinter import messagebox
import pprint as pp
from PIL import Image, ImageTk
from Functions import db_query_functions
from Pages import RecipePage, HelpPage


class Search(tk.Frame):
    rows = []
    user_last_search_str = ''  # users last searched words
    user_last_filter = 'name'  # users last filter applied

    def __init__(self, parent, controller, navigation_dict):
        # dict needs: homePage,helpPage,addPage,pic_location,db_str
        tk.Frame.__init__(self, parent)
        global search_photo
        search_pic_location = navigation_dict['pic']
        test_db_str = navigation_dict['db_str']


        def checkBoxControl(box_var: tk.Checkbutton):  # search page
            """this function makes sure only one check box is selected at a time"""
            chk_boxes = [chk_bx_recipe, chk_bx_title, chk_bx_ingred, chk_bx_instrs]
            chk_boxes = [x for x in chk_boxes if x != box_var]
            for x in chk_boxes:
                if x:
                    x.deselect()
            box_var.select()

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
                rows = db_query_functions.getRowsFiltered(search_txt='', db_connection_str=test_db_str,
                                                          user_filter=checkBoxStatus(),
                                                          return_all=True)  # return all recipes
            else:
                rows = db_query_functions.getRowsFiltered(search_txt=entry_search_text.get(),
                                                          db_connection_str=test_db_str,
                                                          user_filter=checkBoxStatus())  # return filtered recipes
            # Add items to the search listbox
            for item in rows:
                l_box_search.insert(tk.END, item[:2])
            if entry_search_text.get():
                Search.user_last_search_str = entry_search_text.get()  # save last searched word
                Search.user_last_filter = checkBoxStatus()  # save last used filter
            entry_search_text.delete(0, tk.END)  # clear search box

        def checkPages(name, recipe_pages: dict, max_pages_open):
            can_open = True
            cant_open_str = f'cant open {name} - '
            if name in recipe_pages.keys():  # if recipe page already open or
                can_open = False
                cant_open_str += 'recipe already open/ '
            if len(recipe_pages) == max_pages_open:  # if max number of pages open
                can_open = False
                cant_open_str += 'max number of recipes opened/ close a window to see recipe'
            if not can_open:
                print(cant_open_str)
            return can_open

        def recipeSelect(event):  # search page
            """ opens recipe clicked"""  # opens to recipe screen

            # Get the selected item in the list
            selected_item = l_box_search.curselection()
            # Do something with the selected item
            try:
                selected_recipe = db_query_functions.getRecipeInfo(recipe_id=rows[selected_item[0]][0],
                                                                   db_connection_str=test_db_str)
                # pp.pprint(selected_recipe[0])
                # SET UP RECIPE SCREEN
                # using toplevel screens
                open_recipe_page = checkPages(selected_recipe[0]['name'], navigation_dict['open_pages'],
                                              navigation_dict['max_pages'])  # check if allowed to open a new window
                if open_recipe_page:  # can show recipe
                    recipe_page = RecipePage.Recipe(selected_recipe[0], selected_recipe[1])
                    print('-' * 100)


            except IndexError as e:  # if go button pressed while curser isnt on a recipe
                pass

        def randomRecipe():
            selected_item = db_query_functions.getRecipeInfoRandom(db_connection_str=test_db_str)
            open_recipe_page = checkPages(selected_item[0]['name'], navigation_dict['open_pages'],
                                          navigation_dict['max_pages'])  # check if allowed to open a new window
            if open_recipe_page:  # can show recipe
                recipe_page = RecipePage.Recipe(selected_item[0], selected_item[1])
                print('-' * 100)


        def deleteRecipe():
            selected_item = l_box_search.curselection()
            print(selected_item, '<-----------------')
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
                    print(f'DELETING RECIPE_ID {recipe_db_id}')
                    db_query_functions.deleteRecipe(recipe_id=int(recipe_db_id),
                                                    db_connection_str=test_db_str)  # delete recipe from db
                    rows.pop(selected_item[0])  # delete recipe from stored recipe search
                    l_box_search.delete(selected_item[0])  # delete recipe from listbox
            except IndexError as e:  # if delete button pressed while curser isnt on a recipe
                print(e)
                pass

        # --------------------------------------------------------------------------------------
        # FRAME

        frame_navigate = tk.LabelFrame(self, text='navigation')
        frame_navigate.grid(row=0, column=2)

        frame_banned_ingreds = tk.LabelFrame(self, text='banned ingreds')
        frame_banned_ingreds.grid(row=1, column=0)

        frame_search_pic = tk.LabelFrame(self, text='search/pic')
        frame_search_pic.grid(row=1, column=1, columnspan=2)

        frame_toggles = tk.LabelFrame(self, text='toggles')
        frame_toggles.grid(row=2, column=1)

        frame_entry_w_btn = tk.LabelFrame(self, text='search box/btn')
        frame_entry_w_btn.grid(row=3, column=1)  # ,columnspan=2)

        frame_side_btns = tk.LabelFrame(self, text='side btns')
        frame_side_btns.grid(row=2, column=2)

        # BUTTONS
        btn_help = tk.Button(frame_navigate, text='help', command=lambda: HelpPage.Help())
        btn_help.grid(row=0, column=0)
        btn_add = tk.Button(frame_navigate, text='add', command=lambda: controller.show_frame(navigation_dict['add']))
        btn_add.grid(row=0, column=1)
        btn_home = tk.Button(frame_navigate, text='home', command=lambda: controller.show_frame(navigation_dict['home']))
        btn_home.grid(row=0, column=2)
        btn_quit = tk.Button(frame_navigate, text='quit', command=lambda: exit('QUIT'))
        btn_quit.grid(row=0, column=3)

        btn_banned = tk.Button(frame_banned_ingreds, text='+')
        btn_banned.grid(row=0, column=1)

        btn_go = tk.Button(frame_side_btns, text='go', command=lambda: recipeSelect(event=None))
        btn_go.grid(row=0, column=0)
        btn_random = tk.Button(frame_side_btns, text='random', command=randomRecipe)
        btn_random.grid(row=0, column=1)
        btn_favorites = tk.Button(frame_side_btns,text='favs')
        btn_favorites.grid(row=0,column=2)

        btn_entry = tk.Button(frame_entry_w_btn, text='enter', command=search)
        btn_entry.grid(row=0, column=1)
        # confirm before deleting
        btn_delete = tk.Button(self, text='delete', command=deleteRecipe)  # deletes recipe from database
        btn_delete.grid(row=2, column=0)

        # LABEL
        lbl_banned = tk.Label(frame_banned_ingreds,
                              text=f'{"*" * 10}\nbanned\ningrdients\ngo\nhere\n^\n|\n{"*" * 10}')
        lbl_banned.grid(row=1, column=1, columnspan=2)

        image = Image.open(search_pic_location)
        search_photo = ImageTk.PhotoImage(image)
        lbl_pic = tk.Label(frame_search_pic, image=search_photo)
        lbl_pic.grid(row=0, column=1)

        lbl_btm_blank = tk.Label(frame_side_btns, text='')
        lbl_btm_blank.grid(row=0, column=1, padx=15)

        # LISTBOX
        l_box_search = tk.Listbox(frame_search_pic)
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
                                       variable=recipe_toggle, command=lambda: checkBoxControl(chk_bx_recipe))
        chk_bx_recipe.grid(row=0, column=1, padx=5)

        title_toggle = tk.IntVar()
        chk_bx_title = tk.Checkbutton(frame_toggles, text='name',
                                      variable=title_toggle, command=lambda: checkBoxControl(chk_bx_title))
        chk_bx_title.grid(row=0, column=0, padx=5)
        chk_bx_title.select()  # this box is selected by default

        ingred_toggle = tk.IntVar()
        chk_bx_ingred = tk.Checkbutton(frame_toggles, text='ingredient',
                                       variable=ingred_toggle, command=lambda: checkBoxControl(chk_bx_ingred))
        chk_bx_ingred.grid(row=0, column=2, padx=5)

        instrs_toggle = tk.IntVar()
        chk_bx_instrs = tk.Checkbutton(frame_toggles, text='instruction',
                                       variable=instrs_toggle, command=lambda: checkBoxControl(chk_bx_instrs))
        chk_bx_instrs.grid(row=0, column=3, padx=5)

        search()  # loads all recipes into  search box