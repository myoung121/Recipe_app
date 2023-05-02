"""HOME PAGE"""
# todo - move nav buttons to top right like on other scrrens and have slideshow of random images below
import tkinter as tk
from PIL import Image, ImageTk
from Pages import HelpPage
class Home(tk.Frame):
    def __init__(self, parent, controller, navigation_pages:dict):
        self.PAGE_NAME = 'HOME'
        # parent is the root window
        # controller switches the pages
        # navigation_pages are the pages user can go to from this page( format {'Home':frame_obj}
        global home_photo
        pic_location = navigation_pages['pic'] # save copy of image
        del navigation_pages['pic'] # delete image from navigation buttons list
        tk.Frame.__init__(self, parent)

        # FRAME
        frame_pic = tk.Frame(self)
        frame_pic.grid(row=1, column=0)
        frame_btn = tk.Frame(self)
        frame_btn.grid(row=2, column=0, padx=0, pady=0)

        #  LABELS
        image = Image.open(pic_location)
        home_photo = ImageTk.PhotoImage(image)
        lbl_pic = tk.Label(frame_pic, image=home_photo)
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