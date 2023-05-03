"""HOME PAGE"""
# todo - move nav buttons to top right like on other scrrens and have slideshow of random images below
import tkinter as tk
from PIL import Image, ImageTk

import application as app
from Pages import HelpPage
from Functions import db_query_functions as dbFuncs
class Home(tk.Frame):
    def __init__(self, parent, controller, navigation_pages:dict):
        self.PAGE_NAME = 'HOME'
        # parent is the root window
        # controller switches the pages
        # navigation_pages are the pages user can go to from this page and other args needed( format {'Home':frame_obj}
        tk.Frame.__init__(self, parent)
        # get a background image
        print('Home BackGround ', end='')
        bkrnd_image_info = dbFuncs.getImageRandom(app.test_db_str,screen_sized=True,screen_w_h=(app.WINDOW_WIDTH,app.WINDOW_HEIGHT))[0]
        self.bkrnd_image_name = bkrnd_image_info[0]
        self.bkrnd_image = bkrnd_image_info[1]
#-------------------------------------------------------
        # CANVAS

        # BACKGROUND CANVAS
        #canvas_bg = tk.Canvas(self,width=app.WINDOW_WIDTH,height=app.WINDOW_HEIGHT)
        #canvas_bg.pack(fill='both',expand=True)
        # set image in canvas
        #canvas_bg.create_image(0,0,image=self.bkrnd_image,anchor='nw')

        # FRAME
        frame_pic = tk.Frame(self)
        frame_pic.grid(row=1, column=0)
        frame_btn = tk.Frame(self)
        frame_btn.grid(row=2, column=0, padx=0, pady=0)

        #  LABELS
        print('Home Page ',end='')
        image_info = dbFuncs.getImageRandom(app.test_db_str)[0]
        self.image_name = image_info[0]
        self.image = image_info[1]
        lbl_pic = tk.Label(frame_pic, image=self.image)
        lbl_pic.pack()
        lbl_title = tk.Label(self, text='welcome to cookbook app')
        lbl_title.grid(row=0, column=0)

        # BUTTONS
        # navigation buttons
        btn_search = tk.Button(frame_btn, text='search', command=lambda: controller.show_frame(navigation_pages['search']))
        btn_search.grid(row=1, column=0, padx=5)
        btn_add = tk.Button(frame_btn, text='add', command=lambda: controller.show_frame(navigation_pages['add']))
        btn_add.grid(row=1, column=1, padx=5)
        btn_help = tk.Button(frame_btn, text='help', command=lambda: HelpPage.Help())
        btn_help.grid(row=1, column=2, padx=5)
        btn_quit = tk.Button(frame_btn, text='quit',command=lambda:exit('QUIT'))
        btn_quit.grid(row=1, column=3, padx=5)