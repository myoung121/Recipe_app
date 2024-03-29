""" Python Program to make a scrollable frame
skeleton from: https://www.geeksforgeeks.org/scrollable-frames-in-tkinter/
"""

import tkinter as tk
class ScrollTextBox(tk.Frame):

    # constructor
    def __init__(self,parent_frame:tk.LabelFrame,text_iter,bg_color,
                 numbered=True,set_bg_color=False,t_box_height_max = 15,t_box_width_max = 50):
        # parent_frame is where the widget is placed
        # text_iter is the text inserted into the display
        # bg_color is the background color
        # numbered sets if lines are printed with line numbers in display
        # set_bg_color set if background color is applied to the display
        # t_box_height_max is the max number of lines to show
        # t_box_width_max is the max number of letters to show
        super().__init__()
        self.t_box_width = t_box_width_max # set text box width
        self.t_box_height = t_box_height_max # set text box height
        self.BG_COLOR = bg_color # set background color

        s_bar_hor = tk.Scrollbar(parent_frame, orient='horizontal',troughcolor=self.BG_COLOR,bg='white',bd=0)# create a horizontal scrollbar
        s_bar_hor.pack(side=tk.BOTTOM, fill=tk.X,pady=2,padx=1)# attach Scrollbar to text
        s_bar_vert = tk.Scrollbar(parent_frame,troughcolor=self.BG_COLOR,bg='white',bd=0) # create a vertical scrollbar(default is vertical)
        s_bar_vert.pack(side=tk.RIGHT, fill=tk.Y,padx=2)# attach Scrollbar to text
        text_box_info = tk.Text(parent_frame, width=self.t_box_width, height=self.t_box_height, wrap=tk.NONE,
                 xscrollcommand=s_bar_hor.set,
                 yscrollcommand=s_bar_vert.set) # create a Text widget and attach scrollbars
        if set_bg_color: # set a background color
            text_box_info.config(bg=self.BG_COLOR,fg='white')
        # this widget is used for list and strings so have to check for that condition
        if isinstance(text_iter,(list,tuple)):
            for num,text in enumerate(text_iter): # insert the text
                if numbered: # show line numbers with text
                    text_str = f'{num+1}) {text}\n'
                else:
                    text_str = f'{text}\n' # show just the text
                text_box_info.insert(tk.END, text_str)
        else: # if input is a string
            text_box_info.insert('1.0',text_iter)
        text_box_info.configure(state='disabled')# make text widget read only
        text_box_info.pack(side=tk.TOP, fill=tk.X)
        s_bar_hor.config(command=text_box_info.xview) # set scrollbar horizontal movement
        s_bar_vert.config(command=text_box_info.yview)# set scrollbar vertical movement
