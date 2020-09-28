#=================================================
# import modules
#=================================================

import tkinter as tk
from tkinter import ttk
from tkinter import Menu
from tkinter import scrolledtext
from tkinter import messagebox as msg

from tkinter.filedialog import askopenfilename, askdirectory
from bs4 import BeautifulSoup
import re
import urllib.request
import urllib.parse
import json
import socket
import os
import pickle
from time import sleep
from textatistic import Textatistic, fleschkincaid_score
from gutenberg.cleanup import strip_headers
from langdetect import detect
import nltk
from nltk.stem.porter import *
from nltk.collocations import *


# Reserve port

s = socket.socket()
host = socket.gethostname()  # Get the local machine name
port = 12397                 # Reserve a port for your service
s.bind((host,port))  

# Choose stemmer

stemmer = PorterStemmer()

# Declare variables

current_directory = "/cyc/projects/hyperintensionality/concept_tagging/gutenberg/"
current_stemmed_directory = ""
lex_filename = ""
f_k_filename = ""
current_prc_terms_directory = ""

new_lexification_directory = ""

create_stemmed_path = ""
create_lexifications_path = ""
create_f_k_path = ""
create_prc_path = ""

# Create Flesch-Kincaid-izer


# Create Stemming Functions

def stem_convert(text):
       text2 = text.split()
       text3 = [stemmer.stem(term.lower()) for term in text2]
       text4 = ' '.join(text3)
       return(text4)

def reconcile(lexification_dict):
	for term1 in lexification_dict.keys():
		for term2 in lexification_dict.keys():
			if term1 in term2 and term1 != term2:
				lexification_dict[term1] -= lexification_dict[term2]
	return(sum(list(lexification_dict.values())))

def get_data(lexification_list):
	output_dict = {}
	n = 0
	for file_name in new_readability_dictionary.keys():
		cleaned_file_name = file_name + '-clean.txt'
		if cleaned_file_name in files:
			path = '/scratch/gutenberg_cleaned/' + cleaned_file_name
			value = int(round(new_readability_dictionary[file_name], 1)) #check second argument; it might be wrong
			text = open(path, 'r').read()
			count_dict = {}
			for lexification in lexification_list:
				count_dict[lexification] = text.count(lexification)
			count = reconcile(count_dict)
			if value in output_dict.keys():
                		output_dict[value] += count
			else:
				output_dict[value] = count
			print(n)
			n += 1
		else:
			True
	return(output_dict)
    
# lex_filename = 'C:\\gutenberg_lex_test\\dyson.pickle'

def make_prc():
    global current_stemmed_directory
    global lex_filename
    global f_k_filename
    global current_prc_terms_directory
    if current_stemmed_directory == "":
        msg.showwarning("Utility Warning", "No path for stemmed Gutenberg corpus has been selected..")
        return ""
    if lex_filename == "":
        msg.showwarning("Utility Warning", "No dictionary of Cyc lexifications has been selected.")
        return ""
    if f_k_filename == "":
        msg.showwarning("Utility Warning", "No Flesch-Kincaid dictionary has been selected.")
        return ""
    if current_prc_terms_directory == "":
        print(current_prc_terms_directory)
        msg.showwarning("Utility Warning", "No path has been provided.")
        return ""
    print(lex_filename)
    print(f_k_filename)
    with open(lex_filename, 'rb') as lexfile:
        lexification_list = pickle.load(lexfile)
    with open(f_k_filename, 'rb') as fkfile:
        new_readability_dictionary = pickle.load(fkfile)
    for cyc_term in lexification_list.keys():
        print(cyc_term)
    progress_max = len(lexification_list)
    progress_bar["maximum"]=progress_max
    i = 0
    for cyc_term in lexification_list.keys():
        output_dict = {}
        for file_name in new_readability_dictionary.keys():
            m = len(current_directory) + 1
            working_file_name = file_name[m:-4] + "-clean.txt"
            print('cd:', current_directory)
            print('fn:', file_name)
            print('wfn:', working_file_name)
            working_stemmed_file = current_stemmed_directory  + "/" + working_file_name
            f_k_value = int(round(new_readability_dictionary[file_name], -1))
            print(m, working_file_name,working_stemmed_file,f_k_value)
            stemmed_file_list = os.listdir(current_stemmed_directory)
            if working_file_name in stemmed_file_list:
                text = open(working_stemmed_file, 'r').read()
                count_dict = {}
                for lexification in lexification_list[cyc_term]:
                    count_dict[lexification] = text.count(lexification)
                count = reconcile(count_dict)
                if f_k_value in output_dict.keys():
                    output_dict[f_k_value] += count
                else:
                    output_dict[f_k_value] = count
        output_list = [cyc_term, output_dict]
        print(output_list)
        new_output_name  = cyc_term[2:]
        new_output_path = current_prc_terms_directory + "/" + new_output_name + "-processed.pickle"
        with open(new_output_path, 'wb') as handle:
            pickle.dump(output_list, handle, protocol =  pickle.HIGHEST_PROTOCOL)
        i += 1
        progress_bar["value"] = i
        progress_bar.update()
    prc_terms_file_name.config(state="normal")
    prc_terms_file_name.delete(0, tk.END)
    prc_terms_file_name.insert(tk.INSERT, current_prc_terms_directory)
    prc_terms_file_name.config(state="disabled")
    sleep(0.75)
    progress_bar["value"] = 0

