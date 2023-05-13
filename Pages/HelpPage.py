"""HELP PAGE"""
# skeleton from: https://www.geeksforgeeks.org/creating-tabbed-widget-with-python-tkinter/
import tkinter as tk
from tkinter import ttk
from Widgets import ScrollBox as sBox

"""
Explains how to use the application
"""


class Help(tk.Toplevel):
    TABS_GREETING = 'INFO:'
    def __init__(self,bg_colr):
        # nav dict needs:
        super().__init__()
        self.title('Help')
        self.BG_COLOR = bg_colr
        self.geometry('400x300')# set size


        tab_parent = ttk.Notebook(self)# parent widget for tabs

        tab_labels = {'home':ttk.LabelFrame(tab_parent,borderwidth=0,text=self.TABS_GREETING),
                'search':ttk.LabelFrame(tab_parent,borderwidth=0,text=self.TABS_GREETING),
                'add':ttk.LabelFrame(tab_parent,borderwidth=0,text=self.TABS_GREETING),
                'recipe':ttk.LabelFrame(tab_parent,borderwidth=0,text=self.TABS_GREETING),
                'app_info':ttk.LabelFrame(tab_parent,borderwidth=0,text=self.TABS_GREETING),
                'logs':ttk.LabelFrame(tab_parent,borderwidth=0,text=self.TABS_GREETING)
                } # make tab frames

        # ADD INFO
        all_tabs = {
                    'home_info':sBox.ScrollTextBox(tab_labels['home'],'home info here'.split(),self.BG_COLOR,numbered=False),
                    'search_info':sBox.ScrollTextBox(tab_labels['search'], 'search info here'.split(),self.BG_COLOR,numbered=False),
                    'add_info':sBox.ScrollTextBox(tab_labels['add'], 'add info here'.split(),self.BG_COLOR,numbered=False),
                    'recipe_info':sBox.ScrollTextBox(tab_labels['recipe'], 'recipe info here'.split(),self.BG_COLOR,numbered=False),
                    'app_info_info':sBox.ScrollTextBox(tab_labels['app_info'], 'app_info info here'.split(),self.BG_COLOR,numbered=False),
                    'logs_info':sBox.ScrollTextBox(tab_labels['logs'], 'logs info here'.split(),self.BG_COLOR,numbered=False)
                    }


        for t in tab_labels.keys():# add tabs to notebook object
            tab_parent.add(tab_labels[t],text=t)


        tab_parent.pack(expand=1,fill='both')# add parent widget to window

