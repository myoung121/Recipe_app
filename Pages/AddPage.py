"""ADD RECIPE PAGE"""

import tkinter as tk
import pprint as pp
from tkinter import scrolledtext
from Pages import HelpPage
import  application as app

class Add(
    tk.Frame):

    def __init__(self, parent, controller, navigation_dict):
        tk.Frame.__init__(self, parent)
        self.config(bg=app.BG_COLOR)
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
            recipe_ingreds = l_box_ingreds.get(0, tk.END)
            recipe_instrs = l_box_instrs.get(0, tk.END)
            recipe_cooktime = entry_recipe_ck_time.get()
            recipe_comment = entry_recipe_notes.get('1.0', tk.END)
            # REMEMBER TO SET FAVORITE TO TRUE HERE TOO
            not_null_info = (recipe_name, recipe_ingreds, recipe_instrs, recipe_cooktime, recipe_comment)
            pp.pprint(not_null_info)
            pass

        # FRAMES

        frame_entries = tk.Frame(self, padx=0, pady=0,bg=app.BG_COLOR)
        frame_entries.grid(row=1, column=0,columnspan=2)
        frame_entries_left = tk.Frame(frame_entries,padx=5,bg=app.BG_COLOR)
        frame_entries_left.grid(row=0,column=0)
        frame_entries_right = tk.Frame(frame_entries,padx=5,pady=5,bg=app.BG_COLOR)
        frame_entries_right.grid(row=0,column=1)

        frame_navigation = tk.Frame(self, padx=0, pady=0,bg=app.BG_COLOR)
        frame_navigation.grid(row=0, column=6)

        frame_ingred_display = tk.Frame(self, padx=0, pady=0,bg=app.BG_COLOR)
        frame_ingred_display.grid(row=1, column=3,columnspan=4)
        frame_ingred_display_left = tk.Frame(frame_ingred_display,bg=app.BG_COLOR)
        frame_ingred_display_left.grid(row=0,column=0,columnspan=2)
        frame_ingred_display_right = tk.Frame(frame_ingred_display,padx=5,pady=5,bg=app.BG_COLOR)
        frame_ingred_display_right.grid(row=0,column=2,columnspan=2)
        # frame_add_minus_ingred = tk.LabelFrame(frame_ingred_display, text='+-btns', padx=4, pady=5)
        # frame_add_minus_ingred.grid(row=1, column=1,rowspan=4)

        #  TEXT ENTRIES
        entry_recipe_name = tk.Entry(frame_entries_left)
        entry_recipe_name.grid(row=1, column=0, pady=1)

        entry_recipe_ingred = tk.Entry(frame_entries_right)
        entry_recipe_ingred.grid(row=3, column=0, pady=1)
        entry_recipe_ingred.bind('<Return>', addIngred)  # add ingredient when enter is pressed

        entry_recipe_ck_time = tk.Entry(frame_entries_right, width=4)
        entry_recipe_ck_time.grid(row=1, column=0, pady=1)

        entry_recipe_instrs = tk.Entry(frame_entries_right)  # needs to be a text box
        entry_recipe_instrs.grid(row=5, column=0, pady=1)
        entry_recipe_instrs.bind('<Return>', addInstrs)  # add instruction step when enter is pressed

        # SCROLLED TEXT
        entry_recipe_notes = scrolledtext.ScrolledText(frame_entries_left,
                                                       wrap=tk.WORD, width=25, height=4,
                                                       font=("Times New Roman", 10))
        entry_recipe_notes.grid(row=3, column=0, pady=1)

        # BUTTON

        btn_save = tk.Button(self, text='save', command=addRecipe)
        btn_save.grid(row=0, column=0)

        btn_help = tk.Button(frame_navigation, text='help', command=lambda: HelpPage.Help())
        btn_help.grid(row=0, column=0)
        btn_search = tk.Button(frame_navigation, text='search', command=lambda: controller.show_frame(navigation_dict['search']))
        btn_search.grid(row=0, column=1, padx=0)
        btn_home = tk.Button(frame_navigation, text='home', command=lambda: controller.show_frame(navigation_dict['home']))
        btn_home.grid(row=0, column=2)
        btn_quit = tk.Button(frame_navigation, text='quit', command=lambda: exit('QUIT'))
        btn_quit.grid(row=0, column=3)

        btn_minus_ingred = tk.Button(frame_ingred_display_left, text='-', command=deleteIngred)
        btn_minus_ingred.grid(row=1, column=1)
        btn_minus_instrs = tk.Button(frame_ingred_display_right, text='-', command=deleteInstr)
        btn_minus_instrs.grid(row=1, column=3)

        # LISTBOX
        l_box_ingreds = tk.Listbox(frame_ingred_display_left)
        l_box_ingreds.grid(row=1, column=0)
        l_box_instrs = tk.Listbox(frame_ingred_display_right)
        l_box_instrs.grid(row=1, column=2)

        # LABEL
        lbl_recipe_name = tk.Label(frame_entries_left, text='Name')
        lbl_recipe_name.grid(row=0, column=0)
        lbl_recipe_ingreds = tk.Label(frame_entries_right, text='Ingredients')
        lbl_recipe_ingreds.grid(row=2, column=0)
        # lbl_blank = tk.Label(frame_entries)
        # lbl_blank.grid(row=3, column=0, pady=20)
        lbl_recipe_ctime = tk.Label(frame_entries_right, text='Cooktime(mins)')
        lbl_recipe_ctime.grid(row=0, column=0)
        lbl_recipe_instrs = tk.Label(frame_entries_right, text='Instructions')
        lbl_recipe_instrs.grid(row=4, column=0)
        lbl_recipe_notes = tk.Label(frame_entries_left, text='Notes')
        lbl_recipe_notes.grid(row=2, column=0)
        lbl_ingreds_title = tk.Label(frame_ingred_display_left, text='Ingredients')
        lbl_ingreds_title.grid(row=0, column=0)
        lbl_instrs_title = tk.Label(frame_ingred_display_right, text='Instructions')
        lbl_instrs_title.grid(row=0, column=2)