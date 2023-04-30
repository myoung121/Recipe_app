import logging
import tkinter as tk
from tkinter import messagebox, scrolledtext

from PIL import Image, ImageTk

from Pages import RecipePage
from Functions import db_query_functions
import sqlite3
import pprint as pp


log = logging.getLogger(__name__)
test_db_str = '../food_stuff_tester.db' # database connection path
LARGEFONT = ("Verdana", 35)

home_pic_location = '../Food Images/beef-gulasch-356793.jpg'
search_pic_location = '../Food Images/egg-shop-fried-chicken.jpg'
recipe_pic_location = '../Food Images/bubble-and-squeak-with-stilton.jpg'
class MyApp:

    @staticmethod
    def run():
        # Runtime code goes here (remove pass)
        class tkinterApp(tk.Tk):
            """ setup main window
            got code from https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/"""
            # global container
            frames = {}

            # __init__ function for class tkinterApp
            def makeFrames(self, list_of_frames, parent):  # build frames dict
                # initializing frames to an empty array
                frame_dict = {}
                # iterating through a tuple consisting
                # of the different page layouts
                for F in list_of_frames:
                    # initializing frame of that object
                    frame = F(parent, self)
                    frame_dict[F] = frame
                    frame.grid(row=0, column=0, sticky="nsew")
                print(frame_dict)
                return frame_dict

            def addFrame(self, new_frame_obj, current_frames, *recipe_args) -> dict:
                container = tk.Frame()
                container.pack(side="top", fill="both", expand=True)
                print(f'before {current_frames}')
                container.grid_rowconfigure(0, weight=1)
                container.grid_columnconfigure(0, weight=1)
                frame = new_frame_obj(self, *recipe_args)
                current_frames['Recipe'] = frame
                print(f'after {current_frames}')
                frame.grid(row=0, column=0, sticky="nsew")
                app.update()
                return frame

            def __init__(self, *args, **kwargs):
                global container
                global frames
                # __init__ function for class Tk
                tk.Tk.__init__(self, *args, **kwargs)

                # creating a container
                container = tk.Frame(self)
                container.pack(side="top", fill="both", expand=True)

                container.grid_rowconfigure(0, weight=1)
                container.grid_columnconfigure(0, weight=1)

                self.frames = self.makeFrames((Home, Search, Add), parent=container)

                # self.show_frame(Home)
                # start on the homescreen
                self.show_frame(Add)

            # to display the current frame passed as
            # parameter
            def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise()

        class Home(tk.Frame):
            # home_pic_location = '../Food Images/beef-gulasch-356793.jpg'

            def __init__(self, parent, controller):
                global home_photo

                tk.Frame.__init__(self, parent)

                # label of frame Layout 2
                # label = ttk.Label(self, text="Home", font=LARGEFONT)
                # FRAME

                frame_pic = tk.Frame(self, padx=0, pady=0)
                frame_pic.grid(row=1, column=0)

                frame_btn = tk.Frame(self, padx=0, pady=0)
                # frame_btn.columnconfigure(3,minsize=frame_width)
                # frame_btn.rowconfigure(5,minsize=frame_height)
                frame_btn.grid(row=2, column=0, padx=0, pady=0)

                # BUTTONS
                btn_search = tk.Button(frame_btn, text='search', command=lambda: controller.show_frame(Search))
                btn_search.grid(row=1, column=0, padx=5)

                btn_add = tk.Button(frame_btn, text='add', command=lambda: controller.show_frame(Add))
                btn_add.grid(row=1, column=1, padx=5)

                btn_help = tk.Button(frame_btn, text='help', command=lambda: controller.show_frame(Help))
                btn_help.grid(row=1, column=2, padx=5)

                btn_quit = tk.Button(frame_btn, text='quit')
                btn_quit.grid(row=1, column=3, padx=5)

                #  LABELS
                # lbl_title = tk.Label(master=window, text='Enter Message Here')
                # lbl_title.pack()
                image = Image.open(home_pic_location)
                home_photo = ImageTk.PhotoImage(image)
                lbl_pic = tk.Label(frame_pic, image=home_photo)
                lbl_pic.pack()

                lbl_title = tk.Label(self, text='welcome to cookbook app')
                lbl_title.grid(row=0, column=0)

        class Search(tk.Frame):
            rows = []
            user_last_search_str = ''  # users last searched words
            user_last_filter = 'name'  # users last filter applied

            def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)
                global search_photo

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

                def recipeSelect(event):  # search page
                    """ opens recipe clicked"""  # opens to recipe screen

                    # Get the selected item in the list
                    selected_item = l_box_search.curselection()
                    print(selected_item, '<-----------------')
                    # Do something with the selected item
                    try:
                        selected_item = db_query_functions.getRecipeInfo(recipe_id=rows[selected_item[0]][0],
                                                                         db_connection_str=test_db_str,
                                                                         unique_ingreds=db_query_functions.getRowsAll(
                                                                             'Ingredient', test_db_str))
                        recipe_info = selected_item[0]
                        image_blob = selected_item[1]
                        pp.pprint(recipe_info)
                        # SET UP RECIPE SCREEN
                        # using toplevl screens so can delete this and make new func to create topscreen
                        recipe_page = app.addFrame(RecipePage.Recipe,app.frames,
                                                 recipe_info['name'],
                                                 recipe_info['ingredients'], recipe_info['instr'],
                                                 recipe_pic_location)
                        print(f'outside addFrame() - {app.frames} <----------')
                        #app.show_frame('Recipe')  # switch to recipe screen
                        print('-' * 100)
                    except IndexError as e:  # if go button pressed while curser isnt on a recipe
                        print(e)
                        pass

                def randomRecipe():
                    selected_item = db_query_functions.getRecipeInfoRandom(
                        num_recipes=len(db_query_functions.getRowsAll('Recipe', test_db_str)),
                        db_connection_str=test_db_str,
                        unique_ingreds=db_query_functions.getRowsAll('Ingredient', test_db_str))
                    recipe_info = selected_item[0]
                    image_blob = selected_item[1]
                    # controller.show_frame(Recipe)  # switch to recipe screen
                    pp.pprint(recipe_info)
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
                btn_help = tk.Button(frame_navigate, text='help', command=lambda: controller.show_frame(Help))
                btn_help.grid(row=0, column=0)
                btn_add = tk.Button(frame_navigate, text='add', command=lambda: controller.show_frame(Add))
                btn_add.grid(row=0, column=1)
                btn_home = tk.Button(frame_navigate, text='home', command=lambda: controller.show_frame(Home))
                btn_home.grid(row=0, column=2)
                btn_quit = tk.Button(frame_navigate, text='quit', command=lambda: exit('QUIT'))
                btn_quit.grid(row=0, column=3)

                btn_banned = tk.Button(frame_banned_ingreds, text='+')
                btn_banned.grid(row=0, column=1)

                btn_go = tk.Button(frame_side_btns, text='go', command=lambda: recipeSelect(event=None))
                btn_go.grid(row=0, column=0)
                btn_random = tk.Button(frame_side_btns, text='random', command=randomRecipe)
                btn_random.grid(row=0, column=1)

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
                # CAN USE chk_bx.deselect() to make sure only on is checked
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

        # -------------

        class Add(
            tk.Frame):  # save butto needs to clear saved_ingreds or old ingreds will still be thr. and make function to clear before leaving add page

            def __init__(self, parent, controller):
                tk.Frame.__init__(self, parent)

                # FUNCTIONS

                def addIngred(event):
                    """save ingredient to backend user ingred list and onscreen listbox"""
                    user_ingred = entry_recipe_ingred.get()  # user input
                    if user_ingred:
                        if len(user_ingred) < 100 and str(user_ingred):  # limit amount of data user can input
                            if str(user_ingred) not in l_box_ingreds.get(0, tk.END):
                                l_box_ingreds.insert(tk.END, str(user_ingred))  # add to listbox
                                entry_recipe_ingred.delete(0, tk.END)  # clear entry text box
                            else:  # ingred already in list
                                pass
                                # pass error message str  to show in pop up later
                        else:  # too many characters entered
                            pass
                            # pass error message str  to show in pop up later

                def deleteIngred():
                    """remove saved ingredient from onscreen listbox"""
                    try:
                        l_box_ingreds.delete(l_box_ingreds.curselection()[0])  # delete selected item
                    except IndexError:  # button is pressed and no item is selected
                        pass

                def addInstrs(event):
                    """add instructions step onscreen listbox"""
                    user_instrs = entry_recipe_instrs.get()  # user input
                    if user_instrs:
                        if len(user_instrs) <= 250 and str(user_instrs):  # limit amount of data user can input
                            if str(user_instrs) not in l_box_instrs.get(0, tk.END):
                                l_box_instrs.insert(tk.END, str(user_instrs))  # add to listbox
                                entry_recipe_instrs.delete(0, tk.END)  # clear entry text box
                            else:  # instr already in list
                                pass
                                # pass error message str  to show in pop up later
                        else:  # too many characters entered
                            pass
                            # pass error message str  to show in pop up later
                def deleteInstr():
                    """remove saved instruction from onscreen listbox"""
                    try:
                        l_box_instrs.delete(l_box_instrs.curselection()[0])  # delete selected item
                    except IndexError:  # button is pressed and no item is selected
                        pass
                def addRecipe():
                    """add user recipe too database"""
                    # remember to validate entry fields before adding to data base
                    recipe_name = entry_recipe_name.get()
                    recipe_ingreds = l_box_ingreds.get(0,tk.END)
                    recipe_instrs = l_box_instrs.get(0,tk.END)
                    recipe_cooktime = entry_recipe_ck_time.get()
                    recipe_comment = entry_recipe_notes.get('1.0',tk.END)
                    # REMEMBER TO SET FAVORITE TO TRUE HERE TOO
                    not_null_info = (recipe_name,recipe_ingreds,recipe_instrs,recipe_cooktime,recipe_comment)
                    pp.pprint(not_null_info)
                    pass

                # FRAMES

                frame_entries = tk.LabelFrame(self, text='entries', padx=0, pady=0)
                frame_entries.grid(row=1, column=0)

                frame_navigation = tk.LabelFrame(self, text='navigation', padx=0, pady=0)
                frame_navigation.grid(row=0, column=1)

                frame_ingred_display = tk.LabelFrame(self, text='ingreds', padx=0, pady=0)
                frame_ingred_display.grid(row=1, column=1)

                #frame_add_minus_ingred = tk.LabelFrame(frame_ingred_display, text='+-btns', padx=4, pady=5)
                #frame_add_minus_ingred.grid(row=1, column=1,rowspan=4)

                #  TEXT ENTRIES
                entry_recipe_name = tk.Entry(frame_entries)
                entry_recipe_name.grid(row=1, column=0, pady=1)

                entry_recipe_ingred = tk.Entry(frame_entries)
                entry_recipe_ingred.grid(row=3, column=0, pady=1)
                entry_recipe_ingred.bind('<Return>', addIngred)  # add ingredient when enter is pressed

                entry_recipe_ck_time = tk.Entry(frame_entries, width=4)
                entry_recipe_ck_time.grid(row=5, column=0, pady=1)

                entry_recipe_instrs = tk.Entry(frame_entries)  # needs to be a text box
                entry_recipe_instrs.grid(row=7, column=0, pady=1)
                entry_recipe_instrs.bind('<Return>', addInstrs)  # add instruction step when enter is pressed

                # SCROLLED TEXT
                entry_recipe_notes = scrolledtext.ScrolledText(frame_entries,
                                                               wrap=tk.WORD, width=25, height=4,
                                                               font=("Times New Roman", 10))
                entry_recipe_notes.grid(row=9, column=0, pady=1)

                # BUTTON

                btn_save = tk.Button(self, text='save',command=addRecipe)
                btn_save.grid(row=2, column=0)

                btn_help = tk.Button(frame_navigation, text='help', command=lambda: controller.show_frame(Help))
                btn_help.grid(row=0, column=0)
                btn_home = tk.Button(frame_navigation, text='home', command=lambda: controller.show_frame(Home))
                btn_home.grid(row=0, column=1)
                btn_quit = tk.Button(frame_navigation, text='quit', command=lambda: exit('QUIT'))
                btn_quit.grid(row=0, column=2)

                btn_minus_ingred = tk.Button(frame_ingred_display, text='-', command=deleteIngred)
                btn_minus_ingred.grid(row=1, column=1)
                btn_minus_instrs = tk.Button(frame_ingred_display,text='-',command=deleteInstr)
                btn_minus_instrs.grid(row=3,column=1)

                # LISTBOX
                l_box_ingreds = tk.Listbox(frame_ingred_display)
                l_box_ingreds.grid(row=1, column=0)
                l_box_instrs = tk.Listbox(frame_ingred_display)
                l_box_instrs.grid(row=3,column=0)

                # LABEL
                lbl_recipe_name = tk.Label(frame_entries, text='recipe name')
                lbl_recipe_name.grid(row=0, column=0)
                lbl_recipe_ingreds = tk.Label(frame_entries, text='recipe ingredients')
                lbl_recipe_ingreds.grid(row=2, column=0)
                # lbl_blank = tk.Label(frame_entries)
                # lbl_blank.grid(row=3, column=0, pady=20)
                lbl_recipe_name = tk.Label(frame_entries, text='recipe cooktime(mins)')
                lbl_recipe_name.grid(row=4, column=0)
                lbl_recipe_instrs = tk.Label(frame_entries, text='recipe instructions')
                lbl_recipe_instrs.grid(row=6, column=0)
                lbl_recipe_notes = tk.Label(frame_entries, text='recipe notes')
                lbl_recipe_notes.grid(row=8, column=0)
                lbl_ingreds_title = tk.Label(frame_ingred_display, text='ingredients')
                lbl_ingreds_title.grid(row=0, column=0)
                lbl_instrs_title = tk.Label(frame_ingred_display, text='instructions')
                lbl_instrs_title.grid(row=2, column=0)

        class Help(tk.Frame):
            pass

        # Driver Code
        app = tkinterApp()
        app.mainloop()