def make_prc_too():
    print("make_prc")
# LightsOut

def get_url():
    host = name.get()
    port_no = int(port.get()) + 3602
    output = "http://" + host + ":" + str(port_no) + "/cgi-bin/cg?cb-start"
    return output

def lights_out():
    status_text.config(state="normal")
    status_text.delete(0, tk.END)
    status_text.insert(tk.INSERT, "No Good")
    status_text.config(state="disabled")

def lights_on():
    status_text.config(state="normal")
    status_text.delete(0, tk.END)
    status_text.insert(tk.INSERT, "Good")
    status_text.config(state="disabled")

def ping():
    global host
    global port_no
    host = name.get()
    port_no = int(port.get()) + 3602
    output = "http://" + host + ":" + str(port_no) + "/cgi-bin/cg?cb-start"
    print(output)
    try:
        urllib.request.urlopen(output)
        lights_on()
    except urllib.error.HTTPError:
        lights_out()
    except urllib.error.URLError:
        lights_out()


# Lexification Dictionary Tools

def get_lexification_path():
    global new_lexification_directory
    new_lexification_directory_stale = new_lexification_directory
    new_lexification_directory = askdirectory(initialdir="/",
                                     title = "Choose new lexification directory")
    if current_directory != "":
        if new_lexification_directory_stale != new_lexification_directory:
            new_lexification_path.config(state="normal")
            new_lexification_path.delete(0, tk.END)
            new_lexification_path.insert(tk.INSERT, current_directory)
            new_lexification_path.config(state="disabled")
    else:
        new_lexification_directory = new_lexification_directory_stale
        new_lexification_path.config(state = "disabled")

# Get Files

def get_corpus():
    global current_directory
    current_directory_stale = current_directory
    current_directory = askdirectory(initialdir="/",
                                     title = "Choose Gutenberg directory")
    if current_directory != "":
        print(current_directory)
        if current_directory_stale != current_directory:
            corpus_path.config(state="normal")
            corpus_path.delete(0, tk.END)
            corpus_path.insert(tk.INSERT, current_directory)
            corpus_path.config(state="disabled")
    else:
        current_directory = current_directory_stale
        corpus_path.config(state = "disabled")

 
def get_stemmed_corpus():
    global current_stemmed_directory
    current_stemmed_directory_stale = current_stemmed_directory
    current_stemmed_directory = askdirectory(initialdir="/",
                                     title = "Choose stemmed Gutenberg directory")
    if current_stemmed_directory != "":
        if current_stemmed_directory_stale != current_stemmed_directory:
            stemmed_path.config(state="normal")
            stemmed_path.delete(0, tk.END)
            stemmed_path.insert(tk.INSERT, current_stemmed_directory)
            stemmed_path.config(state="disabled")
    else:
        current_stemmed_directory = current_stemmed_directory_stale
        stemmed_path.config(state = "disabled")


 
    
def get_lex_dict():
    global lex_filename
    lex_filename_stale = lex_filename
    lex_filename = askopenfilename(initialdir="/",
                           defaultextension = '.pickle',
                           filetypes =[("Pickle File", "*.pickle"), ('All files', "*.*")],
                           title = "Choose a file"
                           )
    if lex_filename != "":
        if lex_filename_stale != lex_filename:
            lex_dict_file_name.config(state="normal")
            lex_dict_file_name.delete(0, tk.END)
            lex_dict_file_name.insert(tk.INSERT, lex_filename)
            lex_dict_file_name.config(state="disabled")
    else:
        lex_filename = lex_filename_stale
        lex_dict_file_name.config(state="disabled")


def get_f_k_dict():
    global f_k_filename
    f_k_filename_stale = f_k_filename
    f_k_filename = askopenfilename(initialdir="/",
                           defaultextension = '.pickle',
                           filetypes =[("Pickle File", "*.pickle"), ('All files', "*.*")],
                           title = "Choose a file"
                           )
    if f_k_filename != "":
        if f_k_filename_stale != f_k_filename:
            f_k_dict_file_name.config(state="normal")
            f_k_dict_file_name.delete(0, tk.END)
            f_k_dict_file_name.insert(tk.INSERT, f_k_filename)
            f_k_dict_file_name.config(state="disabled")
    else:
        f_k_filename = f_k_filename_stale
        f_k_dict_file_name.config(state="disabled")


def get_prc_terms():
    global current_prc_terms_directory
    current_prc_terms_directory_stale = current_prc_terms_directory
    current_prc_terms_directory = askdirectory(initialdir="/",
                                     title = "Choose processed Cyc terms directory")
    print(current_prc_terms_directory)
    if current_prc_terms_directory != "":
        if current_prc_terms_directory_stale != current_prc_terms_directory:
            create_prc_path_box.config(state="normal")
            create_prc_path_box.delete(0, tk.END)
            create_prc_path_box.insert(tk.INSERT, current_prc_terms_directory)
            create_prc_path_box.config(state="disabled")
    else:
        current_prc_terms_directory = current_prc_terms_directory_stale
        create_prc_path_box.config(state = "disabled")


def choose_stemmed_corpus():
    global create_stemmed_path
    create_stemmed_path_stale = create_stemmed_path
    create_stemmed_path = askdirectory(initialdir="/",
                                     title = "Choose path for stemmed corpus")
    if create_stemmed_path != "":
        if create_stemmed_path_stale != create_stemmed_path:
            create_stemmed_path_box.config(state="normal")
            create_stemmed_path_box.delete(0, tk.END)
            create_stemmed_path_box.insert(tk.INSERT, create_stemmed_path)
            create_stemmed_path_box.config(state="disabled")
    else:
        create_stemmed_path = create_stemmed_path_stale
        create_stemmed_path_box.config(state = "disabled")



def lexifications_path_holder():
    global create_lexifications_path
    create_lexifications_path_stale = create_lexifications_path
    create_lexifications_path = askdirectory(initialdir="/",
                                     title = "Choose path for Cyc lexifications")
    if create_lexifications_path != "":
        if create_lexifications_path_stale != create_lexifications_path:
            create_cyc_lex_box.config(state="normal")
            create_cyc_lex_box.delete(0, tk.END)
            create_cyc_lex_box.insert(tk.INSERT, create_lexifications_path)
            create_cyc_lex_box.config(state="disabled")
    else:
        create_lexifications_path = create_lexifications_path_stale
        create_cyc_lex_box.config(state = "disabled")

def get_new_lexifications_path():
    global create_lexifications_path
    create_lexifications_path_stale = create_lexifications_path
    create_lexifications_path = askdirectory(initialdir="/",
                                     title = "Choose path for lexifications")
    if create_lexifications_path != "":
        if create_lexifications_path_stale != create_lexifications_path:
            create_cyc_lex_box.config(state="normal")
            create_cyc_lex_box.delete(0, tk.END)
            create_cyc_lex_box.insert(tk.INSERT, create_lexifications_path)
            create_cyc_lex_box.config(state="disabled")
    else:
        create_lexifications_path = create_lexifications_path_stale
        create_cyc_lex_box.config(state = "disabled")

        
      
