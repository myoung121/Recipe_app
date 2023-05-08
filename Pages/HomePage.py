"""HOME PAGE"""
from Widgets import NavBar
import tkinter as tk
from Functions import db_query_functions as dbFuncs

class Home(tk.Frame):
    def __init__(self, parent, controller, page_info:dict):
        self.PAGE_NAME = 'HOME'
        # parent is the root window
        # controller switches the pages
        # page_info  is the information and data needed build the page ex: colors, db location, other pages
        tk.Frame.__init__(self, parent)
        self.images = {} # store images
        self.image_frames={} # store image frames
        self.image_labels = {} # store image labels
        self.BG_COLOR = page_info['bg_color'] # page background color
        db_conn_str = page_info['db_str'] # database location / connection
        self.config(bg=self.BG_COLOR) # set page background to the background color
        self.width = int(page_info['win_size'].split('x')[0]) # get window width
        NUM_IMAGES = 3 # number of images to show on this page
#-------------------------------------------------------
        # FRAME
        frame_images = tk.Frame(self,padx=2,bg=self.BG_COLOR,width=self.width) # used as the main frame that holds the images in frames
        frame_images.grid(row=1,column=0,columnspan=3)
        #  LABELS
        lbl_title = tk.Label(self, text='cookbook app'.upper(),bg=self.BG_COLOR,fg='white') # welcome message
        lbl_title.grid(row=0, column=1)
        NavBar.NavBar(self,controller,2,self.BG_COLOR,('help','search','add','quit'))  # navigation frame / buttons


        all_images_info = dbFuncs.getImageRandom(db_conn_str,num_of_images=NUM_IMAGES) # all random image names and images


        for num,i in enumerate(all_images_info): # attach images to page for all frames
            image_frame_text = all_images_info[num][0].replace("_"," ")
            if len(image_frame_text) > 30: # only show 30 chars
                image_frame_text = image_frame_text[:27] + '...' # change last 3 letter to show name is longer
            self.image_frames[f'frame{str(num)}'] = tk.LabelFrame(frame_images, text=f'{image_frame_text}',
                                                                  bg=self.BG_COLOR,fg='white',border=False,labelanchor='s') # make a frame for each image
            self.image_frames[f'frame{str(num)}'].grid(row=1, column=num)  # add image frames to main frame

            self.images[f'image{str(num)}'] = i[1] # add image to image dict
            self.image_labels[f'label{num}'] = tk.Label(self.image_frames[f'frame{str(num)}'],
                                                     image=self.images[f'image{str(num)}'], padx=5) # add images to a label
            self.image_labels[f'label{num}'].grid(row=0, column=0) # add the labels with images to the frame
