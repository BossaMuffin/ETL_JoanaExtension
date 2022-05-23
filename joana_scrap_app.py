#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8

# # SCRAPPING JOANA&VOUS 

# In[1]:

import lib_display as ds
from fake_useragent import UserAgent 
import requests, json, random

# To send an email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import pandas as pd
# Import view func tkinter 
import tkinter as tkt
import webbrowser

# In[2]:
week_days = [
    'lundi', 
    'mardi', 
    'mercredi', 
    'jeudi', 
    'vendredi', 
    'samedi',
    'dimanche',
]

url_login = 'https://api.joanaetvous.com/auth/jwt/create/'
url_api = 'https://api.joanaetvous.com/'
url_app ='your mail'
password = 'your password'

# export and formated datas file
week_file_prefixe = "joanna_scrap_"
week_date_deb = "default"

def construct_files_path(date = week_date_deb):
    r =  {}
    r['week'] = week_file_prefixe + date + ".json"
    r['ingredients'] = week_file_prefixe + 'ingredients_' + week_date_deb + ".txt"
    
    return r 

#week_data_file = construct_files_path()['week']
#week_ingredients_file = construct_files_path()['ingredients']


# Log to Joann&vous
def login(mail, pwd, headers):
    s = requests.Session()
    payload = {
        'email' : mail,
        'password' : pwd
    }
    with s.post(url_login, json = payload, headers=headers) as res:
        s.headers.update({'authorization': 'Bearer '+ json.loads(res.content)['access']})
        #print(res.content)
    return s

# Get json answer from Joana API
def get_json_answer(session, target, uuid=''):
    r = ''
    with session.get(url_api+target+uuid, headers=headers) as resp:
        r = resp.json()
        #resp.headers
        #print(type(resp))
    return r

def get_header():
    # Add a header giving a random user agent
    ua = UserAgent().random
    headers = {'user-agent': ua}
    return headers

def return_joana_account_session(headers):

    current_session = login(email, password, headers)

    # In[5]:

    print('JOANA - SESSION CONNEXION :')
    print('\n')
    print('Login : ', email)
    print('@     :', url_api)
    print('\n')
    print('Headers : ', current_session.headers)
    
    return current_session

def return_joana_session_meta(session):
    r = {}
    
    menu_semaine = get_json_answer(current_session, 'meal-plan/')
    r['week_date_deb'] = menu_semaine['beginning_date'].split(':', 1)[0]
    r['week_pdf'] = menu_semaine['pdf']
    r['uuid_jours'] = [day['uuid'] for day in menu_semaine['weekdays']]
    
    return r

def isFile(filePath):
    try:
        with open(filePath, 'r') as f:
            return True
    except FileNotFoundError as e:
        return False
    except IOError as e:
        return False