#create_cyc_lex_box
  
def get_f_k_path():
    global create_f_k_path
    create_f_k_path_stale = create_f_k_path
    create_f_k_path = askdirectory(initialdir="/",
                                     title = "Choose path for lexifications")
    if create_f_k_path != "":
        if create_f_k_path_stale != create_f_k_path:
            create_f_k_path_box.config(state="normal")
            create_f_k_path_box.delete(0, tk.END)
            create_f_k_path_box.insert(tk.INSERT, create_f_k_path)
            create_f_k_path_box.config(state="disabled")
    else:
        create_f_k_path = create_f_k_path_stale
        create_f_k_path_box.config(state = "disabled")


def get_prc_path():
    global create_prc_path
    create_prc_path_stale = create_prc_path
    create_prc_path = askdirectory(initialdir="/",
                                     title = "Choose path for Cyc terms")
    if create_prc_path != "":
        if create_prc_path_stale != create_prc_path:
            prc_terms_file_name.config(state="normal")
            prc_terms_file_name.delete(0, tk.END)
            prc_terms_file_name.insert(tk.INSERT, create_prc_path)
            prc_terms_file_name.config(state="disabled")
    else:
        create_prc_path = create_prc_path_stale
        prc_terms_file_name.config(state = "disabled")
        

#====================================================
# Creation Utilities
#====================================================
 

def convert(text):
    text2 = text.split()
    text3 = [stemmer.stem(term.lower()) for term in text2]
    text4 = ' '.join(text3)
    return(text4)

def checkpath(path):
    return(path[-4:] == ".txt" and path[-6:] != "-8.txt" and path[-6:] != "-0.txt" and "old" not in path and "readme" not in path and "index" not in path)

def get_count(path):
    i = 0
    for root, dirs, files in os.walk(current_directory, topdown = False):
        for name in files:
            text_loc = os.path.join(root,name)
            if checkpath(text_loc):
                i = i + 1
    return i

def make_stemmed_corpus():
    global create_stemmed_path
    global current_directory
    print(current_directory)
    print(create_stemmed_path)
    print(type(create_stemmed_path))
    if current_directory == "":
        msg.showwarning("Utility Warning", "No path for Gutenberg corpus has been selected.")
        return ""
    if create_stemmed_path == "":
        msg.showwarning("Utility Warning", "No path for stemmed Gutenberg corpus has been selected.")
        return ""
    stemmed_path.config(state="normal")
    stemmed_path.delete(0, tk.END)
    stemmed_path.insert(tk.INSERT, create_stemmed_path)
    stemmed_path.config(state="disabled")
    print("I'm here")
    progress_max = get_count(current_directory) 
    progress_bar["maximum"]=progress_max
    i = 0
    for root, dirs, files in os.walk(current_directory, topdown = False):
        for name in files:
            text_loc = os.path.join(root,name)
            if checkpath(text_loc):
                print(text_loc)
                try:
                    text0 = open(text_loc, "r").read()
                    print(text_loc)
                    text1 = strip_headers(text0)
                    if detect(text1) == "en":
                        text4 = convert(text1)
                        new_name = create_stemmed_path + "/" + name[0:-4] + '-clean.txt'
                        print(new_name)
                        new_file = open(new_name, 'w')
                        new_file.write(text4)
                        new_file.close()
                        i += 1
                        progress_bar["value"] = i
                        progress_bar.update()
                except:
                    continue
    sleep(0.75)
    progress_bar["value"] = 0

