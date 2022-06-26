'''
Created on June 18, 2022
@author: BalthMhs
@society: BossaMuffinConnected
'''
# secret logins to connect with the foreign apps (Joana's API, personnal mail server...)
import config
# # #
import lib_display as ds
from fake_useragent import UserAgent 
import requests, json
import random
# to send an email
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

class ModelScrapping:
    '''
    Classdocs
    '''
    def __init__(self):
        self.URL_LOGIN = 'https://api.joanaetvous.com/auth/jwt/create/'
        self.URL_API = 'https://api.joanaetvous.com/'
        self.URL_APP = 'https://app.joanaetvous.com/'
        self.LOGIN_MAIL = config.EMAIL
        self.LOGIN_PWD = config.PASSWORD
        self.WEEK_DAYS = [
            'lundi', 
            'mardi', 
            'mercredi', 
            'jeudi', 
            'vendredi', 
            'samedi',
            'dimanche',
        ]
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
        self.g_temp_recettes = {}
        try:
            self._initAppScrapping()
        except:
            print(">> Scrap init error")
        else:
            print(">> Loading recettes file and initializing portions...")
            self._initRecettesDatas()
            print(">> Loading completed")
    
    def main(self):
        pass
    
    def _initAppScrapping(self):
        # test if the joana's week have been scrapped yet
        self._getSessionHeader
        with self._login() as e_current_session :
            self._printAccountSessionInfo()
            self._getJoanaSessionMetas()
            ds.printn()
            if self._isWeekFile():
                print(">> Week scrapped yet")
            else:
                print(">> Week to be scrapped")
                print(">> Scrapping process ...")
                self.scrapCurrentWeek()
                print(">> Scrapping done")
                print(">> Sending a notif email ...")
                self._mailNotif()
            self.files_path = self.constructFilesPath()

    def _initRecettesDatas(self):
        with open(self.constructFilesPath()['week'], "r") as l_infile:
            self.g_temp_recettes = json.load(l_infile)
        self._initPortionsToOne()
    
    def _initPortionsToOne(self):
        for l0_i, l0_day_meals in enumerate(self.g_temp_recettes.values()):  
            for l1_i, l1_day_meal in enumerate(l0_day_meals.values()):
                # divide all ingredient quantity by portions to have quantity for 1 person
                for l2_i, l2_ingredient in enumerate(l1_day_meal['ingredients'].values()):
                    if l1_day_meal['portions'] != 0:
                        l2_ingredient['quantity'] = l2_ingredient['quantity'] / l1_day_meal['portions']
                # set portion to 1
                l1_day_meal['portions'] = 1
    
    def _getSessionHeader():
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
            print(">> Index Error on Fake User Agent")
        else:
            print(">> Unknown User-Agent Error")
        self.header = e_header
        
    # Log to Joann&vous
    def _login(self):
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
    
    def _printAccountSessionInfo(self):
        print("\n")
        print("JOANA - SESSION CONNEXION")
        print("Login   : ", self.LOGIN_MAIL)
        print("@       : ", self.URL_API)
        print("Headers : ", self.current_session.headers)

    def _getJoanaSessionMetas(self):
        e_menu_semaine = self._getJsonAnswer('meal-plan/')
        self.week_date_deb = e_menu_semaine['beginning_date'].split(':', 1)[0]
        self.week_pdf = e_menu_semaine['pdf']
        self.days_uuid = [l_day['uuid'] for l_day in e_menu_semaine['weekdays']]

    # Get json answer from Joana API
    def _getJsonAnswer(self, p_target, p_uuid=''):
        e_json_datas = ''
        with self.current_session.get(self.URL_API+p_target+p_uuid, headers=self.header) as l_datas:
            e_json_datas = l_datas.json()
        return e_json_datas

    def _isWeekFile(self):
        try:
            with open(self.constructFilesPath()['week'], 'r'):
                return True
        except (FileNotFoundError, IOError):
            return False   
    
    def constructFilesPath(self):
        e_files_path =  {}
        e_files_path['week'] = self.WEEK_FILE_PREFIXE + self.week_date_deb + ".json"
        e_files_path['ingredients'] = self.WEEK_FILE_PREFIXE + 'ingredients_' + self.week_date_deb + ".txt"
        return e_files_path 
    
    def scrapCurrentWeek(self):
        e_text_to_return = '\n'
        e_week_datas = {}
        e_week_datas = e_week_datas.fromkeys(self.WEEK_DAYS, "np_matrix")
        e_recettes= {}
        e_json_object = {}
        e_week_files_path = {}
        
        e_infos_week = [self._getJsonAnswer("weekday/", l_uuid) for l_uuid in self.days_uuid]
        
        e_text_to_return = e_text_to_return + "\n\n###" +  self.week_date_deb + "###\n\n"
        print("\n\n###",  self.week_date_deb, "###\n\n" )
        
        e_recette_uuid = ''
        for l0_i, l0_day in enumerate(self.WEEK_DAYS):
            e_text_to_return = e_text_to_return + "\n\n\n------------\n" + l0_day + "\n------------"
            print("\n\n\n------------\n", l0_day, "\n------------")
            e_recettes[l0_i] = {}
            l0_k = 0
            for l1_meals in e_infos_week[l0_i]['meals'][1:]:
                e_text_to_return = e_text_to_return + "\n" + l1_meals['category']['name'] 
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
                    e_text_to_return = e_text_to_return + '\n' + str(l0_k) + ' : ' + l2_dish['dish']['name'] + " > add to the list"
                    print("-----------------")
                    print(l2_dish['dish']['name'])
                    print("-----------------")
                    l2_infos_dish = self._getJsonAnswer("dish/", e_recettes[l0_i][l0_k]['id'])
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
        e_json_object = json.dumps(e_recettes, indent = 4)
        with open(self.constructFilesPath()['week'], "w") as l_outfile:
            l_outfile.write(e_json_object)
        return e_text_to_return

    
    def _mailNotif(self):
        # on crée un e-mail
        e_message = MIMEMultipart("alternative")
        e_message["Subject"] = "[BossaMuffin] Scrapping is done"
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
                print(">> Sending failed, Unexpected error : ", 
                      sys.exc_info()[0])
            else: 
                print(">> Sending completed")
                server.sendmail(self.SMTP_LOGIN_MAIL, self.SMTP_RECEIV_MAIL, e_message.as_string())
                print(">> Mail notif sended : \n",
                      "   to   : ", self.SMTP_RECEIV_MAIL, "\n",
                      "   from : ", self.SMTP_LOGIN_MAIL)