def scrap_current_week(headers):
    week_datas = {}
    week_datas = week_datas.fromkeys(week_days, 'np_matrix')

    recettes= {}
    
    current_session = return_joana_account_session(headers)
    week_meta = return_joana_session_meta(current_session)
    week_date_deb = week_meta['week_date_deb']
    week_pdf = week_meta['week_pdf']
    uuid_jours = week_meta['uuid_jours']

    # In[8]:


    infos_week = [get_json_answer(current_session, 'weekday/', uuid) for uuid in uuid_jours]

    # In[9]:

    # jours de 0 à 7 // meals de 1 à 3 // dish de 1 à ?
    ds.printn(2)
    print('###', week_date_deb, '###')
    ds.printn(2)

    recette_uuid = ''

    for i, day in enumerate(week_days):
        print('\n\n\n------------\n', day, '\n------------')
        recettes[i] = {}
        k = 0
        for meals in infos_week[i]['meals'][1:]:
            ds.printn(1)
            print(meals['category']['name'])
            for temp, dish in enumerate(meals['meal']['dishes']):
                # Add to the recettes global list
                k+=1
                recettes[i][k] = {}
                recettes[i][k]['id'] = dish['dish']['uuid']
                recettes[i][k]['display'] = dish['dish']['display']
                recettes[i][k]['name'] = dish['dish']['name']
                recettes[i][k]['portions'] = dish['dish']['portions']
                recettes[i][k]['cooking_time'] = dish['dish']['cooking_time']
                recettes[i][k]['preparation_time'] = dish['dish']['preparation_time']

                recettes[i][k]['days'] = day
                recettes[i][k]['category'] = meals['category']['name']
                print('\n')
                print(k, ' : ', dish['dish']['name'], ' > add to the list (', recettes[i][k]['display'], ')')

                infos_dish = get_json_answer(current_session, 'dish/', recettes[i][k]['id'])
                recettes[i][k]['instructions'] = infos_dish['instructions']
                recettes[i][k]['ingredients'] = {}

                for j, ingredient in enumerate(infos_dish['ingredients']):
                    recettes[i][k]['ingredients'][j] = {}
                    recettes[i][k]['ingredients'][j]['name'] = ingredient['ingredient']['name']
                    recettes[i][k]['ingredients'][j]['category'] = ingredient['ingredient']['category']
                    recettes[i][k]['ingredients'][j]['quantity'] = ingredient['quantity']
                    recettes[i][k]['ingredients'][j]['unit_of_measure'] = {}
                    recettes[i][k]['ingredients'][j]['unit_of_measure'] = ingredient['unit_of_measure']
                    temp_time = random.randrange(3)
                    ds.countdown(temp_time, step=1, show=False, space=0)
                    print('    > "', recettes[i][k]['ingredients'][j]['name'], '"')

    mail_notif()
    # In[11]:

    json_object = json.dumps(recettes, indent = 4)
    
    week_data_files = construct_files_path(week_date_deb)

    with open(week_data_files['week'], "w") as outfile:
        outfile.write(json_object)
    


# In[2]:


## ENVOYER UN EMAIL
# on rentre les renseignements pris sur le site du fournisseur
smtp_address = 'smtp.ionos.fr'
smtp_port = 465

# on rentre les informations sur notre adresse e-mail
email_address = 'engineer@bossamuffin.com'
email_password = 'Alan_BM-48-47..Mail!'

# on rentre les informations sur le destinataire
email_receiver = '4u.mehus@gmail.com'


def mail_notif():

    # on crée un e-mail
    message = MIMEMultipart("alternative")
    # on ajoute un sujet
    message["Subject"] = "[BossaMuffin] scrap ok"
    # un émetteur
    message["From"] = email_address
    # un destinataire
    message["To"] = email_receiver

    # on crée un texte et sa version HTML
    texte = '''
    Hello Youu,

    Le scrapping est terminé.
    L<3ve

    BossaMuffin.com
    '''

    html = '''
    <html>
    <body>
    <h1>Hello Youu</h1>
    <p>Le scrapping est terminé</p>
    <b>L<3ve</b>
    <br>
    <a href="https://www.bossamuffin.com">Quand tu auras 3 secondes, passe jeter un oeil sur BossaMuffin.com, tu pourrais être surprise</a>
    </body>
    </html>
    '''

    # on crée deux éléments MIMEText 
    texte_mime = MIMEText(texte, 'plain')
    html_mime = MIMEText(html, 'html')

    # on attache ces deux éléments 
    message.attach(texte_mime)
    message.attach(html_mime)

    # on crée la connexion
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_address, smtp_port, context=context) as server:
        # connexion au compte
        server.login(email_address, email_password)
        # envoi du mail
        server.sendmail(email_address, email_receiver, message.as_string())
        print('Notification mail envoyée à : ', email_receiver, '\n                        par : ', email_address )
        


# In[3]:


# test if the joana's week have been scrapped yet
headers = get_header()
with return_joana_account_session(headers) as current_session:
    week_meta = return_joana_session_meta(current_session)

    if isFile(week_file_prefixe + week_meta['week_date_deb'] + ".json"):
        print('\n >> Week scrapped yet')
    else:
        ds.printn()
        print('>> Week isn\'t scrapped yet')
        print('>> Scrapping process')
        ds.printn()
        scrap_current_week(headers)
        ds.printn()
        print('>> Scrapping is done')
        ds.printn()
    
    week_data_files = construct_files_path(week_meta['week_date_deb'])


# In[28]:


## Week_days is in joana_scraping !!

temp_recettes = ""
    
with open(week_data_files['week'], "r") as infile:
    temp_recettes = json.load(infile)

separator = '-' * 10

# Les choix proposés au menu du programme sont compris entre l'indice 1 et l'avant-dernier (réservés au titre et à la question)
options = [
    "Choix possibles :",
    "Afficher la liste des recettes de la semaine",
    "Modifier les portions par recette",
    "Afficher les ingredients",
    "Exporter la liste d'ingrédients",
    "Shop on drive",
    "Quitter",
    "Quelle action choisis-tu ?",  
]

print('Chargement ...')
ds.printn(2)

# In[3]:

def show_meals(opt=1):
    
    r = options[opt] + ' :\n'
    day_i = 0
    for day_meals in temp_recettes.values():  

        print('\n')
        print(separator)
        print(week_days[day_i])
        day_i += 1

        for day_meal in day_meals.values():
            r += '\n'

            r += '>' + day_meal['name']
            r += '\n'
            if int(day_meal['portions']) and day_meal['portions'] > 0:
                r += f"\n{'-':<5}{'pour':<10}{day_meal['portions']:<5}{'pax'}"

            if int(day_meal['preparation_time']) and day_meal['preparation_time'] > 0:
                r += f"\n{'-':<5}{'compte':<10}{day_meal['preparation_time']:<5}{'min de prépa'}"

            if int(day_meal['cooking_time']) and day_meal['cooking_time'] > 0:
                r += f"\n{'-':<5}{'et':<10}{day_meal['cooking_time']:<5}{'min de cuisson'}"
    return r
       
# In[4]:

def change_portions(opt=2):
    print(options[opt], ' :')
    day_i = 0
    portion = 0

    for day_meals in temp_recettes.values():  

        if portion != "stop":
            print('\n')
            print(separator)
            print(week_days[day_i])
            day_i += 1


            for day_meal in day_meals.values():

                if portion != "stop":
                    portion = 0
                    print('\n')
                    #print(day_meal)
                    print(separator)
                    print('\n')
                    print ('>', day_meal['name'])

                    
                    ds.countdown(0, show=False)
                    
                    print(f"{'-':<5}{'Actuellement pour ':<20}{day_meal['portions']:<5}{'pax'}")
                    '''      
                    if int(day_meal['portions']) and int(day_meal['portions']) > 0:
                        print(f"{'-':<5}{'Actuellement pour ':<20}{day_meal['portions']:<5}{'pax'}")
                    elif int(day_meal['portions']) and int(day_meal['portions']) == 0:
                        print(f"{'-':<5}{'Actuellement pour ':<20}{'0':<5}{'pax'}")
                    else: 
                        print('Erreur système : mauvaise data.json "portions"')
                        break
                    '''
                          
                    while portion not in ["next", "stop"]:
                        portion = input(f"{'-':<5}{'Pour combien de pax ? (sinon <stop> ou <next>)'}")

                        print('\n')

                        if not portion.isdigit():
                            if portion not in ["next", "stop"]:
                                print('Entre un nombre')
                                continue
                            elif portion == "next":
                                print('Next')
                                break
                            elif portion == "stop":
                                break

                        #elif int(portion) > 0:

                        #print(day_meal['portions'])
                        for ingredient in day_meal['ingredients'].values():

                            if ingredient['quantity'] != 0:
                                
                                try:
                                    ingredient['quantity'] = (ingredient['quantity'] / day_meal['portions'] ) * float(portion)
                                except ZeroDivisionError:
                                     ingredient['quantity'] = ingredient['quantity'] * float(portion)
                                #print('->', temp_ingr_quant, '>', ingredient['quantity'], ' ', ingredient['unit_of_measure']['symbol'] )

                        plural=''
                        if int(portion) > 1:plural = 's'

                        print(f"{'-':<5}{'On passe de '}{day_meal['portions']}{' à '}{portion}{' portion'}{plural}" )
                        day_meal['portions'] = int(portion)

                        portion = input(f"{'-':<5}{'Valider ? (presse <Entrée> sinon <non>)'}")

                        if portion == "non":
                            continue
                        else:
                            break
                              
                else:
                    break
        else:
            print('Fin de la procédure')
            break

