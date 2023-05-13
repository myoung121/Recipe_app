import logging
import tkinter as tk
from Pages import HomePage,SearchPage, AddPage, RecipePage


log = logging.getLogger(__name__)
global test_db_str # database connection path
test_db_str = './food_stuff_tester.db'
DB_STR = './food_stuff_tester.db'
WINDOW_WIDTH = 830
WINDOW_HEIGHT = 300
WINDOW_SIZE = f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}'
BG_COLOR = '#242c3f'
MAX_OPEN_RECIPES = 5# track how many windows open
# this tracks open recipe windows by name as key and image as value(images had to be avail in this file)
open_recipes = []
help_open = False # tracks if help page is open
class MyApp:

    @staticmethod
    def run():
        class tkinterApp(tk.Tk):
            """ setup main window
            got code from https://www.geeksforgeeks.org/tkinter-application-to-switch-between-different-page-frames/"""
            # global container
            frames = {}

            # __init__ function for class tkinterApp
            def makeFrames(self, list_of_frames, frames_args:tuple,parent):  # build frames dict
                # initializing frames to an empty array
                frame_dict = {}
                # iterating through a tuple consisting
                # of the different page layouts
                for num,F in enumerate(list_of_frames):
                    # initializing frame of that object
                    frame = F(parent, self,frames_args[num])
                    frame_dict[F] = frame
                    frame.grid(row=0, column=0, sticky="nsew")
                #print(frame_dict)
                return frame_dict

            def __init__(self, *args, **kwargs):
                global container
                global frames
                # __init__ function for class Tk
                tk.Tk.__init__(self, *args, **kwargs)
                self.geometry(WINDOW_SIZE) # set window size
                self.resizable(width=False,height=False) # lock window size
                # creating a container
                container = tk.Frame(self)
                container.pack(side="top", fill="both", expand=True)

                container.grid_rowconfigure(0, weight=1)
                container.grid_columnconfigure(0, weight=1)
                home_nav = {'bg_color':BG_COLOR,'db_str':DB_STR,'win_size':WINDOW_SIZE}
                search_nav = {'bg_color':BG_COLOR,'recipe_page':RecipePage.Recipe,'db_str':test_db_str,'open_pages':open_recipes,
                              'max_pages':MAX_OPEN_RECIPES}
                add_nav = {'bg_color':BG_COLOR,'win_size':WINDOW_SIZE,'db_conn':DB_STR}
                self.frames = self.makeFrames((HomePage.Home, SearchPage.Search, AddPage.Add),
                                              (home_nav,search_nav,add_nav),parent=container)

                # start on the home page
                self.show_frame(HomePage.Home)
                self.title('COOKBOOK')

            # to display the current frame passed as parameter
            def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise()


        # --------------------------------------------------------------------------------------------------------------------------------------------------------



        # Driver Code
        app = tkinterApp()
        app.mainloop()

