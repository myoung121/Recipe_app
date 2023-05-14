"""APPLICATION ROOT WINDOW"""

# skeleton code from https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/
import logging
import os
import tkinter as tk
from Pages import HomePage,SearchPage, AddPage, RecipePage


log = logging.getLogger(__name__)
DB_STR = os.path.join(".", "FOOD_STUFF.db")
WINDOW_TITLE = 'CookBook'
WINDOW_WIDTH = 830 # window width
WINDOW_HEIGHT = 300 # window height
WINDOW_SIZE = f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}' # window size
BG_COLOR = '#242c3f' # app bg color / used by every page and window
MAX_OPEN_RECIPES = 5 # max number of recipe windows that can be open at once
open_recipes = []# this tracks open recipe windows by name as key and image as value(images had to be avail in this file)
class MyApp:
    @staticmethod
    def run():
        class tkinterApp(tk.Tk):
            frames = {}# global container
            def makeFrames(self, list_of_frames, frames_args:tuple,parent):  # build frames dict
                # initializing frames to an empty array
                frame_dict = {}
                # iterating through  page layouts
                for num,F in enumerate(list_of_frames):
                    # initializing frame of that object
                    frame = F(parent, self,frames_args[num])
                    frame_dict[F] = frame
                    frame.grid(row=0, column=0, sticky="nsew")
                return frame_dict

            def __init__(self, *args, **kwargs):
                #global container
                #global frames
                tk.Tk.__init__(self, *args, **kwargs)
                self.geometry(WINDOW_SIZE) # set window size
                self.resizable(width=False,height=False) # lock window size
                self.title(WINDOW_TITLE)  # set window title
                container = tk.Frame(self)# creating a container for frame
                container.pack(side="top", fill="both", expand=True)
                container.grid_rowconfigure(0, weight=1)
                container.grid_columnconfigure(0, weight=1)
                home_info = {'bg_color':BG_COLOR,'db_str':DB_STR,'win_size':WINDOW_SIZE} # info needed to build home page
                search_info = {'bg_color':BG_COLOR,'recipe_page':RecipePage.Recipe,'db_str':DB_STR,'open_pages':open_recipes,
                              'max_pages':MAX_OPEN_RECIPES} # info needed to build search page
                add_info = {'bg_color':BG_COLOR,'win_size':WINDOW_SIZE,'db_conn':DB_STR} # info needed to build add page

                self.frames = self.makeFrames((HomePage.Home, SearchPage.Search, AddPage.Add),
                                              (home_info,search_info,add_info),parent=container) # make the page frame and to the container
                self.show_frame(HomePage.Home) # open to home page when app starts


            def show_frame(self, cont):
                """switches the page frames"""
                frame = self.frames[cont]
                frame.tkraise()

        # Driver Code
        app = tkinterApp()
        app.mainloop()