# In[5]:

def show_ingredients(opt=3):
    print(options[3], ' :')

    for i, ingredient_group in order_ingredients_in_df().items():
        line = f"{'>':<5}{ingredient_group}"
        r = r + '\n' + line
    return(r)

# In[7]:

def print_ingredients_in_file(opt=4):
    print(options[4], ' :')
                                        
    nb_lines = 0
    with open(week_data_files['ingredients'], "w") as outfile:
        outfile.write('LISTE DES INGREDIENTS DE LA SEMAINE \n-----------------\n\n')
        
        for i, ingredient_group in order_ingredients_in_df().items():
            line = f"{'+':<5}{ingredient_group}"
            print(line)
            outfile.write(line + '\n')
            nb_lines += 1
        
    return nb_lines
   
# In[8]:

ingredient_list = [('','','')]
df_ingredients = pd.DataFrame(columns = ['Category', 'Name' , 'Quantity', 'Symbol'])

def order_ingredients_in_df():
    print('Tri des ingrédients :')
    
    nb_lines = 0
    
    for day_meals in temp_recettes.values():  

        for day_meal in day_meals.values():

            if day_meal['portions'] != 0:

                for ingredient in day_meal['ingredients'].values():

                    if ingredient['unit_of_measure']['symbol'] != None:
                        symbol = ingredient['unit_of_measure']['symbol']
                    else:
                        symbol = ""
                    # uniformisation des unités
                    if symbol == 'cs':
                        ingredient['quantity'] = ingredient['quantity']*3
                        symbol = 'cc'
                    elif symbol == 'kg':
                        ingredient['quantity'] = ingredient['quantity']*1000
                        symbol = 'g'
                    elif symbol == 'cl':
                        ingredient['quantity'] = ingredient['quantity']*10
                        symbol = 'ml'
                    elif symbol == 'dl':
                        ingredient['quantity'] = ingredient['quantity']*100
                        symbol = 'ml'
                    elif symbol == 'l':
                        ingredient['quantity'] = ingredient['quantity']*1000
                        symbol = 'ml'
                        
                    df_ingredients.loc[nb_lines] = [ ingredient['category']['name'], ingredient['name'], ingredient['quantity'], symbol ]
                    ingredient['unit_of_measure']['symbol'] = symbol
                    nb_lines += 1
    #print(nb_lines)
    df_ingredients_sorted = df_ingredients.groupby(['Category', 'Name', 'Symbol']).sum()

    return df_ingredients_sorted

# In[9]:

def init_zero_and_two_portion_to_one():
    
    for day_meals in temp_recettes.values():  
        
        for day_meal in day_meals.values():
            
            if day_meal['portions'] == 0 :
                day_meal['portions'] = 1
                
            elif day_meal['portions'] == 2:
                day_meal['portions'] = 1

                for ingredient in day_meal['ingredients'].values():

                    if ingredient['quantity'] != 0:
                        ingredient['quantity'] = ingredient['quantity'] / 2

                
init_zero_and_two_portion_to_one()


# In[29]:


