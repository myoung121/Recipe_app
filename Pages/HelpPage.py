"""HELP PAGE"""
# skeleton from: https://www.geeksforgeeks.org/creating-tabbed-widget-with-python-tkinter/
import tkinter as tk
from tkinter import ttk
from Pages import ScrollBox as sBox

"""
should open in sep. window
only one can be open
tabs should have scroll boxes
make close button
    move tabs down a row
"""


class Help(tk.Toplevel):

    def __init__(self):
        # nav dict needs:
        super().__init__()
        self.title('Help / Info')

        # make parent widget for tabs
        tab_parent = ttk.Notebook(self)

        # make tab frames
        tabs = {'home':ttk.LabelFrame(tab_parent),
                'search':ttk.LabelFrame(tab_parent),
                'add':ttk.LabelFrame(tab_parent),
                'recipe':ttk.LabelFrame(tab_parent),
                'app_info':ttk.LabelFrame(tab_parent),
                'logs':ttk.LabelFrame(tab_parent)
                }



        # ADD INFO
        home_info=sBox.ScrollTextBox(tabs['home'],'add info here'.split(),numbered=False,with_canvas=True)
        search_info=sBox.ScrollTextBox(tabs['search'], 'add info here'.split(),numbered=False,with_canvas=True)
        add_info=sBox.ScrollTextBox(tabs['add'], 'add info here'.split(),numbered=False,with_canvas=True)
        recipe_info=sBox.ScrollTextBox(tabs['recipe'], 'add info here'.split(),numbered=False,with_canvas=True)
        app_info_info=sBox.ScrollTextBox(tabs['app_info'], 'add info here'.split(),numbered=False,with_canvas=True)
        logs_info=sBox.ScrollTextBox(tabs['logs'], 'add info here'.split(),numbered=False,with_canvas=True)
        # add tabs to notebook object
        for t in tabs.keys():
            tab_parent.add(tabs[t],text=t)

        # add parent widget to window
        tab_parent.pack(expand=1,fill='both')
