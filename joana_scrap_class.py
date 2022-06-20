#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# joanna_scrap_class
# configuration CONST file (login, smtp...)
import config
# libraries
import copy
import requests, json
import lib_display as ds
import random
# to send an email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

import pandas as pd

class Scrap:
        
    def __init__(self):
        self.WEEK_DAYS = [
            'lundi', 
            'mardi', 
            'mercredi', 
            'jeudi', 
            'vendredi', 
            'samedi',
            'dimanche',
        ]
        
        self.URL_LOGIN = 'https://api.joanaetvous.com/auth/jwt/create/'
        self.URL_API = 'https://api.joanaetvous.com/'
        self.URL_APP = 'https://app.joanaetvous.com/'
        
        self.LOGIN_MAIL = config.EMAIL
        self.LOGIN_PWD = config.PASSWORD
        
        self.SMTP_ADDRESS = config.SMTP_ADDRESS
        self.SMTP_PORT = config.SMTP_PORT
        
        self.SMTP_LOGIN_MAIL = config.SMTP_EMAIL
        self.SMTP_LOGIN_PWD = config.SMTP_PASSWORD
        self.SMTP_RECEIV_MAIL = config.SMTP_RECEIVER
        
        self.SMTP_MAIL_TEXT = '''
        Hello Youu,

        Le scrapping est terminé.
        L<3ve

        BossaMuffin.com
        '''
        
        self.SMTP_MAIL_HTML = '''
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
        
        self.WEEK_FILE_PREFIXE = "scrapped/joanna_scrap_"
        
        self.week_date_deb = "default"
        self.header = {}
        self.current_session = {}
        self.week_pdf = ""
        self.days_uuid = []
        self.temp_recettes = {}
        
        # Les choix proposés au menu du programme sont compris entre l'indice 1 et l'avant-dernier (réservés au titre et à la question)
        self.OPTIONS = [
            "Choix possibles :",
            "Afficher la liste des recettes de la semaine",
            "Modifier les portions par recette",
            "Afficher les ingredients",
            "Exporter la liste d'ingrédients",
            "Shop on drive",
            "Quitter",
            "Quelle action choisis-tu ?",  
        ]
        
    def constructFilesPath(self):
        e_files_path =  {}
        e_files_path['week'] = self.WEEK_FILE_PREFIXE + self.week_date_deb + ".json"
        e_files_path['ingredients'] = self.WEEK_FILE_PREFIXE + 'ingredients_' + self.week_date_deb + ".txt"
        return e_files_path 
    
    
    def isWeekFile(self):
        try:
            with open(self.constructFilesPath()['week'], 'r'):
                return True
        except (FileNotFoundError, IOError):
            return False

        
    def getSessionHeader():
        e_header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36', 
            'Accept-Encoding': 'gzip, deflate', 
            'Accept': '*/*', 
            'Connection': 'keep-alive'}
        # Add a header giving a random user agent
        try: 
            e_ua = UserAgent().random
            e_header['User-Agent'] = e_ua
        except IndexError :
            print('Index Error on Fake User Agent')
        else:
            print("Unknown User-Agent Error")
        self.header = e_header
    
    
    # Log to Joann&vous
    def login(self):
        e_session = requests.Session()
        e_session.headers.update(self.header)
        e_payload = {
            'email' : self.LOGIN_MAIL,
            'password' : self.LOGIN_PWD
        }
        with e_session.post(self.URL_LOGIN, json = e_payload, headers=self.header) as l_post:
            e_session.headers.update({'authorization': 'Bearer '+ json.loads(l_post.content)['access']})
        self.current_session = e_session
        return e_session
        
    
    # Get json answer from Joana API
    def getJsonAnswer(self, p_target, p_uuid=''):
        e_json_datas = ''
        with self.current_session.get(self.URL_API+p_target+p_uuid, headers=self.header) as l_datas:
            e_json_datas = l_datas.json()
        return e_json_datas


    def printAccountSessionInfo(self):
        print('JOANA - SESSION CONNEXION :')
        print('\n')
        print('Login : ', self.LOGIN_MAIL)
        print('@     :', self.URL_API)
        print('\n')
        print('Headers : ', self.current_session.headers)

        
    def getJoanaSessionMetas(self):
        e_menu_semaine = self.getJsonAnswer('meal-plan/')
        self.week_date_deb = e_menu_semaine['beginning_date'].split(':', 1)[0]
        self.week_pdf = e_menu_semaine['pdf']
        self.days_uuid = [l_day['uuid'] for l_day in e_menu_semaine['weekdays']]

    
    def mailNotif(self):
        # on crée un e-mail
        e_message = MIMEMultipart("alternative")
        e_message["Subject"] = "[BossaMuffin] scrap ok"
        e_message["From"] = self.SMTP_LOGIN_MAIL
        e_message["To"] = self.SMTP_RECEIV_MAIL
        # on crée deux éléments MIMEText (un texte et sa version HTML)
        e_texte_mime = MIMEText(self.SMTP_MAIL_TEXT, 'plain')
        e_html_mime = MIMEText(self.SMTP_MAIL_HTML, 'html')
        e_message.attach(e_texte_mime)
        e_message.attach(e_html_mime)
        # envoie
        e_context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.SMTP_ADDRESS, self.SMTP_PORT, context=e_context) as l_server:
            try: 
                l_server.login(self.SMTP_LOGIN_MAIL, self.SMTP_LOGIN_PWD)
            except:
                print(">> Sending failed, Unexpected error:", 
                      sys.exc_info()[0])
            else: 
                print('>> Sending ok')
                server.sendmail(self.SMTP_LOGIN_MAIL, self.SMTP_RECEIV_MAIL, e_message.as_string())
                print('Notification mail envoyée à : ', self.SMTP_RECEIV_MAIL,
                      '\n                        par : ', self.SMTP_LOGIN_MAIL )

            
    def scrapCurrentWeek(self):
        e_text_to_return = '\n'
        e_week_datas = {}
        e_week_datas = e_week_datas.fromkeys(self.WEEK_DAYS, 'np_matrix')
        e_recettes= {}
        e_json_object = {}
        e_week_files_path = {}
        
        e_infos_week = [self.getJsonAnswer('weekday/', l_uuid) for l_uuid in self.days_uuid]
        
        e_text_to_return = e_text_to_return + '\n\n###' +  self.week_date_deb + '###\n\n'
        print('\n\n###',  self.week_date_deb, '###\n\n' )
        
        e_recette_uuid = ''
        for l0_i, l0_day in enumerate(self.WEEK_DAYS):
            e_text_to_return = e_text_to_return + '\n\n\n------------\n' + l0_day + '\n------------'
            print('\n\n\n------------\n', l0_day, '\n------------')
            e_recettes[l0_i] = {}
            l0_k = 0
            for l1_meals in e_infos_week[l0_i]['meals'][1:]:
                e_text_to_return = e_text_to_return + '\n' + l1_meals['category']['name'] 
                print("-----------------")
                print(l1_meals['category']['name'] )
                print("-----------------")
                #g_text_to_show.set(e_text_to_return)
                #g_label_content.update()
                for l2_temp, l2_dish in enumerate(l1_meals['meal']['dishes']):
                    # Add to the recettes global list
                    l0_k+=1
                    e_recettes[l0_i][l0_k] = {}
                    e_recettes[l0_i][l0_k]['id'] = l2_dish['dish']['uuid']
                    e_recettes[l0_i][l0_k]['display'] = l2_dish['dish']['display']
                    e_recettes[l0_i][l0_k]['name'] = l2_dish['dish']['name']
                    e_recettes[l0_i][l0_k]['portions'] = l2_dish['dish']['portions']
                    e_recettes[l0_i][l0_k]['cooking_time'] = l2_dish['dish']['cooking_time']
                    e_recettes[l0_i][l0_k]['preparation_time'] = l2_dish['dish']['preparation_time']
                    e_recettes[l0_i][l0_k]['days'] = l0_day
                    e_recettes[l0_i][l0_k]['category'] = l1_meals['category']['name']
                    e_text_to_return = e_text_to_return + '\n' + str(l0_k) + ' : ' + l2_dish['dish']['name'] + ' > add to the list'
                    print("-----------------")
                    print(l2_dish['dish']['name'])
                    print("-----------------")
                    #g_text_to_show.set(text_to_return)
                    #g_label_content.update()
                    l2_infos_dish = self.getJsonAnswer('dish/', e_recettes[l0_i][l0_k]['id'])
                    print('ok')
                    e_recettes[l0_i][l0_k]['instructions'] = l2_infos_dish['instructions']
                    e_recettes[l0_i][l0_k]['ingredients'] = {}
                    for l3_j, l3_ingredient in enumerate(l2_infos_dish['ingredients']):
                        e_recettes[l0_i][l0_k]['ingredients'][l3_j] = {}
                        e_recettes[l0_i][l0_k]['ingredients'][l3_j]['name'] = l3_ingredient['ingredient']['name']
                        e_recettes[l0_i][l0_k]['ingredients'][l3_j]['category'] = l3_ingredient['ingredient']['category']
                        e_recettes[l0_i][l0_k]['ingredients'][l3_j]['quantity'] = l3_ingredient['quantity']
                        e_recettes[l0_i][l0_k]['ingredients'][l3_j]['unit_of_measure'] = {}
                        e_recettes[l0_i][l0_k]['ingredients'][l3_j]['unit_of_measure'] = l3_ingredient['unit_of_measure']
                        l3_temp_time = random.randrange(3)
                        ds.countdown(l3_temp_time, p_step=1, p_show=False, p_space=0)
                        e_text_to_return = e_text_to_return + '    > "' + e_recettes[l0_i][l0_k]['ingredients'][l3_j]['name'] + '"'
                        print(e_recettes[l0_i][l0_k]['ingredients'][l3_j]['name'])
                        #g_text_to_show.set(e_text_to_return)
                        #g_label_content.update()
        e_json_object = json.dumps(e_recettes, indent = 4)
        with open(self.constructFilesPath()['week'], "w") as l_outfile:
            l_outfile.write(e_json_object)
        return e_text_to_return

    def initAppScrapping(self):
        # test if the joana's week have been scrapped yet
        self.getSessionHeader
        with self.login() as e_current_session :
            self.printAccountSessionInfo()
            self.getJoanaSessionMetas()
            
            if self.isWeekFile():
                print('\n >> Week scrapped yet')
            else:
                ds.printn()
                print('>> Week isn\'t scrapped yet')
                print('>> Scrapping process')
                ds.printn()
                self.scrapCurrentWeek()
                ds.printn()
                print('>> Scrapping is done')
                ds.printn()
                print('>> Sending a notif email')
                self.mailNotif()
        ds.printn()

    def initRecettesDatas(self):
        with open(self.constructFilesPath()['week'], "r") as l_infile:
            self.temp_recettes = json.load(l_infile)
            e_temp_recettes = self.temp_recettes
        self.initPortionsToOne()
    
    def initPortionsToOne(self):
        for l0_i, l0_day_meals in enumerate(self.temp_recettes.values()):  
            for l1_i, l1_day_meal in enumerate(l0_day_meals.values()):
                l1_day_meal['portions'] = 1
                #self.temp_recettes[str(l0_i)][str(l1_i+1)]['portions'] = 1
                for l2_i, l2_ingredient in enumerate(l1_day_meal['ingredients'].values()):
                    if l2_ingredient['quantity'] != 0:
                        l2_ingredient['quantity'] = l2_ingredient['quantity'] / l1_day_meal['portions']
                        #self.temp_recettes[str(l0_i)][str(l1_i+1)]['ingredients'][str(l2_i)]['quantity'] = l2_ingredient['quantity']

    def orderIngredientsInDf(self):
        e_df_ingredients = pd.DataFrame(columns = ['Category', 'Name' , 'Quantity', 'Symbol'])
        e_nb_lines = 0
        e_temp_recettes = {}
        e_temp_recettes = copy.deepcopy(self.temp_recettes)
        for l0_day_meals in e_temp_recettes.values():  
            for l1_day_meal in l0_day_meals.values():
                if l1_day_meal['portions'] != 0:
                    for l2_ingredient in l1_day_meal['ingredients'].values():
                        # change ingredients quantity by portions 
                        l2_ingredient['quantity'] = l2_ingredient['quantity'] * l1_day_meal['portions']

                        if l2_ingredient['unit_of_measure']['symbol'] != None:
                            l2_symbol = l2_ingredient['unit_of_measure']['symbol']
                        else:
                            l2_symbol = ""
                        # uniformisation des unités
                        if l2_symbol == 'cs':
                            l2_ingredient['quantity'] = l2_ingredient['quantity']*3
                            l2_symbol = 'cc'
                        elif l2_symbol == 'kg':
                            l2_ingredient['quantity'] = l2_ingredient['quantity']*1000
                            l2_symbol = 'g'
                        elif l2_symbol == 'cl':
                            l2_ingredient['quantity'] = l2_ingredient['quantity']*10
                            l2_symbol = 'ml'
                        elif l2_symbol == 'dl':
                            l2_ingredient['quantity'] = l2_ingredient['quantity']*100
                            l2_symbol = 'ml'
                        elif l2_symbol == 'l':
                            l2_ingredient['quantity'] = l2_ingredient['quantity']*1000
                            l2_symbol = 'ml'
                        e_df_ingredients.loc[e_nb_lines] = [ l2_ingredient['category']['name'], l2_ingredient['name'], l2_ingredient['quantity'], l2_symbol ]
                        l2_ingredient['unit_of_measure']['symbol'] = l2_symbol
                        e_nb_lines += 1
        e_df_ingredients_sorted = e_df_ingredients.groupby(['Category', 'Name', 'Symbol']).sum()
        return e_df_ingredients_sorted


    def showMeals(self):
        e_text_to_return = self.OPTIONS[1] + ' :\n'
        l0_day_i = 0
        for l0_day_meals in self.temp_recettes.values():  
            e_text_to_return += '\n'
            e_text_to_return += '\n'
            e_text_to_return += '\n'
            e_text_to_return += ds.separator(5)
            e_text_to_return += self.WEEK_DAYS[l0_day_i]
            l0_day_i += 1
            for l1_day_meal in l0_day_meals.values():
                e_text_to_return += '\n'
                e_text_to_return += '\n'
                e_text_to_return += '>' + l1_day_meal['name']
                if int(l1_day_meal['portions']) and l1_day_meal['portions'] > 0:
                    e_text_to_return += f"\n{'-':<5}{'pour':<10}{l1_day_meal['portions']:<5}{'pax'}"

                if int(l1_day_meal['preparation_time']) and l1_day_meal['preparation_time'] > 0:
                    e_text_to_return += f"\n{'-':<5}{'compte':<10}{l1_day_meal['preparation_time']:<5}{'min de prépa'}"

                if int(l1_day_meal['cooking_time']) and l1_day_meal['cooking_time'] > 0:
                    e_text_to_return += f"\n{'-':<5}{'et':<10}{l1_day_meal['cooking_time']:<5}{'min de cuisson'}"

        #print(e_text_to_return)
        return e_text_to_return
    
    def showMealsByDay(self, p_asked_day=0):
        e_text_to_return = '\n'
        e_text_to_return += '\n'
        e_text_to_return += self.OPTIONS[1] + ' :\n'
        e_text_to_return += '\n'
        e_text_to_return += ds.separator(5)
        e_text_to_return += self.WEEK_DAYS[p_asked_day]
        for l0_day_meal in self.temp_recettes[str(p_asked_day)].values():
            e_text_to_return += '\n'
            e_text_to_return += '\n'
            e_text_to_return += '>' + l0_day_meal['name']
            if int(l0_day_meal['portions']) and l0_day_meal['portions'] > 0:
                e_text_to_return += f"\n{'-':<5}{'pour':<10}{l0_day_meal['portions']:<5}{'pax'}"

            if int(l0_day_meal['preparation_time']) and l0_day_meal['preparation_time'] > 0:
                e_text_to_return += f"\n{'-':<5}{'compte':<10}{l0_day_meal['preparation_time']:<5}{'min de prépa'}"

            if int(l0_day_meal['cooking_time']) and l0_day_meal['cooking_time'] > 0:
                e_text_to_return += f"\n{'-':<5}{'et':<10}{l0_day_meal['cooking_time']:<5}{'min de cuisson'}"

        print(e_text_to_return)
        return e_text_to_return 
    
    def showIngredients(self):
        e_text_to_return = self.OPTIONS[3] + ' :\n'
        for l0_i, l0_ingredient_group in self.orderIngredientsInDf().items():
            l1_line = f"{'>':<5}{l0_ingredient_group}"
            e_text_to_return = e_text_to_return + '\n' + l1_line
        print(e_text_to_return)
        return e_text_to_return


    def printIngredientsInFile(self):
        e_text_to_return = self.OPTIONS[4] + ' :\n'                                    
        e_nb_lines = 0
        with open(self.constructFilesPath()['ingredients'], "w") as l0_outfile:
            l0_outfile.write('LISTE DES INGREDIENTS DE LA SEMAINE \n-----------------\n\n')

            for l1_i, l1_ingredient_group in self.orderIngredientsInDf().items():
                l1_line = f"{'+':<5}{l1_ingredient_group}"
                e_text_to_return = e_text_to_return + '\n' + l1_line
                l0_outfile.write(l1_line + '\n')
                e_nb_lines += 1
        e_text_to_return += str(e_nb_lines)
        return e_text_to_return 


# In[ ]:





# In[ ]:




