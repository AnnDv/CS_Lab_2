from tkinter import *
from tkinter import filedialog
import json

root = Tk()
root.title('Laboratory 2')
root.geometry('1200x660')

global selected
selected = False

start_match = []
end_match = []
word_index = 0
custom_items_used = []
jsons_no = 0
to_json = {}
extension = ''
current_file = ''


# new file function
def new_file():
    # clear previous text
    my_text.delete('1.0', END)

    # update status bars
    root.title('New File')
    status_bar.config(text='New File       ')


# cut text
def cut_text(e):
    global selected
    # check if keyboard shortcut was used
    if e:
        selected = root.clipboard_get()
    elif my_text.selection_get():
        # grab selected text from textbox
        selected = my_text.selection_get()
        # delete selected text from textbox
        my_text.delete("sel.first", "sel.last")
        # clear clipboard then append
        root.clipboard_clear()
        root.clipboard_append(selected)


# copy text
def copy_text(e):
    global selected
    # check if keyboard shortcut was used
    if e:
        selected = root.clipboard_get()
    if my_text.selection_get():
        # grab selected text from textbox
        selected = my_text.selection_get()
        # clear clipboard then append
        root.clipboard_clear()
        root.clipboard_append(selected)


# paste text
def paste_text(e):
    global selected
    # check if keyboard shortcut was used
    if e:
        selected = root.clipboard_get()
    elif selected:
        position = my_text.index(INSERT)
        my_text.insert(position, selected)


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)
        # use start += 1 to find overlapping matches


# open file function
def open_file():
    global jsons_no
    global to_json
    global extension
    global current_file

    # clear previous text
    my_text.delete('1.0', END)

    # get file name
    text_file = filedialog.askopenfilename(
        initialdir='lab2/Audit Files',
        title='Open File', filetypes=(('All Files', '*.*'),))
    
    current_file = text_file

    # update status bars
    name = text_file
    status_bar.config(text=f'{name}       ')
    name = name.replace('lab2/', '')
    root.title(f'{name} - Dvorac Ana')

    extension = ''
    i = len(name) - 1
    while name[i] != '.':
        extension += name[i]
        i -= 1
    extension = extension[::-1]

    # open file
    if extension == 'audit':
        text_file = open(text_file, 'r')
        contents = text_file.read()

        contents = contents.replace('            :', ':')
        contents = contents.replace('           :', ':')
        contents = contents.replace('          :', ':')
        contents = contents.replace('         :', ':')
        contents = contents.replace('        :', ':')
        contents = contents.replace('       :', ':')
        contents = contents.replace('      :', ':')
        contents = contents.replace('     :', ':')
        contents = contents.replace('    :', ':')
        contents = contents.replace('   :', ':')
        contents = contents.replace('  :', ':')
        contents = contents.replace(' :', ':')

        start = list(find_all(contents, '<custom_item>'))
        ending = list(find_all(contents, '</custom_item>'))

        custom_item = {}

        custom_item['CMD_EXEC'] = {'type': [], 'description': [], 'cmd': [], 'expect': []}
        custom_item['MACOSX_DEFAULTS_READ'] = {'type': [], 'description': [], 'regex': [], 'plist_item': [], 'plist_name ': [], 'plist_option': []}
        custom_item['FILE_CONTENT_CHECK'] = {'type': [], 'description': []}
        custom_item['FILE_CONTENT'] = {'type': [], 'description': []}
        custom_item['FILE_CONTENT_CHECK_NOT'] = {'type': [], 'description': []}
        custom_item['BANNER_CHECK'] = {'type': [], 'description': []}
        
        general_custom_item = {}
        general_custom_item_keys = []

        for key in custom_item:
            keys_list = list(custom_item[key])
            for key_x in keys_list:
                if key_x not in general_custom_item_keys:
                    general_custom_item_keys.append(key_x)

        general_custom_item['custom_item_number'] = []

        for key in general_custom_item_keys:
            general_custom_item[key] = []

        general_custom_item['type'] = []
        general_custom_item['info'] = []
        general_custom_item['description'] = []
        general_custom_item['see_also'] = []

        for i in range(len(start)):
                content_type_block = contents[start[i] + 13: ending[i]]
                general_custom_item['custom_item_number'].append(i)
                for element in list(general_custom_item.keys()):
                    element_length = len(element) + 1
                    if content_type_block.find(element) != -1:
                        general_custom_item[element].append(content_type_block[content_type_block.find(
                            element + ':') + element_length: content_type_block[content_type_block.find(
                            element + ':') + element_length:].find('\n') + content_type_block.find(
                            element + ':') + element_length].strip())
                    else:
                        if element != 'custom_item_number':
                            general_custom_item[element].append('')
                            
        jsons_no = len(general_custom_item['custom_item_number'])

        to_json = []
        for i in range(len(general_custom_item['type'])):
            to_print = {}
            for element in list(general_custom_item.keys()):
                if general_custom_item[element][i] != '':
                    to_print[element] = general_custom_item[element][i]
            to_json.append(to_print)

        my_text.insert(END, json.dumps(to_json, indent=4))

        # close file
        text_file.close()

    elif extension == 'json':

        text_file = open(text_file, 'r')
        to_json = json.load(text_file)
        jsons_no = len(to_json)
        my_text.insert(END, json.dumps(to_json, indent=4))
        text_file.close()

