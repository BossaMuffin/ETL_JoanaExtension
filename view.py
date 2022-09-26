"""
Created on June 18, 2022
@author: BalthMhs
@society: BossaMuffinConnected
"""
# constants available in the whole app
import global_constants as g_const
# # #
import lib_display as ds
import tkinter as tk

class TkView(tk.Tk):
    '''
    Classdocs
    '''
    def __init__(self):
        super().__init__()
        
    def setupWindow(self, p_controller):
        self.controller  = p_controller
        #Set the global parameters
        self.BG_CLR = 'white'
        self.BG_CLR_1 = "#41B77F"
        self.BG_CLR_2 = "#f2f2f2"
        self.TXT_CLR = 'white'
        #self.GTRY = '1080x'+str(self.winfo_screenheight())
        self.MIN_WIDTH = 720
        self.MIN_HEIGHT = 720
        self.WIDTH_BTN = 20
        self.IPADY_CONTENT = 20
        self.PADX_CONTENT = 10
        self.WIDTH_CONTENT_AREA = self.MIN_WIDTH-self.WIDTH_BTN-(4*self.PADX_CONTENT)
        self.LOGO_ICO = 'logo.ico'
        self.BORDER = 1
        self.CONTENT_MESSAGE = (
            "Coucou Jude \n Pour débuter le programme : \nappuie sur le bouton démarrer (à gauche de l'écran)",
            "Qu'est-ce qu'on mange ? \n 1) on récupère le menu de la semaine de Joana ; \n 2) tu choisis les repas qui t'intéressent ; \n 3) on prépare ta liste de course. \n Easy, n'est-ce pas ?",
        )
        #Init local attributes
        self.btn_choosing_day = {}
        self.btn_choosing_day_in_app = {}
        self.frame_by_day = {}
        self.label_by_day = {}
        # Make the window and the frames
        self._initWindow()

    def startMainLoop(self):
        self.mainloop()
    
    def _centerWindow(self):
        self.update()
        e_width = self.winfo_width()
        e_height = self.winfo_screenheight()
        e_xoffset = (self.winfo_screenwidth() - e_width) // 2
        e_yoffset = (self.winfo_screenheight() - e_height) // 2
        e_gtry = f'{e_width}x{e_height}+{e_xoffset}+{e_yoffset}'
        self.geometry(e_gtry)
        
    # Create the navigation bar
    def _makeNavBar(self):
        self.nav_bar = tk.Menu(self)
        e_opt_nav_quit = tk.Menu(self.nav_bar, tearoff=0)
        e_opt_nav_quit.add_command(label='Confirmer', command=self.controller.stopApp)
        self.nav_bar.add_cascade(label=g_const.OPTIONS['quit_app'], menu=e_opt_nav_quit)
    
    def addScrapBtnToNavBar(self):
        e_opt_nav_scrap = tk.Menu(self.nav_bar, tearoff=0)
        e_opt_nav_scrap.add_command(label="Valider", command=self.controller.forceScrapping)
        self.nav_bar.add_cascade(label=g_const.OPTIONS['force_scrap'], menu=e_opt_nav_scrap)
        
    def _makeTitlesBar(self):
        self.title("Joana's patch")
        self.frame_title = tk.Frame(self, 
                                bg="blue", 
                                width=self.MIN_WIDTH, 
                                height=self.MIN_HEIGHT)
        self.label_title = tk.Label(self.frame_title, 
                                text="MENU DE LA SEMAINE", 
                                bg=self.BG_CLR_1, 
                                fg=self.TXT_CLR)
        self.var_subtitle_to_show = tk.StringVar()
        self.var_subtitle_to_show.set("Hello my Jude'")
        self.label_subtitle = tk.Label(self.frame_title, 
                                    text="Hello my Jude'", 
                                    textvariable=self.var_subtitle_to_show,
                                    bg=self.BG_CLR_1, 
                                    fg=self.TXT_CLR)
        self.frame_title.pack(fill='x')
        self.label_title.pack(fill='x')
        self.label_subtitle.pack(fill='x')

    def _initWindow(self):
        #Create the main window
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)
        self._centerWindow()
        self._makeNavBar()
        self._makeTitlesBar()
        #self.iconbitmap("img/icon_checked.ico")
        self.config(menu=self.nav_bar, background=self.BG_CLR, relief='sunken')
        self.resizable(width=True, height=True)
        #self.attributes('-fullscreen', True) 
        self._makeMainWidgets()
        self._makeMainEntries()
        self._showStartButton()
        self._showContent()
        self.showContentMessage()
        self._centerWindow()

    def setupMainView(self, p_controller):
        pass

    def _makeMainWidgets(self):
        self.frame_buttons = tk.Frame(self, bg=self.BG_CLR_1, width=self.WIDTH_BTN)
        self.frame_buttons.pack(side="left", fill='y', padx= self.PADX_CONTENT, ipadx=10, ipady=20)
        self._makeMainButtons()
        self._makeDaysButtons()
        self._makeContentWidgets()
        self._makePortionsAppWidgets()
    
    def _makeMainEntries(self):
        pass

    def _makeContentWidgets(self):
        self.frame_content = tk.Frame(self,
                                       width=self.WIDTH_CONTENT_AREA,
                                       bg=self.BG_CLR_2)
        self.var_message_to_show = tk.StringVar()
        self.var_message_to_show.set(self.CONTENT_MESSAGE[0])
        self.message_content = tk.Message(self.frame_content, 
                                      text=self.CONTENT_MESSAGE[0], 
                                      textvariable=self.var_message_to_show, 
                                      width=self.WIDTH_CONTENT_AREA, 
                                      justify="left")
    
    def _makeMainButtons(self):
        # Menu au chargement
        self.var_start_btn_txt = tk.StringVar()
        self.var_start_btn_txt.set("Démarrer")
        self.btn_opt_start = tk.Button(self.frame_buttons,
                                       text="Démarrer", 
                                       textvariable=self.var_start_btn_txt,
                                       command=self.controller.setRecettesDatas,
                                       width=self.WIDTH_BTN)
        # Menu principale
        self.btn_opt_menu = tk.Button(self.frame_buttons, 
                                  text="Qu'est-ce qu'on mange ?", 
                                  command=self.controller.showWeekMenu, 
                                  width=self.WIDTH_BTN)
        self.btn_opt_download = tk.Button(self.frame_buttons, 
                                  text="Télécharger le menu", 
                                  command=self.controller.downloadJoanaPngMenu, 
                                  width=self.WIDTH_BTN)
        self.btn_opt_portionsApp = tk.Button(self.frame_buttons, 
                                      text="Changer les portions", 
                                      command=self.controller.showPortionsApp, 
                                      width=self.WIDTH_BTN)
        self.btn_opt_ingredients = tk.Button(self.frame_buttons, 
                                         text="Voir les ingrédients", 
                                         command=self.controller.showIngredientsList, 
                                         width=self.WIDTH_BTN)
        self.btn_opt_exportIngredients = tk.Button(self.frame_buttons, 
                                         text="Exporter les ingrédients", 
                                         command=self.controller.exportIngredientsInFile, 
                                         width=self.WIDTH_BTN)
        self.label_space = tk.Label(self.frame_buttons, 
                                     bg=self.BG_CLR_1, 
                                     text='')

    def _makeDaysButtons(self):
        for l0_i, l0_day in enumerate(g_const.WEEK_DAYS) :
            self.btn_choosing_day[l0_i] = tk.Button(self.frame_buttons, 
                                                     text=l0_day, 
                                                     width=self.WIDTH_BTN,
                                                     command=lambda day_id=l0_i : self.controller.chooseDayToShow(p_day_id=day_id, p_current_view='menu'))
            
            self.btn_choosing_day_in_app[l0_i] = tk.Button(self.frame_buttons,
                                                            text=l0_day, 
                                                            width=self.WIDTH_BTN,
                                                            command=lambda day_id=l0_i : self.controller.chooseDayToShowInApp(day_id))
    
    def _makePortionsAppWidgets(self):
        # these elements are not displayed at the begining
        self.btn_hide_portionsApp = tk.Button(self.frame_buttons, 
                                           text="Retour", 
                                           command=self.controller.hidePortionsApp, 
                                           width=self.WIDTH_BTN)

        self.frame_portionsApp = tk.Frame(self.frame_content, 
                                            bg=self.BG_CLR_2,  
                                            width=self.WIDTH_CONTENT_AREA)   

    def makeDaysFrames(self):
        e_temp_recettes = self.controller.getDictRecettes()
        for l0_i, l0_day in enumerate(g_const.WEEK_DAYS):
            self.frame_by_day[l0_i] = tk.Frame(self.frame_portionsApp, 
                                       width=self.WIDTH_CONTENT_AREA)
            self.label_by_day[l0_i] = tk.Label(self.frame_by_day[l0_i], 
                                       text=g_const.WEEK_DAYS[l0_i],
                                       width=self.WIDTH_CONTENT_AREA)
            self.label_by_day[l0_i].pack(pady=2)
            for l1_i, l1_day_meal in enumerate(e_temp_recettes[str(l0_i)].values()):
                e_var_current_btn_txt = tk.StringVar()
                ds.separator()
                e_frame_slider_by_meal = tk.Frame(self.frame_by_day[l0_i], 
                                                   width=self.WIDTH_CONTENT_AREA)
                e_btn_by_meal = tk.Button(e_frame_slider_by_meal, 
                                                       text="Valider",
                                                       textvariable=e_var_current_btn_txt)
                e_var_current_btn_txt.set("Valider")
                e_scale_by_meal = tk.Scale(e_frame_slider_by_meal, 
                                        orient='horizontal', 
                                        from_=0, to=3,
                                        resolution=1, 
                                        tickinterval=1, 
                                        length=self.WIDTH_CONTENT_AREA/2, 
                                        label=l1_day_meal['name'])  
                e_scale_by_meal.set(e_temp_recettes[str(l0_i)][str(l1_i+1)]["portions"])
                e_btn_by_meal['command'] = lambda day_id=l0_i, meal_id=l1_i, scale=e_scale_by_meal, btn_text=e_var_current_btn_txt: self.controller.updatePortion(day_id, meal_id, scale, btn_text)
                e_frame_slider_by_meal.pack(pady=2)
                e_scale_by_meal.pack()
                e_btn_by_meal.pack() 

    def _showEmptySpace(self):
        self.label_space.pack(fill='x', pady=2)
    
    def _hideEmptySpace(self):
        self.label_space.pack_forget()
    
    def _showStartButton(self):
        self.btn_opt_start.pack(fill='x', pady=2)
    
    def hideStartButton(self):
        self.btn_opt_start.pack_forget()
        
    def showNavButtons(self):
        self.btn_opt_menu.pack(fill='x', pady=2)
        self.btn_opt_download.pack(fill='x', pady=2)
        self.btn_opt_portionsApp.pack(fill='x', pady=2)
        self.btn_opt_ingredients.pack(fill='x', pady=2)
        self.btn_opt_exportIngredients.pack(fill='x', pady=2)
        
    def hideNavButtons(self):
        self.btn_opt_download.pack_forget()
        self.btn_opt_menu.pack_forget()
        self.btn_opt_portionsApp.pack_forget()
        self.btn_opt_ingredients.pack_forget()
        self.btn_opt_exportIngredients.pack_forget()
    
    def showDaysButtons(self):
        self._showEmptySpace()
        for l0_i in range(len(g_const.WEEK_DAYS)):
            self.btn_choosing_day[l0_i].pack(fill='x', pady=2)
    
    def hideDaysButtons(self):
        self._hideEmptySpace()
        for l0_i in range(len(g_const.WEEK_DAYS)):
            self.btn_choosing_day[l0_i].pack_forget()

    def showDaysButtonsInApp(self):
        self._showEmptySpace()
        for l0_i in range(len(g_const.WEEK_DAYS)):
            self.btn_choosing_day_in_app[l0_i].pack(fill='x', pady=2)
    
    def hideDaysButtonsInApp(self):
        self._hideEmptySpace()
        for l0_i in range(len(g_const.WEEK_DAYS)):
            self.btn_choosing_day_in_app[l0_i].pack_forget()
    
    def _showContent(self):
        self.frame_content.pack(side='left', expand=1, fill='both', padx=self.PADX_CONTENT)

    def showContentMessage(self):
        self.message_content.pack(fill='both', ipady=10, ipadx=50)
        
    def hideContentMessage(self):
        self.message_content.pack_forget()
    
    def showPortionsScalesByDay(self, p_asked_day):
        self.frame_by_day[p_asked_day].pack(pady=2)
        
    def hidePortionsScalesByDay(self):
        e_asked_day_in_app = self.controller.getAskedDayInPortionsApp()
        self.frame_by_day[e_asked_day_in_app].pack_forget()
