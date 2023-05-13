"""
RECIPE PAGE
"""

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import scrolledtext
import  io
import random as ran
from Functions import db_query_functions as dbFuncs
from Widgets import ScrollBox as sBox


class Recipe(tk.Toplevel):
    WINDOW_WIDTH = '800' # window width
    WINDOW_HEIGHT = '700' # window height
    LABEL_TEXT_FONT = ('Default',10) # window text font
    __bg_colors__ = tuple('#b2d3c2 #ebe1a1 #2c7564 #9e7b6f #524d5c #8f9ba6 '
                          '#945d00 #ffb6c1 #ffeead #4b0082'.split(' ')) # poss background colors
    __BG_COLORS2__ = tuple('#FFA07A #FFD700 #FF69B4 #9400D3 #FF8C00 ' 
                           '#00FFFF #FF1493 #BA55D3 #32CD32 #FF4500'.split(' ')) # poss background colors
    FAV_TEXT = u"\u2B50\uFE0F" # star emoji output when recipe is favorited


    def __init__(self, recipe_info:dict, recipe_image_blob:bytes,open_pages_tracker,db_connection_str):
        super().__init__()
        #color_set = ran.choice((self.__bg_colors__,self.__bg_colors2__))
        self.color = ran.choice(self.__bg_colors__) # pick a random background color for each instance
        self.text_color = 'black' # instance text color
        self.recipe_id = recipe_info['recipe_id'] # instance recipe id number
        self.recipe_name = recipe_info['name'] # instance recipe name
        self.recipe_ingreds = recipe_info['ingredients'] # instance recipe ingredients
        self.recipe_instrs = recipe_info['instr'].split('. ') # instance recipe instructions
        self.recipe_comment = recipe_info['comment'] # instance recipe comments
        self.open_pages = open_pages_tracker # tracks open windows
        self.db_conn = db_connection_str # database pathway
        if recipe_info['favorite']: # track if recipe is a user favorite
            self.favorite = True
        else:
            self.favorite = False
        if not self.recipe_comment:
            self.recipe_comment = '' # get the comment in the right data type
        try: # get the recipe image or a random image if a user created recipe
            pic = Image.open(io.BytesIO(recipe_image_blob))  # convert image bytes to PIL image format(jpeg)
            self.recipe_pic = ImageTk.PhotoImage(pic)
        except TypeError: # when opening a user created recipe, the image is already built b/c it uses getImageRandom() so just need to add to window.
            self.recipe_pic = recipe_image_blob
        self.geometry(f'{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}') # set window size
        self.title(f'#{self.recipe_id} {self.recipe_name.upper()}') # set the window displayed name
        self.config(bg=self.color) # set the background color

        #-----------------------------------------------------------------
        # FUNCTIONS
        def closePage():
            """closes recipe page"""
            self.open_pages.remove(self.recipe_name)  # remove itself from the open windows tracker
            print(f'closed {self.recipe_id}-{self.recipe_name} ->')
            self.destroy()  # close window

        def toggleFav():
            """add and remove favorite from recipe"""
            dbFuncs.toggleFav(self.recipe_id, self.db_conn) # set favorite to true in database
            self.favorite = not self.favorite # switch the favorite value
            if self.favorite:
                lbl_fav_display.config(text=self.FAV_TEXT) # display pic showing recipe was favorited
            else:
                lbl_fav_display.config(text=' ') # if unfavorited, switch text to blank

        def editComment():
            """toggle recipe comment edit mode / set comment box to normal,disable"""
            comment_box_state = recipe_note.cget('state')  # get comment box state
            if comment_box_state == 'disabled':
                recipe_note.config(state='normal',takefocus=True)
            else:
                recipe_note.config(state='disabled')

        def saveComment():
            """save comment to database while comment box is active"""
            if recipe_note.cget('state') == 'normal': # get comment box state and only save comment in edit mode
                notes =recipe_note.get('1.0',tk.END)[:-1].strip() # get all comments
                if notes: # if comment not blank
                    dbFuncs.addComment(self.recipe_id,self.db_conn,notes) # add comment to recipe in database
                else: # comment box is blank
                    pass
                recipe_note.config(state='disabled')
        #-----------------------------------------------------------------
        # CLOSE WINDOW WIDGETS
        frame_close = tk.Frame(self,bg=self.color) # close button frame
        frame_close.grid(row=0, column=1,pady=10)
        btn_close = tk.Button(frame_close,bg=self.color,fg=self.text_color,text='Close',command=closePage) # CLOSE WINDOW BUTTON
        btn_close.grid(row=0,column=2,padx=5)
        lbl_fav_display = tk.Label(frame_close,width=6,bg=self.color,fg='yellow',text=' ',font=('Default',12)) # between favorite and close buttons / shows if recipe is a favorite
        lbl_fav_display.grid(row=0,column=1)
        btn_fav = tk.Button(frame_close, bg=self.color,fg=self.text_color,text='Fav',command=toggleFav) # button to add/remove recipe to/from favorites
        btn_fav.grid(row=0, column=0)
        if self.favorite:
            lbl_fav_display.config(text=self.FAV_TEXT) # show text that recipe is a favorite


        # IMAGE AND COMMENTS WIDGETS
        frame_image_comment = tk.Frame(self,bg=self.color) # image and note frame
        frame_image_comment.grid(row=1, column=1,rowspan=3)
        frame_image = tk.LabelFrame(frame_image_comment,bg=self.color,font=self.LABEL_TEXT_FONT,
                                    fg=self.text_color,text=self.recipe_name,borderwidth=0) # image frame
        frame_image.grid(row=0,column=0,pady=5)
        lbl_pic = tk.Label(frame_image, bg=self.color,image=self.recipe_pic) # recipe image label
        lbl_pic.grid(row=0, column=0)
        frame_comment = tk.LabelFrame(frame_image_comment, bg=self.color,text='Comments',borderwidth=0,font=self.LABEL_TEXT_FONT) # recipes comments frame
        frame_comment.grid(row=2, column=0,columnspan=3,pady=5)
        recipe_note = scrolledtext.ScrolledText(frame_comment,
                                    width=30,height=8) # display for the recipe comment. disabled by default
        recipe_note.grid(column=0,row=0, pady=0, padx=0,columnspan=3)
        recipe_note.insert(tk.INSERT,self.recipe_comment) # add recipe's comments to the box
        recipe_note.config(state = 'disabled') # disable scroll box
        btn_save_note = tk.Button(frame_comment, bg=self.color,fg=self.text_color,text='Save',
                                  command=saveComment) # save recipe comment button
        btn_save_note.grid(row=1, column=2,pady=5)
        btn_edit=tk.Button(frame_comment,bg=self.color,fg=self.text_color,
                           text='Edit',command=editComment) # allows comment to be editable
        btn_edit.grid(row=1,column=0,pady=5)


        # INGREDIENTS AND INSTRUCTIONS WIDGETS
        frame_ingreds_instrs = tk.Frame(self, bg=self.color,height=int(self.WINDOW_HEIGHT)-100, width=int(int(self.WINDOW_WIDTH) / 2)) # main ingredient and instructions frame
        frame_ingreds_instrs.grid(row=1, rowspan=2,column=0,padx=5)
        frame_ingreds = tk.LabelFrame(frame_ingreds_instrs,text='Ingredients', bg=self.color,fg=self.text_color,
                                      borderwidth=0,font=self.LABEL_TEXT_FONT) # recipe ingredients frame
        frame_ingreds.grid(row=0,column=0,sticky='n',pady=20)
        scroll_text_ingreds= sBox.ScrollTextBox(frame_ingreds,self.recipe_ingreds,self.color) # ingredients are listed in a scrollbox
        lbl_blank = tk.Label(frame_ingreds_instrs,bg=self.color) # empty spacer between ingredients and instructions scroll tboxes
        lbl_blank.grid(row=1, column=0, pady=5)
        frame_instrs = tk.LabelFrame(frame_ingreds_instrs,text='Instructions',bg=self.color,fg=self.text_color,
                                      borderwidth=0,font=self.LABEL_TEXT_FONT) # recipe instructions frame
        frame_instrs.grid(row=1,column=0,sticky='s',pady=25)
        scroll_text_istrs = sBox.ScrollTextBox(frame_instrs,self.recipe_instrs,self.color) # instructions are listed in a scrollbox


        self.protocol("WM_DELETE_WINDOW", closePage) # call the closePage function when the window is closed