def make_lexifications():
    host_name = name.get()
    port_no = port.get() + 3602
    port_string = str(port_no)
    output = "http://" + host_name + ":" + port_string + "/cgi-bin/cg?cb-start"
    print(output)
    number_of_terms = create_cyc_lex_no_var.get()
    path = create_cyc_lex_var.get()
    titlish = create_cyc_lex_name_var.get()
    progress_bar["maximum"]=3
    if path == "":
        msg.showwarning("Utility Warning", "No path specified.")
        return ""
    if titlish == "":
        msg.showwarning("Utility Warning", "Provide a filename.")
        return "" 
    if titlish == "":
        msg.showwarning("Utility Warning", "Indicate number of terms.")
        return "" 
    try:
        urllib.request.urlopen(output)
        lights_on()
        print("OPEN")
    except urllib.error.HTTPError:
        msg.showwarning("Utility Warning", "Check connection.")
        return ""
    except urllib.error.URLError:
        msg.showwarning("Utility Warning", "Check connection.")
        return ""
    progress_bar["value"] = 1
    progress_bar.update()
    subl_query = "(get-lexification-sets-for-n-concepts " + str(number_of_terms) + ")"
    uri_query = urllib.parse.quote(subl_query)
    header = "http://" + host_name + ":" + port_string + "/cgi-bin/cb-eval-subl?expression=" 
    request = header + uri_query
    print(request)
    progress_bar["value"] = 2
    progress_bar.update()
    content_return = urllib.request.urlopen(request).read()
    soup_return = BeautifulSoup(content_return, "html.parser")
    json_return = json.loads(soup_return.getText())
    returns = json_return["results"]
    returns_string = str(returns)
    returns_string = returns_string[3:-3]
    returns_string = returns_string.replace("\\'", "\'")
    returns_dict = eval(returns_string)
    progress_bar["value"] = 3
    progress_bar.update()
    file_name = path + "/" + titlish + '.pickle'
    with open(file_name, 'wb') as handle:
        pickle.dump(returns_dict, handle, protocol =  pickle.HIGHEST_PROTOCOL)
    sleep(0.75)
    progress_bar["value"] = 0  

   

def flesch_kincaidizer(gutenberg_path, pickle_dump_path):
    output_dict = {}
    for root, dirs, files in os.walk(gutenberg_path, topdown = False):
        for name in files:
            text_loc = os.path.join(root,name)
            if name[-4:] == ".txt" and name[-6:] != "-8.txt" and name[-6:] != "-0.txt" and "old" not in text_loc:
                i += 1
                progress_bar["value"] = i
                progress_bar.update()
                try:
                    text0 = open(text_loc, "r").read()
                    text1 = strip_headers(open(text_loc,"r").read())
                    if detect(text1) == "en":
                        text2 = Textatistic(text1)
                        output_dict[text_loc] = text2.fleschkincaid_score
                        print(text_loc, output_dict[text_loc])
                except:
                    continue
    os.chdir(pickle_dump_path)
    with open('readability_dictionary.pickle', 'wb') as handle:
        pickle.dump(output_dict, handle, protocol =  pickle.HIGHEST_PROTOCOL)
    sleep(0.75)
    progress_bar["value"] = 0   

def create_f_k_dict():
    global current_directory
    file_name = create_f_k_name_var.get()
    path_name = create_f_k_path_var.get()
    file_path = path_name + "/" + file_name + ".pickle"
    if current_directory == "":
        msg.showwarning("Utility Warning", "No Gutenberg corpus specified.")
        return ""
    if file_name == "":
        msg.showwarning("Utility Warning", "Provide a filename.")
        return "" 
    if path_name == "":
        msg.showwarning("Utility Warning", "Provide a path for Flesch-Kincaid dictionary.")
        return ""
    output_dict = {}
    progress_max = get_count(current_directory) 
    progress_bar["maximum"] = progress_max
    i = 0    
    print(i)
    for root, dirs, files in os.walk(current_directory, topdown = False):
        for name in files:
            text_loc = os.path.join(root,name)
            if checkpath(name):
                try:
                    text0 = open(text_loc, "r").read()
                    text1 = strip_headers(open(text_loc,"r").read())
                    if detect(text1) == "en":
                        text2 = Textatistic(text1)
                        output_dict[text_loc] = text2.fleschkincaid_score
                        print(text_loc, output_dict[text_loc])
                        i += 1
                        progress_bar["value"] = i
                        progress_bar.update()
                except:
                    continue
    print(output_dict)
    with open(file_path, 'wb') as handle:
        pickle.dump(output_dict, handle, protocol =  pickle.HIGHEST_PROTOCOL) 
    f_k_dict_file_name.config(state="normal")
    f_k_dict_file_name.delete(0, tk.END)
    f_k_dict_file_name.insert(tk.INSERT, file_path)
    f_k_dict_file_name.config(state="disabled")
    sleep(0.75)
    progress_bar["value"] = 0  



