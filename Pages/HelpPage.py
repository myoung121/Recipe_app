"""HELP PAGE"""
# skeleton from: https://www.geeksforgeeks.org/creating-tabbed-widget-with-python-tkinter/
import tkinter as tk
from tkinter import ttk

import application as app
from Widgets import ScrollBox as sBox

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
        # set size
        self.geometry('400x300')
        db_str = app.test_db_str
        # make parent widget for tabs
        tab_parent = ttk.Notebook(self)

        # make tab frames
        tab_labels = {'home':ttk.LabelFrame(tab_parent),
                'search':ttk.LabelFrame(tab_parent),
                'add':ttk.LabelFrame(tab_parent),
                'recipe':ttk.LabelFrame(tab_parent),
                'app_info':ttk.LabelFrame(tab_parent),
                'logs':ttk.LabelFrame(tab_parent)
                }

        # ADD INFO
        all_tabs = {
                    'home_info':sBox.ScrollTextBox(tab_labels['home'],'home info here'.split(),
                                                 numbered=False,with_canvas=True,db_connection_str=db_str),
                    'search_info':sBox.ScrollTextBox(tab_labels['search'], 'search info here'.split(),
                                                   numbered=False,with_canvas=True,db_connection_str=db_str),
                    'add_info':sBox.ScrollTextBox(tab_labels['add'], 'add info here'.split(),
                                                numbered=False,with_canvas=True,db_connection_str=db_str),
                    'recipe_info':sBox.ScrollTextBox(tab_labels['recipe'], 'recipe info here'.split(),
                                                   numbered=False,with_canvas=True,db_connection_str=db_str),
                    'app_info_info':sBox.ScrollTextBox(tab_labels['app_info'], 'app_info info here'.split(),
                                                     numbered=False,with_canvas=True,db_connection_str=db_str),
                    'logs_info':sBox.ScrollTextBox(tab_labels['logs'], 'logs info here'.split(),
                                                 numbered=False,with_canvas=True,db_connection_str=db_str)
                    }

        # export canvas images to main app
        #for tab_name,box in all_tabs.items():
        #    app.help_canvas[tab_name] = box.getImage()
        # add tabs to notebook object
        for t in tab_labels.keys():
            tab_parent.add(tab_labels[t],text=t)

        # add parent widget to window
        tab_parent.pack(expand=1,fill='both')
"""
home_info=sBox.ScrollTextBox(tabs['home'],'home info here'.split(),
                                     numbered=False,with_canvas=True,db_connection_str=db_str)
        search_info=sBox.ScrollTextBox(tabs['search'], 'search info here'.split(),
                                       numbered=False,with_canvas=True,db_connection_str=db_str)
        add_info=sBox.ScrollTextBox(tabs['add'], 'add info here'.split(),
                                    numbered=False,with_canvas=True,db_connection_str=db_str)
        recipe_info=sBox.ScrollTextBox(tabs['recipe'], 'recipe info here'.split(),
                                       numbered=False,with_canvas=True,db_connection_str=db_str)
        app_info_info=sBox.ScrollTextBox(tabs['app_info'], 'app_info info here'.split(),
                                         numbered=False,with_canvas=True,db_connection_str=db_str)
        logs_info=sBox.ScrollTextBox(tabs['logs'], 'logs info here'.split(),
                                     numbered=False,with_canvas=True,db_connection_str=db_str)
"""