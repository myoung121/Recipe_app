"""HELP PAGE"""
# skeleton from: https://www.geeksforgeeks.org/creating-tabbed-widget-with-python-tkinter/
import tkinter as tk
from tkinter import ttk
from Widgets import ScrollBox as sBox
from Pages import HelpPage_text as hTxt


class Help(tk.Toplevel):
    TABS_GREETING = 'INFO:'
    def __init__(self,bg_colr):
        # bg_color is the window background color
        super().__init__()
        self.title('Help') # set the window title
        self.BG_COLOR = bg_colr
        self.geometry('600x300')# set size
        self.resizable(width=False, height=False)  # lock window size
        tab_parent = ttk.Notebook(self)# parent widget for tabs
        tab_labels = {'home':ttk.LabelFrame(tab_parent,borderwidth=0,text=self.TABS_GREETING),
                'search':ttk.LabelFrame(tab_parent,borderwidth=0,text=self.TABS_GREETING),
                'add':ttk.LabelFrame(tab_parent,borderwidth=0,text=self.TABS_GREETING),
                'recipe':ttk.LabelFrame(tab_parent,borderwidth=0,text=self.TABS_GREETING),
                'app_info':ttk.LabelFrame(tab_parent,borderwidth=0,text=self.TABS_GREETING)
                } # make tab frames
        all_tabs = {
                    'home_info':sBox.ScrollTextBox(tab_labels['home'],hTxt.getHomeTxt(),self.BG_COLOR,numbered=False,set_bg_color=True),
                    'search_info':sBox.ScrollTextBox(tab_labels['search'], hTxt.getSearchTxt(),self.BG_COLOR,numbered=False,set_bg_color=True),
                    'add_info':sBox.ScrollTextBox(tab_labels['add'], hTxt.getAddTxt(),self.BG_COLOR,numbered=False,set_bg_color=True),
                    'recipe_info':sBox.ScrollTextBox(tab_labels['recipe'], hTxt.getRecipeTxt(),self.BG_COLOR,numbered=False,set_bg_color=True),
                    'app_info_info':sBox.ScrollTextBox(tab_labels['app_info'], hTxt.getAppInfoTxt(),self.BG_COLOR,numbered=False,set_bg_color=True)
                    } #tabs with added text
        for t in tab_labels.keys():# add tabs to notebook object
            tab_parent.add(tab_labels[t],text=t)
        tab_parent.pack(expand=1,fill='both')# add parent widget to window

