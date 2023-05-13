""" Python Program to make a scrollable frame
skeleton from: https://www.geeksforgeeks.org/scrollable-frames-in-tkinter/
"""

import tkinter as tk
class ScrollTextBox(tk.Frame):

    # constructor
    def __init__(self,parent_frame:tk.LabelFrame,text_iter,bg_color,
                 numbered=True,t_box_height_max = 15,t_box_width_max = 50):
        # t_box_height_max is the max number of lines to show
        # t_box_width_max is the max number of letters to show
        super().__init__()
        self.t_box_width = t_box_width_max
        self.t_box_height = t_box_height_max
        self.BG_COLOR = bg_color

        s_bar_hor = tk.Scrollbar(parent_frame, orient='horizontal',troughcolor=self.BG_COLOR,bg='white',bd=0)# create a horizontal scrollbar
        s_bar_hor.pack(side=tk.BOTTOM, fill=tk.X,pady=2,padx=1)# attach Scrollbar to text
        s_bar_vert = tk.Scrollbar(parent_frame,troughcolor=self.BG_COLOR,bg='white',bd=0) # create a vertical scrollbar(default is vertical)
        s_bar_vert.pack(side=tk.RIGHT, fill=tk.Y,padx=2)# attach Scrollbar to text
        text_box_info = tk.Text(parent_frame, width=self.t_box_width, height=self.t_box_height, wrap=tk.NONE,
                 xscrollcommand=s_bar_hor.set,
                 yscrollcommand=s_bar_vert.set) # create a Text widget and attach scrollbars

        for num,text in enumerate(text_iter): # insert the text
            if numbered: # show line numbers with text
                text_str = f'{num+1}) {text}\n'
            else:
                text_str = f'{text}\n' # show just the text
            text_box_info.insert(tk.END, text_str)
        text_box_info.configure(state='disabled')# make text widget read only
        text_box_info.pack(side=tk.TOP, fill=tk.X)
        s_bar_hor.config(command=text_box_info.xview) # set scrollbar horizontal movement
        s_bar_vert.config(command=text_box_info.yview)# set scrollbar vertical movement