# Fix f_k_filename
        
    
# Create lexifications function



#====================================================
# Create GUI
#====================================================

# Create instance

gui = tk.Tk()


gui.title("Hyperintensionality Utilities v.1")

# Enable resizing

gui.resizable(False,False)


# Create Tabs

tabControl = ttk.Notebook(gui)
configure_tab = ttk.Frame(tabControl)
tabControl.add(configure_tab, text = 'Import')
construct_tab = ttk.Frame(tabControl)
tabControl.add(construct_tab, text = 'Create')
visualize_tab = ttk.Frame(tabControl)
tabControl.add(visualize_tab, text = 'Visualize')


tabControl.pack(expand=1, fill="both")









#=======================================
# Configure Tab
#=======================================





prepare = ttk.LabelFrame(configure_tab, text = " Cyc Connection ")
prepare.grid(column=0, row=0, padx=4, pady=4, sticky = "EW")


corpus = ttk.LabelFrame(configure_tab, text = " Gutenberg Corpus")
corpus.grid(column=0, row=2, padx=4, pady=4, sticky = "EW")


stemmed = ttk.LabelFrame(configure_tab, text = " Stemmed Corpus")
stemmed.grid(column=0, row=4, padx=4, pady=4, sticky = "EW")

lex_dict = ttk.LabelFrame(configure_tab, text = " Lexifications Dictionary ")
lex_dict.grid(column=0, row=6, padx=4, pady=4, sticky = "EW")


f_k_dict = ttk.LabelFrame(configure_tab, text = " Flesch-Kincaid Dictionary ")
f_k_dict.grid(column=0, row=8, padx=4, pady=4, sticky = "EW")


prc_terms = ttk.LabelFrame(configure_tab, text = " Processed Cyc Terms Path")
prc_terms.grid(column=0, row=10, padx=4, pady=4)



# Get Host


ttk.Label(prepare, text="Host").grid(column=0,row=0)

name = tk.StringVar()
name_entered = ttk.Entry(prepare, width=18, textvariable=name)
name_entered.grid(column=0, row=1)

# Get Port

ttk.Label(prepare, text="Port").grid(column=1, row=0)

port = tk.IntVar()
port_chosen = ttk.Combobox(prepare, width=12, textvariable=port, state= "readonly")
port_chosen['values'] = ("00",20,40,60,80)
port_chosen.grid(column=1,row=1)
port_chosen.current(0)


# Display Status

ttk.Label(prepare, text="Status").grid(column=2, row=0)

status = tk.StringVar()
status_text = ttk.Entry(prepare, width=12, textvariable=status, state = "disabled")
status_text.grid(column=2,row=1)
lights_out()




# Check Status Button

check_button = ttk.Button(prepare, text="Check Status", command = ping)
check_button.grid(column=3, row=1)



# Obtain Corpus




ttk.Label(corpus, text="  Gutenberg Corpus Path").grid(column=0,row=0, sticky="W")

corpus_var = tk.StringVar()
corpus_path = ttk.Entry(corpus, width=54, textvariable=corpus_var)
corpus_path.grid(column=0, row=1)

corpus_path.config(state="normal")
corpus_path.insert(tk.INSERT, current_directory)
corpus_path.config(state="disabled")

# Get Corpus Button

corpus_button = ttk.Button(corpus, text="Load", command = get_corpus)
corpus_button.grid(column=3, row=1)




# Obtain Stemmed Corpus




ttk.Label(stemmed, text="  Stemmed Gutenberg Corpus Path").grid(column=0,row=0, sticky="W")

stemmed_var = tk.StringVar()
stemmed_path = ttk.Entry(stemmed, width=54, textvariable=stemmed_var)
stemmed_path.grid(column=0, row=1)
stemmed_path.config(state="disabled")

# Get Corpus Button

