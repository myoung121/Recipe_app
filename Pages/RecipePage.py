"""
how to make recipe page:
when clicked it should call the recipe class and add to frames in main tkinterApp obj and show page

    list class on sepeate fiile
    make function to add to tkinterApp frames dict
    make function to remove page from dict after user leaves page

"""


from PIL import Image, ImageTk
import tkinter as tk
from tkinter import scrolledtext

class Recipe(tk.Toplevel):

    #def addFrame(self, new_frame_obj ,*recipe_args, current_frames:dict=frames)->dict:
    #    container = tk.Frame(self)
    #    container.pack(side="top", fill="both", expand=True)
#
    #    container.grid_rowconfigure(0, weight=1)
    #    container.grid_columnconfigure(0, weight=1)
    #    frame = new_frame_obj(container, self,*recipe_args)
    #    current_frames[new_frame_obj] = frame
    #    frame.grid(row=0, column=0, sticky="nsew")
         #return new_frame_obj
    def __init__(self, controller, recipe_name, recipe_ingreds, recipe_instrs, pic_location):
        #,,,recipe_notes
        super().__init__()
        global recipe_photo
        #tk.Toplevel.__init__(self, parent)
        #tk.Frame()
        self.geometry("900x700")

        # FRAME
        frame_navigation = tk.LabelFrame(self, text='navigation', padx=0, pady=0)
        frame_navigation.grid(row=0, column=1)

        frame_note = tk.LabelFrame(self, text='notes')
        frame_note.grid(row=2, column=1)

        frame_ingreds_instrs = tk.LabelFrame(self, text='Ingreds/Instrs')
        frame_ingreds_instrs.grid(row=1, rowspan=3, column=0)

        # CHECKBOX
        favorite_toggle = tk.IntVar()
        chk_box_fav = tk.Checkbutton(frame_navigation, text='fav', variable=favorite_toggle)
        chk_box_fav.grid(row=0, column=0)

        # BUTTON
        """        btn_search = tk.Button(frame_navigation, text='search', command=lambda: controller.show_frame(search_page))
        btn_search.grid(row=0, column=1)
        btn_home = tk.Button(frame_navigation, text='home', command=lambda: controller.show_frame(home_page))
        btn_home.grid(row=0, column=2)"""
        btn_close = tk.Button(frame_navigation,text='close',command=lambda:self.destroy)
        btn_close.grid(row=0,column=1)
        btn_save_note = tk.Button(frame_note, text='save')
        btn_save_note.grid(row=1, column=0)

        # LABEL
        lbl_recipe_name = tk.Label(self, text=recipe_name)
        lbl_recipe_name.grid(row=0, column=0)

        lbl_ingreds = tk.Label(frame_ingreds_instrs, text=recipe_ingreds)
        lbl_ingreds.grid(row=0, column=0)
        lbl_blank = tk.Label(frame_ingreds_instrs)
        lbl_blank.grid(row=1, column=0, pady=5)
        lbl_instrs = tk.Label(frame_ingreds_instrs, text=recipe_instrs)
        lbl_instrs.grid(row=2, column=0)
        #try:
        image = Image.open(pic_location)
        recipe_photo = ImageTk.PhotoImage(image)
        lbl_pic = tk.Label(self, image=recipe_photo)
        lbl_pic.grid(row=1, column=1)

        # ENTRY
        entry_recipe_note = tk.Entry(frame_note,
                                     borderwidth=4)  # should be a tall text box with info in field with optioon to edit when window opened
        entry_recipe_note.grid(row=0, column=0, pady=0)

        # SCROLLED TEXT
        # Creating scrolled text area
        recipe_note = scrolledtext.ScrolledText(frame_note,
                                    width=30,
                                    height=8,
                                    font=("Times New Roman",
                                          15))
        recipe_note.grid(column=0,row=0, pady=0, padx=0)
        # Inserting Text which is read only
        recipe_note.insert(tk.INSERT,
                         """\
                         RECIPE COMMENTS
                         """)
        # Making the text read only
        recipe_note.configure(state='disabled')
