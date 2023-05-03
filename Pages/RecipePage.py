"""
RECIPE PAGE
"""
import pprint

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import scrolledtext
import  io
from Functions import db_query_functions as dbFuncs
import application as app
from Pages import ScrollBox as sBox
class Recipe(tk.Toplevel):

    def closePage(self,name):
        app.open_recipes.remove(self.recipe_name)
        print(f'closed {self.recipe_id}-{self.recipe_name} ->')

        self.destroy()

    def toggleFav(self,chk_box_state):
        """add and remove favorite from recipe"""
        dbFuncs.toggleFav(self.recipe_id,app.test_db_str)

    def __init__(self, recipe_info:dict, recipe_image_blob:bytes):
        super().__init__()
        self.recipe_id = recipe_info['recipe_id']
        self.recipe_name = recipe_info['name']
        self.recipe_ingreds = recipe_info['ingredients']
        self.recipe_instrs = recipe_info['instr'].split('. ')
        self.recipe_comment = recipe_info['comment']
        if recipe_info['favorite']:
            self.favorite = True
        else:
            self.favorite = False
        if not self.recipe_comment:
            self.recipe_comment = ''
        # convert image bytes to file-like object
        pic = Image.open(io.BytesIO(recipe_image_blob))  # convert image bytes to PIL image format(jpeg)
        self.recipe_pic = ImageTk.PhotoImage(pic)
        width = '800'
        height = '700'
        self.geometry(f'{width}x{height}')
        self.title(f'#{self.recipe_id} {self.recipe_name.upper()}')
        # FRAME
        frame_navigation = tk.LabelFrame(self, text='navigation', padx=0, pady=0)
        frame_navigation.grid(row=0, column=1)
        frame_image_note = tk.LabelFrame(self,text='image/note')
        frame_image_note.grid(row=1, column=1,rowspan=3)
        frame_ingreds_instrs = tk.LabelFrame(self, text='Ingreds/Instrs',height=int(height)-100,width=int(int(width)/2))
        frame_ingreds_instrs.grid(row=1, rowspan=2,column=0)
        frame_ingreds = tk.LabelFrame(frame_ingreds_instrs,text='ingreds')
        frame_ingreds.grid(row=0,column=0,sticky='n',pady=20)
        frame_instrs = tk.LabelFrame(frame_ingreds_instrs,text='instrs')
        frame_instrs.grid(row=1,column=0,sticky='s',pady=25)
        frame_note = tk.LabelFrame(frame_image_note, text='notes')
        frame_note.grid(row=2, column=0,columnspan=3)
        # CHECKBOX
        favorite_toggle = tk.IntVar()
        chk_box_fav = tk.Checkbutton(frame_navigation, text='fav', variable=favorite_toggle,command=lambda:self.toggleFav(self.recipe_id))
        chk_box_fav.grid(row=0, column=0)
        # if recipe is favorite


        # FAV CHECKBOX WONT SELECT
        if self.favorite:
            #print('fav should be selected')
            chk_box_fav.select()



        # BUTTON
        btn_close = tk.Button(frame_navigation,text='close',command=lambda:self.closePage(self.recipe_name))
        btn_close.grid(row=0,column=1)
        btn_save_note = tk.Button(frame_note, text='save')
        btn_save_note.grid(row=1, column=2)
        btn_edit=tk.Button(frame_note,text='edit')
        btn_edit.grid(row=1,column=0)
        # LABEL
        lbl_blank = tk.Label(frame_ingreds_instrs)
        lbl_blank.grid(row=1, column=0, pady=5)
        # SCROLLTEXT
        scroll_text_ingreds= sBox.ScrollTextBox(frame_ingreds,self.recipe_ingreds)
        scroll_text_istrs = sBox.ScrollTextBox(frame_instrs,self.recipe_instrs)
        # IMAGE
        lbl_pic = tk.Label(frame_image_note, image=self.recipe_pic)
        lbl_pic.grid(row=0, column=0)
        # ENTRY
        #entry_recipe_note = tk.Entry(frame_note,
        #                             borderwidth=4)
        #entry_recipe_note.grid(row=0, column=0, pady=0)
        # SCROLLED TEXT
        # Creating scrolled text area
        recipe_note = scrolledtext.ScrolledText(frame_note,
                                    width=30,
                                    height=8,
                                    font=("Times New Roman",
                                          15))
        recipe_note.grid(column=0,row=0, pady=0, padx=0,columnspan=3)
        # Inserting Text which is read only
        recipe_note.insert(tk.INSERT,self.recipe_comment)
        # Making the text read only
        recipe_note.configure(state='disabled')
