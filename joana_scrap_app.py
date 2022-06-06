#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# # SCRAPPING JOANA&VOUS 
import joana_scrap_class
import lib_display as ds
import sys
# Import view func tkinter 
import tkinter as tkt
import webbrowser

joana = joana_scrap_class.Scrap()

try:
    joana.initAppScrapping()
except:
    print(">> Scrap init error")
else:
    print('>> Loading recettes file and init portions...')
    joana.initRecettesDatas()
    print('Init ok')

#joana.scrapCurrentWeek()
#joana.showMeals()
#joana.showIngredients()
#joana.updatePortions()
#joana.printIngredientsInFile()


# In[ ]:


# APP VIEW

shop_url = 'https://www.intermarche.com/accueil'
bg_clr = '#41B77F'
txt_clr = 'white'
gtry = '1080x720'
min_size_L = 480
min_size_H = 360
logo_ico = 'logo.ico'
border = 1
   
# hide a frame
def hideFrame():
    frame_content.pack_forget()
    
# show the liste of meals in the menu of the week
def viewMenu():
    text = joana.showMeals()
    text_to_show.set(text)

# change portions of meals
def changePortions():
    #joana.updatePortions()
    frame_buttons.pack_forget()
    frame_content.pack_forget()
    frame_change.pack(expand=1)
    app_to_show.set('Change your portions')
        
# show the list of all necessary ingredients
def viewIngredients():
    frame_buttons.pack_forget()
    text = joana.showIngredients()
    text_to_show.set(text)
    frame_buttons.pack(expand=1)

# force te API scrapping
def forceScrap():  
    frame_buttons.pack_forget()
    text = joana.scrapCurrentWeek()
    print('>>>   Semaine scrappée')
    frame_buttons.pack(expand=1)

# export the list of all necessary ingredients
def exportIngredients():  
    text = joana.printIngredientsInFile()
    print('>>>   Ingrédients ajoutés au fichier de la semaine')
    text_to_show.set(text)

# open the shop webpage
def openShop(url=shop_url):
    webbrowser.open_new(url)

# Create the window
window = tkt.Tk()

# open the shop webpage
def stopApp(w=window):
    window.destroy
    sys.exit(0)
# def text():
#     frame_buttons.delete(0, END)
#     frame_buttons.insert(0, 'Hello world')

# Create the navigation bar
nav_bar = tkt.Menu(window)
opt_nav=tkt.Menu(nav_bar, tearoff=0)
opt_nav.add_command(label='Scrap /!\\', command=forceScrap)
opt_nav.add_command(label='Imprimer', command=viewIngredients)
opt_nav.add_command(label='Quitter', command=stopApp)
nav_bar.add_cascade(label="Options", menu=opt_nav)

# Configure the window
window.title("Je t'aime mon âme d'am°°°")
window.geometry(gtry)
window.minsize(min_size_L, min_size_H)
#window.iconbitmap("logo.ico")
window.config(menu=nav_bar, background=bg_clr, bd=1, relief='sunken')

scrollbar = tkt.Scrollbar(window)


# Create the frames
frame_title = tkt.Frame(window, bd=border,bg=bg_clr)
frame_buttons = tkt.Frame(window, bd=border, bg=bg_clr)
frame_change = tkt.Frame(window, bd=border, bg=bg_clr)
frame_content = tkt.Canvas(window, yscrollcommand=scrollbar.set, bd=border, bg=bg_clr)

scrollbar.pack(side='right', fill='y')
scrollbar.config(command=frame_content.yview )


# Add texts
label_title = tkt.Label(frame_title, text='Menu de la semaine', font=("Arial", 30), bd=border, bg=bg_clr, fg=txt_clr)
label_subtitle = tkt.Label(frame_title, text='Hello Judith', font=("Arial", 20), bd=border, bg=bg_clr, fg=txt_clr)
label_change = tkt.Label(frame_change, text='Change', font=("Arial", 20), bd=border, bg=bg_clr, fg=txt_clr)

text_to_show = tkt.StringVar()
text_to_show.set('Affichage')

app_to_show = tkt.StringVar()
app_to_show.set('My changing app')

label_changing = tkt.Label(frame_change, textvariable=app_to_show, font=("Arial", 20), bd=border, bg=bg_clr, fg=txt_clr)
label_content = tkt.Label(frame_content, textvariable=text_to_show, font=("Arial", 20), bd=border, bg=bg_clr, fg=txt_clr)

# Add buttons
menu_button = tkt.Button(frame_buttons, 
                        text=joana.OPTIONS[1], font=("Arial", 20), relief='groove', bd=border, bg=bg_clr, fg=txt_clr, 
                        command=viewMenu)
change_button = tkt.Button(frame_buttons, 
                        text=joana.OPTIONS[2], font=("Arial", 20), relief='groove', bd=border, bg=bg_clr, fg=txt_clr, 
                        command=changePortions)
ingredients_button = tkt.Button(frame_buttons, 
                        text=joana.OPTIONS[3], font=("Arial", 20), relief='groove', bd=border, bg=bg_clr, fg=txt_clr, 
                        command=viewIngredients)
export_button = tkt.Button(frame_buttons, 
                        text=joana.OPTIONS[4], font=("Arial", 20), relief='groove', bd=border, bg=bg_clr, fg=txt_clr, 
                        command=exportIngredients)
shop_button = tkt.Button(frame_buttons, 
                        text=joana.OPTIONS[5], font=("Arial", 20), relief='groove', bd=border, bg=bg_clr, fg=txt_clr, 
                        command=openShop)
quit_button = tkt.Button(frame_buttons, 
                        text=joana.OPTIONS[6], font=("Arial", 20), relief='groove', bd=border, bg=bg_clr, fg=txt_clr, 
                        command=window.destroy)

# Add pictures
'''
width = 300
height = 300
image = photoImage(file='profil.png').zoom(35).subsample(32)
canvas = Canvas(window, width=width, height=height, bg=bg_clr, bd=0, highlighttickness = 0)
canvas.create_image(width/2, height/2, image=image)
'''
# Show content
#label_title.pack(side=LEFT)
label_title.pack(expand='yes')
label_subtitle.pack(expand='yes')

frame_title.pack(expand='yes')

# Show button
menu_button.grid(row=0, column=0, pady=10)
change_button.grid(row=0, column=1, pady=10)
ingredients_button.grid(row=1, column=0, pady=10)
export_button.grid(row=1, column=1, pady=10)
shop_button.grid(row=2, columnspan=2, pady=10)
quit_button.grid(row=3, columnspan=2, pady=10)

frame_buttons.pack(expand=1)

# Show canvas
label_changing.pack(expand='yes')

label_content.pack(expand='yes')
frame_content.pack(expand=1)
#canvas.pack(expand=YES)


# Show the app
window.mainloop()


# In[ ]:





# In[ ]:




