"""HOME PAGE"""

import tkinter as tk
from PIL import Image, ImageTk
class Home(tk.Frame):
    # home_pic_location = '../Food Images/beef-gulasch-356793.jpg'

    def __init__(self, parent, controller, navigation_pages:dict,pic_location):
        self.PAGE_NAME = 'HOME'
        # parent is the root window
        # controller switches the pages
        # navigation_pages are the pages user can go to from this page( format {'Home':frame_obj}
        global home_photo
        counter = 0
        tk.Frame.__init__(self, parent)

        # FRAME
        frame_pic = tk.Frame(self, padx=0, pady=0)
        frame_pic.grid(row=1, column=0)

        frame_btn = tk.Frame(self, padx=0, pady=0)
        frame_btn.grid(row=2, column=0, padx=0, pady=0)

        # BUTTONS
        # creat navigation buttons
        print(navigation_pages)
        for name, frame in navigation_pages.items():
            new_button = tk.Button(frame_btn,text=name,command=lambda:controller.show_frame(navigation_pages[name]))
            new_button.grid(row=1,column=counter,padx=5)
            counter+=1
        btn_quit = tk.Button(frame_btn, text='quit',command=lambda:exit('QUIT'))
        btn_quit.grid(row=1, column=counter, padx=5)

        #  LABELS
        image = Image.open(pic_location)
        home_photo = ImageTk.PhotoImage(image)
        lbl_pic = tk.Label(frame_pic, image=home_photo)
        lbl_pic.pack()

        lbl_title = tk.Label(self, text='welcome to cookbook app')
        lbl_title.grid(row=0, column=0)

        """btn_search = tk.Button(frame_btn, text='search', command=lambda: controller.show_frame(Search))
        btn_search.grid(row=1, column=0, padx=5)

        btn_add = tk.Button(frame_btn, text='add', command=lambda: controller.show_frame(Add))
        btn_add.grid(row=1, column=1, padx=5)

        btn_help = tk.Button(frame_btn, text='help', command=lambda: controller.show_frame(Help))
        btn_help.grid(row=1, column=2, padx=5)"""