def save():
    global jsons_no
    global to_json
    global extension

    def check():
        global custom_items_used
        global jsons_no
        global to_json
        global extension
        global current_file

        custom_items_used = []

        for i in range(len(check_btns)):
            if var[i].get() == 1:
                custom_items_used.append(i)

        root_checkbox.destroy()

        if extension == 'audit':
            text_file = filedialog.asksaveasfilename(defaultextension='.*', initialdir='lab2/Audit Files/',
                                                     title='Save File', filetypes=(('All Files', '*.*'),))
        elif extension == 'json':
            text_file = current_file

        if text_file:
            # update status bars
            name = text_file
            status_bar.config(text=f'{name}       ')
            name = name.replace('lab2/Audit Files/', '')
            root.title(f'{name} - ')

            to_print = []
            for i in custom_items_used:
                to_print.append(to_json[i])

            # save file
            text_file = open(text_file, 'w')
            json.dump(to_print, text_file, indent=4)

            # close file
            text_file.close()

            if extension == 'json':
                new_file()
                text_file = current_file
                text_file = open(text_file, 'r')
                to_json = json.load(text_file)
                jsons_no = len(to_json)
                my_text.insert(END, json.dumps(to_json, indent=4))

                # close file
                text_file.close()


    def select_all():
        for i in range(len(check_btns)):
            var[i].set(1)

    def select_none():
        for i in range(len(check_btns)):
            var[i].set(0)

    root_checkbox = Tk()
    root_checkbox.title('Select the desired custom items')

    # scrollbar for checkbox
    checkbox_scroll = Scrollbar(root_checkbox, orient='vertical')
    checkbox_scroll.pack(side=RIGHT, fill=Y)

    checkbox_txt = Text(root_checkbox, width=80, height=50, yscrollcommand=checkbox_scroll.set)

    # configure scrollbar
    checkbox_scroll.config(command=checkbox_txt.yview)

    var = []
    for i in range(jsons_no):
        var.append(IntVar(root_checkbox))
    checkbox_txt.pack(side=TOP, fill=BOTH, expand=True)
    check_btns = [Checkbutton(root_checkbox, text="custom item № %s" % i,
                                variable=var[i], onvalue=1, offvalue=0, )
                    for i in range(jsons_no)]
    for chk_btn in check_btns:
        checkbox_txt.window_create('end', window=chk_btn)
        checkbox_txt.insert('end', '\n')

    # submit button
    submit_btn = Button(root_checkbox, text='Submit')
    submit_btn.pack(side=BOTTOM)
    submit_btn.config(command=check)

    # select all button
    select_all_btn = Button(root_checkbox, text='Select All')
    select_all_btn.pack(side=TOP)
    select_all_btn.config(command=select_all)

    # select none button
    select_none_btn = Button(root_checkbox, text='Deselect All')
    select_none_btn.pack(side=TOP)
    select_none_btn.config(command=select_none)

    root_checkbox.mainloop()