stemmed_button = ttk.Button(stemmed, text="Load", command = get_stemmed_corpus)
stemmed_button.grid(column=3, row=1)


# Obtain Lexifications Dictionary




ttk.Label(lex_dict, text="  Lexifications Dictionary").grid(column=0,row=0, sticky="W")

lex_dict_var = tk.StringVar()
lex_dict_file_name = ttk.Entry(lex_dict, width=54, textvariable=lex_dict_var)
lex_dict_file_name.grid(column=0, row=1)
lex_dict_file_name.config(state="disabled")

# Get Lexification Dictionary Button

lex_dict_button = ttk.Button(lex_dict, text="Load", command = get_lex_dict)
lex_dict_button.grid(column=3, row=1)





# Obtain Flesch-Kincaid Dictionary




ttk.Label(f_k_dict, text="  Flesch-Kincaid Dictionary").grid(column=0,row=0, sticky="W")

f_k_dict_var = tk.StringVar()
f_k_dict_file_name = ttk.Entry(f_k_dict, width=54, textvariable=f_k_dict_var)
f_k_dict_file_name.grid(column=0, row=1)
f_k_dict_file_name.config(state="disabled")

# Get Flesch-Kincaid Dictionary Button

f_k_dict_button = ttk.Button(f_k_dict, text="Load", command = get_f_k_dict)
f_k_dict_button.grid(column=3, row=1)



# Obtain Analyzed Cyc Terms




ttk.Label(prc_terms, text="  Analyzed Cyc Terms").grid(column=0,row=0, sticky="W")

prc_terms_var = tk.StringVar()
prc_terms_file_name = ttk.Entry(prc_terms, width=54, textvariable=prc_terms_var)
prc_terms_file_name.grid(column=0, row=1)
prc_terms_file_name.config(state="disabled")

# Get Flesch-Kincaid Dictionary Button

prc_terms_dict_button = ttk.Button(prc_terms, text="Load", command = get_prc_path)
prc_terms_dict_button.grid(column=3, row=1)




#=======================================
# Construct Tab
#=======================================


create_stemmed = ttk.LabelFrame(construct_tab, text = " Stem Corpus ")
create_stemmed.grid(column=0, row=0, padx=4, pady=4, sticky = "EW")


create_lex = ttk.LabelFrame(construct_tab, text = " Create Lexifications Dictionary")
create_lex.grid(column=0, row=2, padx=4, pady=4, sticky = "EW")

create_f_k = ttk.LabelFrame(construct_tab, text = " Create Flesch-Kincaid Dictionary")
create_f_k.grid(column=0, row=3, padx=4, pady=4, sticky = "EW")

create_process = ttk.LabelFrame(construct_tab, text = " Process Cyc Lexifications")
create_process.grid(column=0, row=4, padx=4, pady=4, sticky = "EW")


# Create Stemmed Corpus

ttk.Label(create_stemmed, text="  Stemmed Gutenberg Corpus Path").grid(column=0,row=0, sticky="W")

create_stemmed_var = tk.StringVar()
create_stemmed_path_box = ttk.Entry(create_stemmed, width=54, textvariable=create_stemmed_var)
create_stemmed_path_box.grid(column=0, row=1)
create_stemmed_path_box.config(state="disabled")

# Choose Stem Corpus Button

choose_new_stemmed_button = ttk.Button(create_stemmed, text="Load", command = choose_stemmed_corpus)
choose_new_stemmed_button.grid(column=3, row=1)

# Choose Stem Corpus Button
ttk.Label(create_stemmed, text="").grid(column=3,row=2, sticky="W")

make_new_stemmed_button = ttk.Button(create_stemmed, text="Create", command = make_stemmed_corpus)
make_new_stemmed_button.grid(column=3, row=3)




# Create Cyc Lexification Dictionary Path

ttk.Label(create_lex, text="  Cyc Lexifications Path").grid(column=0,row=0, sticky="W")

create_cyc_lex_var = tk.StringVar()
create_cyc_lex_box = ttk.Entry(create_lex, width=54, textvariable=create_cyc_lex_var)
create_cyc_lex_box.grid(column=0, row=1)
create_cyc_lex_box.config(state="disabled")

