import logging
import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk
from Pages import HomePage,SearchPage, AddPage
import pprint as pp


log = logging.getLogger(__name__)
test_db_str = './food_stuff_tester.db' # database connection path
home_pic_location = './food images/beef-gulasch-356793.jpg'
search_pic_location = './food images/egg-shop-fried-chicken.jpg'

# track how many windows open
MAX_OPEN_RECIPES = 3
# this tracks open recipe windows by name as key and image as value(images had to be avail in this file)
open_recipes = {}
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
                self.geometry('800x500')
                # creating a container
                container = tk.Frame(self)
                container.pack(side="top", fill="both", expand=True)

                container.grid_rowconfigure(0, weight=1)
                container.grid_columnconfigure(0, weight=1)
                home_nav = {'search':SearchPage.Search,'add':AddPage.Add,'help':Help,'pic':home_pic_location}
                search_nav = {'help':Help,'add':AddPage.Add,'home':HomePage.Home,
                              'pic':search_pic_location,'db_str':test_db_str,
                              'open_pages':open_recipes,'max_pages':MAX_OPEN_RECIPES}
                add_nav = {'help':Help,'home':HomePage.Home,}
                self.frames = self.makeFrames((HomePage.Home, SearchPage.Search, AddPage.Add),
                                              (home_nav,search_nav,add_nav),parent=container)

                # start on the home page
                self.show_frame(HomePage.Home)
                self.title('RecipeApp 1.0')

            # to display the current frame passed as parameter
            def show_frame(self, cont):
                frame = self.frames[cont]
                frame.tkraise()


        # --------------------------------------------------------------------------------------------------------------------------------------------------------

        class Help(tk.Frame):
            pass

        # Driver Code
        app = tkinterApp()
        app.mainloop()