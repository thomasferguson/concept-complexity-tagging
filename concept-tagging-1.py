# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 23:37:21 2018

@author: thomasferguson
"""

import os

from textatistic import Textatistic, fleschkincaid_score

from gutenberg.cleanup import strip_headers

from langdetect import detect

output_dict = {}

for root, dirs, files in os.walk("E://gutenberg", topdown = False):
    for name in files:
        if name[-4:] == ".txt" and name[-6:] != "-8.txt" and name not in output_dict.keys():
            text_loc = os.path.join(root,name)
            text1 = strip_headers(open(text_loc,"r").read())
            if detect(text1) == "en":
                text2 = Textatistic(text1)
                output_dict[text_loc] = text2.fleschkincaid_score
                print(text_loc, output_dict[text_loc])