# Choose Stem Corpus Button

lexification_path = ttk.Button(create_lex, text="Load", command = get_new_lexifications_path)
lexification_path.grid(column=3, row=1)

#Choose Cyc Lexification Dictionary Name

ttk.Label(create_lex, text="  Filename").grid(column=0,row=2, sticky="W")
create_cyc_lex_name_var = tk.StringVar()
create_cyc_lex_name_box = ttk.Entry(create_lex, width=54, textvariable=create_cyc_lex_name_var)
create_cyc_lex_name_box.grid(column=0, row=3)

# Choose Cyc Lexification Dictionary Number

ttk.Label(create_lex, text="  Number of Terms").grid(column=0,row=4, sticky="W")
create_cyc_lex_no_var = tk.StringVar()
create_cyc_lex_no_box = ttk.Entry(create_lex, width=14, textvariable=create_cyc_lex_no_var)
create_cyc_lex_no_box.grid(column=0, row=5 , sticky="W")


# Choose Stem Corpus Button

make_lexifications = ttk.Button(create_lex, text="Create", command = make_lexifications)
make_lexifications.grid(column=3, row=3)



# Create Flesch-Kincaid Dictionary Path

ttk.Label(create_f_k, text="  Flesch-Kincaid Dictionary Path").grid(column=0,row=0, sticky="W")

create_f_k_path_var = tk.StringVar()
create_f_k_path_box = ttk.Entry(create_f_k, width=54, textvariable=create_f_k_path_var)
create_f_k_path_box.grid(column=0, row=1)
create_f_k_path_box.config(state="disabled")

# Choose Flesch-Kincaid Path Button

f_k_path = ttk.Button(create_f_k, text="Load", command = get_f_k_path)
f_k_path.grid(column=3, row=1)

# Choose Flesch-Kincaid Filename

ttk.Label(create_f_k, text="  Filename").grid(column=0,row=2, sticky="W")
create_f_k_name_var = tk.StringVar()
create_f_k_name_box = ttk.Entry(create_f_k, width=54, textvariable=create_f_k_name_var)
create_f_k_name_box.grid(column=0, row=3)

# Create Flesch-Kincaid Button

new_f_k_path = ttk.Button(create_f_k, text="Create", command = create_f_k_dict)
new_f_k_path.grid(column=3, row=3)


# Create Processed Cyc Terms Path

ttk.Label(create_process, text="  Processed Cyc Terms Path").grid(column=0,row=0, sticky="W")

create_prc_path_var = tk.StringVar()
create_prc_path_box = ttk.Entry(create_process, width=54, textvariable=create_prc_path_var)
create_prc_path_box.grid(column=0, row=1)
create_prc_path_box.config(state="disabled")

# Choose Processed Cyc Terms Path Button

prc_path_button = ttk.Button(create_process, text="Load", command = get_prc_terms)
prc_path_button.grid(column=3, row=1)

# Create Processed Cyc Terms

ttk.Label(create_process, text="").grid(column=3,row=2, sticky="W")
make_new_prc_button = ttk.Button(create_process, text="Create", command = make_prc)
make_new_prc_button.grid(column=3, row=3)

# Make ProgressBar

progress_bar = ttk.Progressbar(construct_tab, orient = "horizontal", length = 410, mode = "determinate")
progress_bar.grid(column = 0, row = 5, pady = 4, columnspan = 4)


# Exit GUI

def _quit():
    gui.quit()
    gui.destroy()
    exit()

# Add menu bar

menu_bar = Menu(gui)
gui.config(menu = menu_bar)

# Add exit menu

file_menu = Menu(menu_bar, tearoff = 0)
#file_menu.add_command(label = "Configure", command = _configure)
file_menu.add_command(label = "Exit", command = _quit)
menu_bar.add_cascade(label= "File", menu = file_menu)


about_menu = Menu(menu_bar, tearoff = 0)
about_menu.add_command(label = "About")
menu_bar.add_cascade(label= "About", menu = about_menu)


name_entered.focus()

#=================================================
# Start GUI
#=================================================


gui.mainloop()