# save as file function
def save_as_file():
    global jsons_no
    global to_json
    global extension

    def check():
        global custom_items_used
        global jsons_no
        global to_json
        global extension
        global current_file

        custom_items_used = []
        for i in range(len(check_btns)):
            if var[i].get() == 1:
                custom_items_used.append(i)
        root_checkbox.destroy()

        text_file = filedialog.asksaveasfilename(
            defaultextension='.*',
            initialdir='lab2/Audit Files/',
            title='Save File', filetypes=(('All Files', '*.*'),))

        if text_file:
            # update status bars
            name = text_file
            status_bar.config(text=f'{name}       ')
            name = name.replace('lab2/Audit Files/', '')
            root.title(f'{name} - Dvorac Ana')

            to_print = []
            for i in custom_items_used:
                to_print.append((to_json[i]))

            text_file = open(text_file, 'w')
            json.dump(to_print, text_file, indent=4)

            text_file.close()
    
    def select_all():
        for i in range(len(check_btns)):
            var[i].set(1)

    def select_none():
        for i in range(len(check_btns)):
            var[i].set(0)

    root_checkbox = Tk()
    root_checkbox.title('Select the desired custom items')

    # scrollbar for checkbox
    checkbox_scroll = Scrollbar(root_checkbox, orient='vertical')
    checkbox_scroll.pack(side=RIGHT, fill=Y)

    checkbox_txt = Text(root_checkbox, width=80, height=50, yscrollcommand=checkbox_scroll.set)

    # configure scrollbar
    checkbox_scroll.config(command=checkbox_txt.yview)

    var = []
    for i in range(jsons_no):
        var.append(IntVar(root_checkbox))
    checkbox_txt.pack(side=TOP, fill=BOTH, expand=True)
    check_btns = [Checkbutton(root_checkbox, text="custom item № %s" % i,
                              variable=var[i], onvalue=1, offvalue=0, )
                  for i in range(jsons_no)]
    for chk_btn in check_btns:
        checkbox_txt.window_create('end', window=chk_btn)
        checkbox_txt.insert('end', '\n')

    # submit button
    submit_btn = Button(root_checkbox, text='Submit')
    submit_btn.pack(side=BOTTOM)
    submit_btn.config(command=check)

    # select all button
    select_all_btn = Button(root_checkbox, text='Select All')
    select_all_btn.pack(side=TOP)
    select_all_btn.config(command=select_all)

    # select none button
    select_none_btn = Button(root_checkbox, text='Deselect All')
    select_none_btn.pack(side=TOP)
    select_none_btn.config(command=select_none)

    root_checkbox.mainloop()

def export():
    global jsons_no
    global to_json
    global extension

    def check():
        global custom_items_used
        global jsons_no
        global to_json
        global extension
        global current_file

        custom_items_used = []
        for i in range(len(check_btns)):
            if var[i].get() == 1:
                custom_items_used.append(i)
        root_checkbox.destroy()

        text_file = filedialog.asksaveasfilename(
            defaultextension='.*',
            initialdir='lab2/Audit Files/',
            title='Save File', filetypes=(('All Files', '*.*'),))

        if text_file:
            # update status bars
            name = text_file
            status_bar.config(text=f'{name}      ')
            name = name.replace('lab2/Audit Files/', '')
            root.title(f'{name} - Dvorac Ana')

        text_file = open(text_file, 'w')

        to_print = []
        for i in custom_items_used:
            text_file.write('<custom_item>\n')
            for j in to_json[i]:
                text_file.write('\t' + j + ' : ' + str(to_json[i][j]) + '\n')
                text_file.write('</custom_item>\n')

                # close file
            text_file.close()

    def select_all():
        for i in range(len(check_btns)):
            var[i].set(1)

    def select_none():
        for i in range(len(check_btns)):
            var[i].set(0)

    root_checkbox = Tk()
    root_checkbox.title('Select the desired custom items')

    # scrollbar for checkbox
    checkbox_scroll = Scrollbar(root_checkbox, orient='vertical')
    checkbox_scroll.pack(side=RIGHT, fill=Y)

    checkbox_txt = Text(root_checkbox, width=80, height=50, yscrollcommand=checkbox_scroll.set)

    # configure scrollbar
    checkbox_scroll.config(command=checkbox_txt.yview)
    var = []
    for i in range(jsons_no):
        var.append(IntVar(root_checkbox))
    checkbox_txt.pack(side=TOP, fill=BOTH, expand=True)
    check_btns = [Checkbutton(root_checkbox, text="custom item № %s" % i,
                              variable=var[i], onvalue=1, offvalue=0, )
                  for i in range(jsons_no)]
    for chk_btn in check_btns:
        checkbox_txt.window_create('end', window=chk_btn)
        checkbox_txt.insert('end', '\n')

    # submit button
    submit_btn = Button(root_checkbox, text='Submit')
    submit_btn.pack(side=BOTTOM)
    submit_btn.config(command=check)

    # select all button
    select_all_btn = Button(root_checkbox, text='Select All')
    select_all_btn.pack(side=TOP)
    select_all_btn.config(command=select_all)

    # select none button
    select_none_btn = Button(root_checkbox, text='Deselect All')
    select_none_btn.pack(side=TOP)
    select_none_btn.config(command=select_none)
    root_checkbox.mainloop()


# update listbox function
def update(data):
    # clear listbox
    entry_list.delete(0, END)

    # add entry to listbox
    for item in data:
        entry_list.insert(END, item)


