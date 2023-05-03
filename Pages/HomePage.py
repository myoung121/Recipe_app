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
        self.images = {}
        self.image_frames={}
        self.image_labels = {}
        NUM_IMAGES = 3
#-------------------------------------------------------
        # CANVAS

        # BACKGROUND CANVAS
        #canvas_bg = tk.Canvas(self,width=app.WINDOW_WIDTH,height=app.WINDOW_HEIGHT)
        #canvas_bg.pack(fill='both',expand=True)
        # set image in canvas
        #canvas_bg.create_image(0,0,image=self.bkrnd_image,anchor='nw')

        # WILL HAVE 3 PICS
        # FRAME
        frame_images = tk.LabelFrame(self,text='images main',padx=2)
        frame_images.grid(row=1,column=0,columnspan=3)
        frame_navigation = tk.Frame(self)
        frame_navigation.grid(row=0, column=2)
        """        frame_img1 = tk.LabelFrame(frame_images,text='pic1')
        frame_img1.grid(row=0,column=0)
        frame_img2= tk.LabelFrame(frame_images,text='pic2')
        frame_img2.grid(row=0,column=1)
        frame_img3= tk.LabelFrame(frame_images,text='pic3')
        frame_img3.grid(row=0,column=2)
"""


        #  LABELS
        lbl_title = tk.Label(self, text='cookbook app'.upper())
        lbl_title.grid(row=0, column=1)
    # make frames for number of images
        for b in range(NUM_IMAGES):
            self.image_frames[f'frame{str(b)}'] = tk.LabelFrame(frame_images,text=f'pic{b}')
            self.image_frames[f'frame{str(b)}'].grid(row=1,column=b)
        # IMAGE LABELS
        # get random images
        print('Home Page ',end='')
        all_images_info = dbFuncs.getImageRandom(app.test_db_str,num_of_images=NUM_IMAGES)
        # attach images to page for all frames
        for num,i in enumerate(all_images_info):
            self.images[f'image{str(num)}'] = i[1]
        for numm,a in enumerate(self.images):
            self.image_labels[f'label{numm}'] =tk.Label(self.image_frames[f'frame{str(numm)}'],
                                                        image=self.images[f'image{str(numm)}'],padx=5)
            self.image_labels[f'label{numm}'].grid(row=0,column=0)


        # BUTTONS
        # navigation buttons
        btn_search = tk.Button(frame_navigation, text='search',
                               command=lambda: controller.show_frame(navigation_pages['search']))
        btn_search.grid(row=0, column=1, padx=0)
        btn_add = tk.Button(frame_navigation, text='add', command=lambda: controller.show_frame(navigation_pages['add']))
        btn_add.grid(row=0, column=2, padx=0)
        btn_help = tk.Button(frame_navigation, text='help', command=lambda: HelpPage.Help())
        btn_help.grid(row=0, column=0, padx=0)
        btn_quit = tk.Button(frame_navigation, text='quit', command=lambda: exit('QUIT'))
        btn_quit.grid(row=0, column=3, padx=0)
        """# FRAME
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
        btn_quit.grid(row=1, column=3, padx=5)"""