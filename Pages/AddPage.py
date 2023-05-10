"""ADD RECIPE PAGE"""

import tkinter as tk
import pprint as pp
from tkinter import scrolledtext
from Widgets import NavBar
from Functions import db_query_functions as dFuncs

# todo - make pop ups or move on to Search Page

class Add(
    tk.Frame):

    def __init__(self, parent, controller, page_info):
        tk.Frame.__init__(self, parent)
        self.BG_COLOR = page_info['bg_color'] # page background color
        db_conn_str = page_info['db_conn']
        self.config(bg=self.BG_COLOR) # set background to color
        # FUNCTIONS

        def addIngred(event):
            """save ingredient to backend user ingredient list and onscreen listbox"""
            user_ingred = entry_recipe_ingred.get().strip().lower() # user input
            if user_ingred: # if entry isnt blank
                if len(user_ingred) < 100 and str(user_ingred):  # limit amount of data user can input
                    if str(user_ingred) not in l_box_ingreds.get(0, tk.END): # if ingredient not already added to onscreen list
                        l_box_ingreds.insert(tk.END, str(user_ingred))  # add to listbox
                        entry_recipe_ingred.delete(0, tk.END)  # clear entry text box
                    else:  # ingredient already in list
                        pass
                        # pass error message str  to show in pop up later
                else:  # too many characters entered
                    pass
                    # pass error message str  to show in pop up later

        def deleteIngred():
            """remove saved ingredient from onscreen listbox"""
            try:
                l_box_ingreds.delete(l_box_ingreds.curselection()[0])  # delete selected item
            except IndexError:  # delete button is pressed and no item is selected
                pass

        def addInstrs(event):
            """add instructions step onscreen listbox"""
            user_instrs = entry_recipe_instrs.get().strip().lower()  # user input
            if user_instrs: # if entry isnt blank
                if len(user_instrs) <= 250:  # limit amount of data user can input
                    if str(user_instrs) not in l_box_instrs.get(0, tk.END): # instruction not already added
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
            """add user recipe to database"""
            error_message = 'ERROR ADDING RECIPE: '
            message_start_len = len(error_message) # track if error found
            try:

                recipe_name = entry_recipe_name.get() # get recipe name (not null)
                recipe_ingreds = l_box_ingreds.get(0, tk.END)  # get all ingredients (not null)
                recipe_instrs = l_box_instrs.get(0, tk.END)  # get all instructions (not null)

                if not recipe_name: # recipe name blank
                    error_message += 'RECIPE NAME BLANK/ '
                if len(recipe_ingreds) == 0: # no ingredients in list
                    error_message += 'RECIPE INGREDIENTS BLANK/ '
                if len(recipe_instrs) == 0: # no instructions in list
                    error_message += 'RECIPE INSTRUCTIONS BLANK/ '
                if len(error_message) == message_start_len: # if error message has same amount of chars at start, no required user input is blank
                    recipe_cooktime = entry_recipe_ck_time.get()  # get the cooktime (can be null)
                    recipe_comment = entry_recipe_notes.get('1.0', tk.END)[:-1].strip() # get the notes/ comment (can be null)
                    recipe_instrs = '. '.join(recipe_instrs) # change to string to store in database
                    # REMEMBER TO SET FAVORITE TO TRUE HERE TOO
                    #recipe_info = {'name':recipe_name,'ingred': recipe_ingreds, 'instrs':recipe_instrs,
                    #               'cktime': recipe_cooktime, 'comment':recipe_comment, 'favorite':True}
                    #pp.pprint(recipe_info)
                    try:
                        dFuncs.addRecipe(db_connection=db_conn_str,recipe_name=recipe_name,
                                     instructions=recipe_instrs, ingredients=recipe_ingreds,
                                     cook_time_minutes=recipe_cooktime,comment=recipe_comment)# add recipe to database
                    except Exception as e:
                        print(e)
                else: # show pop-up for empty required fields
                    raise EntryError(error_message)


            except EntryError as e:
                # show message that recipe not added / show which field was invalid
                print(e)

        class EntryError(Exception):
            """invalid USER INPUT error"""
            pass
        # FRAMES

        frame_entries = tk.Frame(self, padx=0, pady=0,bg=self.BG_COLOR) # main frame used to store entry frames
        frame_entries.grid(row=1, column=0,columnspan=2)
        frame_entries_left = tk.Frame(frame_entries,padx=5,bg=self.BG_COLOR) # left column entry frames
        frame_entries_left.grid(row=0,column=0)
        frame_entries_right = tk.Frame(frame_entries,padx=5,pady=5,bg=self.BG_COLOR) # right column entry frames
        frame_entries_right.grid(row=0,column=1)
        NavBar.NavBar(self, controller, 6, self.BG_COLOR, ('help', 'search', 'home', 'quit')) # navigation frame / buttons

        frame_display = tk.Frame(self, padx=0, pady=0,bg=self.BG_COLOR) # holds ingredients/instructions display frames
        frame_display.grid(row=1, column=3,columnspan=4)
        frame_display_left = tk.Frame(frame_display,bg=self.BG_COLOR) # ingredients label and frame display
        frame_display_left.grid(row=0,column=0,columnspan=2)
        frame_display_right = tk.Frame(frame_display,padx=5,pady=5,bg=self.BG_COLOR) # # instructions label and frame display
        frame_display_right.grid(row=0,column=2,columnspan=2)


        #  TEXT ENTRIES
        entry_recipe_name = tk.Entry(frame_entries_left) # recipe name input box
        entry_recipe_name.grid(row=1, column=0, pady=1)

        entry_recipe_ck_time = tk.Entry(frame_entries_right, width=4) # cook time input box
        entry_recipe_ck_time.grid(row=1, column=0, pady=1)

        entry_recipe_ingred = tk.Entry(frame_entries_right) # ingredients input box
        entry_recipe_ingred.grid(row=3, column=0, pady=1)
        entry_recipe_ingred.bind('<Return>', addIngred)  # add ingredient to display when enter is pressed

        entry_recipe_instrs = tk.Entry(frame_entries_right)  # instructions input box
        entry_recipe_instrs.grid(row=5, column=0, pady=1)
        entry_recipe_instrs.bind('<Return>', addInstrs)  # add instruction to display when enter is pressed

        # SCROLLED TEXT
        entry_recipe_notes = scrolledtext.ScrolledText(frame_entries_left,
                                                       wrap=tk.WORD, width=25, height=4,
                                                       font=("Times New Roman", 10)) # note/comment input scroll box
        entry_recipe_notes.grid(row=3, column=0, pady=1)

        # BUTTON
        btn_save = tk.Button(self, text='save', bg=self.BG_COLOR,fg='white',command=addRecipe) # add recipe to database
        btn_save.grid(row=0, column=0)
        btn_minus_ingred = tk.Button(frame_display_left, text='X', bg=self.BG_COLOR,fg='white',command=deleteIngred) # delete ingredient from display
        btn_minus_ingred.grid(row=1, column=1)
        btn_minus_instrs = tk.Button(frame_display_right, text='X', bg=self.BG_COLOR, fg='white',command=deleteInstr) # delete instruction from display
        btn_minus_instrs.grid(row=1, column=3)


        # LIST-BOXES
        l_box_ingreds = tk.Listbox(frame_display_left) # displays user ingredients inputs
        l_box_ingreds.grid(row=1, column=0)
        l_box_instrs = tk.Listbox(frame_display_right) # displays user instructions inputs
        l_box_instrs.grid(row=1, column=2)

        # LABELS
        lbl_recipe_name = tk.Label(frame_entries_left, text='Name',bg=self.BG_COLOR,fg='white') # recipe name label
        lbl_recipe_name.grid(row=0, column=0)

        lbl_recipe_ingreds = tk.Label(frame_entries_right, text='Ingredients',bg=self.BG_COLOR,fg='white') # recipe ingredients label
        lbl_recipe_ingreds.grid(row=2, column=0)

        lbl_recipe_ctime = tk.Label(frame_entries_right, text='Cooktime(mins)',bg=self.BG_COLOR,fg='white') # recipe cook time label
        lbl_recipe_ctime.grid(row=0, column=0)

        lbl_recipe_instrs = tk.Label(frame_entries_right, text='Instructions',bg=self.BG_COLOR,fg='white') # recipe instructions label
        lbl_recipe_instrs.grid(row=4, column=0)

        lbl_recipe_notes = tk.Label(frame_entries_left, text='Notes',bg=self.BG_COLOR,fg='white') # recipe notes label
        lbl_recipe_notes.grid(row=2, column=0)

        lbl_ingreds_title = tk.Label(frame_display_left, text='Ingredients',bg=self.BG_COLOR,fg='white') # ingredients display label
        lbl_ingreds_title.grid(row=0, column=0)

        lbl_instrs_title = tk.Label(frame_display_right, text='Instructions',bg=self.BG_COLOR,fg='white') # instructions display label
        lbl_instrs_title.grid(row=0, column=2)