# fill search abr with suggestion on click
def fillout(e):
    # clear searchbar entry
    search_bar.delete(0, END)

    # add entry to the searchbar on click
    search_bar.insert(0, entry_list.get(ANCHOR))

# searchbar entry checker against listbox entries
def check_entry(e):
    # get searchbar entry
    typed = search_bar.get()

    if typed == '':
        data = suggestion_listing
    else:
        data = []
        for item in suggestion_listing:
            if typed.lower() in item.lower():
                data.append(item)

    # update listbox
    update(data)

def find():
    global start_match
    global end_match
    global word_index

    start_match = []
    end_match = []
    word_index = 0

    my_text.tag_remove('found', '1.0', END)

    searched_word = search_bar.get()

    if searched_word:
        index = '1.0'
        while 1:
            index = my_text.search(searched_word, index, nocase=1, stopindex=END)
            if not index: break

            start_match.append(index)

            last_index = '%s+%dc' % (index, len(searched_word))
            end_match.append(last_index)

            index = last_index

        next_word()

def next_word():
    global word_index
    global start_match
    global end_match

    if word_index < len(start_match):
        my_text.tag_remove('found', '1.0', END)
        index = start_match[word_index]
        last_index = end_match[word_index]
        my_text.tag_add('found', index, last_index)
        to_see = int(index[0:index.find('.')])
        my_text.yview(to_see - 10)
        if word_index < (len(start_match) - 1):
            word_index += 1
        my_text.tag_config('found', foreground='black', background='red')

def previous_word():
    global word_index
    global start_match
    global end_match

    if word_index >= 0:
        my_text.tag_remove('found', '1.0', END)
        index = start_match[word_index]
        last_index = end_match[word_index]
        my_text.tag_add('found', index, last_index)
        to_see = int(index[0:index.find('.')])
        my_text.yview(to_see - 10)
        if word_index > 0:
            word_index -= 1
        my_text.tag_config('found', foreground='black', background='red')

# main_frame = Frame(root)

# entry box and configuration
search_bar = Entry(root, font=("Helvetica", 12))
search_bar.pack(ipady=5, ipadx=100)

# direct input focus setup
search_bar.focus_set()

# find button
search_btn = Button(search_bar, text='Find')
search_btn.pack(side=RIGHT)
search_btn.config(command=find)

# go next and go back buttons
next_button = Button(search_bar, text='Next')
next_button.pack(side=RIGHT)
next_button.config(command=next_word)
back_button = Button(search_bar, text='Previous')
back_button.pack(side=RIGHT)
back_button.config(command=previous_word)

# listbox
entry_list = Listbox(root, width=50)
entry_list.pack(pady=10)

# suggestion list
suggestion_listing = ["password", "type", "description", "check_type", "value_type", "value_data"]
update(suggestion_listing)

# listbox bindings
entry_list.bind("<KeyRelease>", check_entry)

# main_frame.pack(side=TOP)

# main frame
my_frame = Frame(root)
my_frame.pack(pady=5)

# text box scrollbar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)

# horizontal scrollbar
hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)

# text box
my_text = Text(my_frame, width=97, height=25, font=("Helvetica", 16),
               selectbackground="yellow", selectforeground="black",
               undo=True, yscrollcommand=text_scroll.set, wrap="none",
               xscrollcommand=hor_scroll.set)
my_text.pack()

# configure scrollbar
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)
# menu
my_menu = Menu(root)
root.config(menu=my_menu)

# file menu
file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save')
file_menu.add_command(label='Save As', command=save_as_file)
file_menu.add_command(label='Export', command=export)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)

# edit menu
edit_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label='Edit', menu=edit_menu)
edit_menu.add_command(label='Cut', command=lambda: cut_text(False), accelerator="(Ctrl+X)")
edit_menu.add_command(label='Copy', command=lambda: copy_text(False), accelerator="(Ctrl+C)")
edit_menu.add_command(label='Paste', command=lambda: paste_text(False), accelerator="(Ctrl+V)")
edit_menu.add_separator()
edit_menu.add_command(label='Undo', command=my_text.edit_undo, accelerator="(Ctrl+Z)")
edit_menu.add_command(label='Redo', command=my_text.edit_redo, accelerator="(Ctrl+Y)")

# bottom status bar
status_bar = Label(root, text='Ready     ', anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=15)

# edit bindings
root.bind('<Control-Key-x>', cut_text)
root.bind('<Control-Key-c>', copy_text)
root.bind('<Control-Key-v>', paste_text)

root.mainloop()