# In[1]:
shop_url = 'https://www.intermarche.com/accueil'
bg_clr = '#41B77F'
txt_clr = 'white'
gtry = '1080x720'
min_size_L = 480
min_size_H = 360
logo_ico = 'logo.ico'
border = 1


# In[3]:
   
# hide a frame
def hide_frame():
    frame_content.pack_forget()
    
# show the liste of meals in the menu of the week
def view_menu():
    text = show_meals()
    text_to_show.set(text)

# change portions of meals
def change_portions():
    change_portions(opt=2)
    
    frame_buttons.pack_forget()
    frame_content.pack_forget()
    frame_change.pack(expand=1)
    app_to_show.set('Change your portions')
        
# show the list of all necessary ingredients
def view_ingredients():
    show_ingredients()
    text_to_show.set('Import : Liste des ingrédient')
    
# export the list of all necessary ingredients
def export_ingredients():  
    print(print_ingredients_in_file(opt=4), ' >>>   Ingrédients ajoutés au fichier de la semaine')

# open the shop webpage
def open_shop(url=shop_url):
    webbrowser.open_new(url)

# Create the window
window = tkt.Tk()

# open the shop webpage
def stop_app(w=window):
    window.destroy
    sys.exit(0)
# def text():
#     frame_buttons.delete(0, END)
#     frame_buttons.insert(0, 'Hello world')
# 

# In[4]:

# Create the navigation bar
nav_bar = tkt.Menu(window)
opt_nav=tkt.Menu(nav_bar, tearoff=0)
opt_nav.add_command(label='Scrap /!\\', command=scrap_current_week)
opt_nav.add_command(label='Imprimer', command=view_ingredients)
opt_nav.add_command(label='Quitter', command=stop_app)
nav_bar.add_cascade(label="Options", menu=opt_nav)

# In[5]:

# Configure the window
window.title("Je t'aime mon âme d'am°°°")
window.geometry(gtry)
window.minsize(min_size_L, min_size_H)
#window.iconbitmap("logo.ico")
window.config(menu=nav_bar, background=bg_clr, bd=1, relief='sunken')

# In[6]:

# Create the frames
frame_title = tkt.Frame(window, bd=border,bg=bg_clr)
frame_buttons = tkt.Frame(window, bd=border, bg=bg_clr)
frame_change = tkt.Frame(window, bd=border, bg=bg_clr)
frame_content = tkt.Frame(window, bd=border, bg=bg_clr)

# In[7]:

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
                        text=options[1], font=("Arial", 20), relief='groove', bd=border, bg=bg_clr, fg=txt_clr, 
                        command=view_menu)
change_button = tkt.Button(frame_buttons, 
                        text=options[2], font=("Arial", 20), relief='groove', bd=border, bg=bg_clr, fg=txt_clr, 
                        command=change_portions)
ingredients_button = tkt.Button(frame_buttons, 
                        text=options[3], font=("Arial", 20), relief='groove', bd=border, bg=bg_clr, fg=txt_clr, 
                        command=view_ingredients)
export_button = tkt.Button(frame_buttons, 
                        text=options[4], font=("Arial", 20), relief='groove', bd=border, bg=bg_clr, fg=txt_clr, 
                        command=hide_frame)
shop_button = tkt.Button(frame_buttons, 
                        text=options[5], font=("Arial", 20), relief='groove', bd=border, bg=bg_clr, fg=txt_clr, 
                        command=open_shop)
quit_button = tkt.Button(frame_buttons, 
                        text=options[6], font=("Arial", 20), relief='groove', bd=border, bg=bg_clr, fg=txt_clr, 
                        command=window.destroy)

# In[8]:

# Add pictures
'''
width = 300
height = 300
image = photoImage(file='profil.png').zoom(35).subsample(32)
canvas = Canvas(window, width=width, height=height, bg=bg_clr, bd=0, highlighttickness = 0)
canvas.create_image(width/2, height/2, image=image)
'''

# In[9]:

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

# In[ ]:

# Show the app
window.mainloop()


# In[ ]:




