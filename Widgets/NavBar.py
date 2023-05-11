"""NAVIGATION BAR USED AT TOP RIGHT OF SCREEN - GOES TO OTHER PAGES/QUIT"""

import tkinter as tk
from Pages import SearchPage,AddPage,HomePage,HelpPage


class NavBar(tk.Frame):
    def __init__(self,parent,controller,start_column:int,bg_color,buttons_used:tuple):
        # parent = frame placed on
        # controller = function to switch between pages
        # start_column = column number the widget starts on / row is always 0
        # bg_color = background color
        # buttons_used = nav buttons used
        super().__init__()
    # BUTTONS


        frame_navigation = tk.Frame(parent)  # used to hold the navigation and quit button
        frame_navigation.grid(row=0, column=start_column)

        for num,button in enumerate(buttons_used):
            button = button.lower()
            # SEARCH
            if button == 'search':
                btn_search = tk.Button(frame_navigation, text='SEARCH', bg=bg_color, fg='white', border=False,
                               command=lambda: controller.show_frame(SearchPage.Search))# goto recipe search page
                btn_search.grid(row=0, column=num, padx=0)
            elif button == 'add':
                # ADD
                btn_add = tk.Button(frame_navigation, text='ADD', bg=bg_color, fg='white', border=False,
                                    command=lambda: controller.show_frame(AddPage.Add))  # goto add recipe page
                btn_add.grid(row=0, column=num, padx=0)
            elif button == 'help':
                # HELP
                btn_help = tk.Button(frame_navigation, text='HELP', bg=bg_color, fg='white', border=False,
                                     command=lambda: HelpPage.Help())  # open help / info pop-up
                btn_help.grid(row=0, column=num, padx=0)
            elif button == 'quit':
                # QUIT
                btn_quit = tk.Button(frame_navigation, text='QUIT', bg=bg_color, fg='red', border=False,
                                     command=lambda: exit('QUIT'))  # quit / close app
                btn_quit.grid(row=0, column=num, padx=0)
            elif button == 'home':
                btn_home = tk.Button(frame_navigation, text='HOME', bg=bg_color, fg='green', border=False,
                                     command=lambda: controller.show_frame(HomePage.Home))
                btn_home.grid(row=0, column=num) # goto home page