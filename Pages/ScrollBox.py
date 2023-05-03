""" Python Program to make a scrollable frame
skeleton from: https://www.geeksforgeeks.org/scrollable-frames-in-tkinter/
"""
import pprint
import tkinter as tk
import  io
from PIL import Image, ImageTk
from Functions import db_query_functions as dbFuncs
class ScrollTextBox(tk.Frame):

    # constructor
    def __init__(self,parent_frame:tk.LabelFrame,text_iter,
                 numbered=True,with_canvas=False,db_connection_str='',
                 t_box_height_max = 15,t_box_width_max = 50):
        # t_box_height_max is the max number of lines to show
        # t_box_width_max is the max number of letters to show
        super().__init__()
        self.t_box_width = t_box_width_max
        self.t_box_height = t_box_height_max



        # create a horizontal scrollbar
        s_bar_hor = tk.Scrollbar(parent_frame, orient='horizontal')
        # attach Scrollbar to text
        s_bar_hor.pack(side=tk.BOTTOM, fill=tk.X)

        # create a vertical scrollbar
        s_bar_vert = tk.Scrollbar(parent_frame)

        # attach Scrollbar to text
        s_bar_vert.pack(side=tk.RIGHT, fill=tk.Y)
        if len(text_iter) < self.t_box_height:
            self.t_box_height = len(text_iter)

        if with_canvas: # use a canvas backround with pic
            # create a Canvas widget
            canvas = tk.Canvas(parent_frame, width=self.t_box_width, height=self.t_box_height)
            canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

            # get random image name and image
            print('Help Tab ', end='')
            random_image_info = dbFuncs.getImageRandom(db_connection_str)[0]
            self.image_name = random_image_info[0]
            self.image = random_image_info[1]
            # create a PhotoImage object from the image file
            #self.img = Image.open(io.BytesIO(self.image_bytes))
            #self.img = ImageTk.PhotoImage(self.img)
            #img = tk.PhotoImage(data=dbFuncs.getImageRandom(db_connection_str)[0][0])
            # create an image item on the canvas
            canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
            # create a Text widget on top of the canvas
            text_box_info = tk.Text(canvas, width=self.t_box_width, height=self.t_box_height, wrap=tk.NONE,
                                    xscrollcommand=s_bar_hor.set,
                                    yscrollcommand=s_bar_vert.set)
        else:
            # create a Text widget
            # xscrollcomannd is used to attach Text widget to the horizontal scrollbar
            # yscrollcomannd is used to attach Text widget to the vertical scrollbar
            text_box_info = tk.Text(parent_frame, width=self.t_box_width, height=self.t_box_height, wrap=tk.NONE,
                     xscrollcommand=s_bar_hor.set,
                     yscrollcommand=s_bar_vert.set)

        # insert some text into the text widget
        for num,text in enumerate(text_iter):
            if numbered:
                text_str = f'{num+1}) {text}\n'
            else:
                text_str = f'{text}\n'
            text_box_info.insert(tk.END, text_str)
        # make text read only
        text_box_info.configure(state='disabled')

        if with_canvas:
            # attach Text widget to the canvas
            canvas.create_window(0, 0, anchor=tk.NW, window=text_box_info)
            # configure the Text widget's scrolling
            s_bar_hor.config(command=canvas.xview)
            s_bar_vert.config(command=canvas.yview)
            canvas.configure(scrollregion=canvas.bbox(tk.ALL))
        else:
            # attach Text widget
            text_box_info.pack(side=tk.TOP, fill=tk.X)
            # command represents the method to be executed xview is executed on
            s_bar_hor.config(command=text_box_info.xview)
            # command represents the method to be executed yview is executed on
            s_bar_vert.config(command=text_box_info.yview)

    def getImage(self):
       try:
           return self.image
       except AttributeError: # only canvas boxes have this attribute
           return None